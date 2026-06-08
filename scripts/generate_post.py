#!/usr/bin/env python3
"""
generate_post.py — orchestrate the 9-step blog post generation pipeline.

Usage (from repo root):
  # Generate the next pending topic:
  python3 scripts/generate_post.py

  # Generate a specific topic by ID:
  python3 scripts/generate_post.py --topic T100

  # Dry run (research + plan only, no write):
  python3 scripts/generate_post.py --dry-run

  # Skip the audit step (faster, use only when iterating prompts):
  python3 scripts/generate_post.py --skip-audit

Steps:
  1. Pick topic from data/topic-queue.json
  2. Research pass (MiniMax M3) → JSON brief
  3. Verify external links (HEAD) + Wayback fallback
  4. Plan visuals (handled in step 5 prompt)
  5. Write article (MiniMax M3) → JSON output
  6. Audit pass (MiniMax M3) — score >= 18, retry max 2x
  7. Build JSON-LD schemas (local, no LLM)
  8. File assembly via post_builder.py
  9. Side effects: update posts.json, topic-queue.json, related links
"""
import argparse
import json
import os
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from lib.llm_client import LLMClient, LLMError
from lib.authority_link_checker import check_with_relevance, filter_survivors
from lib.post_builder import build as build_post_html
from lib.markdown_parser import parse as parse_md

DATA = REPO / "data"
BLOG = REPO / "blog"
TEMPLATE = REPO / "scripts" / "lib" / "post_template.html.j2"
TRUSTED_URLS = DATA / "trusted-urls.json"

POSTS_JSON = DATA / "posts.json"
QUEUE_JSON = DATA / "topic-queue.json"
LINKS_JSON = DATA / "internal-links.json"
CLUSTERS_JSON = DATA / "clusters.json"


def load_posts_index() -> dict:
    if not POSTS_JSON.exists():
        print("ERROR: data/posts.json missing — run scripts/build_posts_index.py first.")
        sys.exit(1)
    return json.loads(POSTS_JSON.read_text(encoding="utf-8"))


def save_posts_index(data: dict):
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    POSTS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_queue() -> dict:
    if not QUEUE_JSON.exists():
        print("ERROR: data/topic-queue.json missing — run scripts/build_topic_queue.py first.")
        sys.exit(1)
    return json.loads(QUEUE_JSON.read_text(encoding="utf-8"))


def save_queue(q: dict):
    q["last_updated"] = datetime.now(timezone.utc).isoformat()
    q["total_pending"] = len(q.get("pending_tasks", []))
    q["total_completed"] = len(q.get("completed_tasks", []))
    QUEUE_JSON.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")


def pick_topic(queue: dict, topic_id: str | None) -> dict | None:
    pending = queue.get("pending_tasks", [])
    if not pending:
        return None
    if topic_id:
        for t in pending:
            if t["id"] == topic_id:
                return t
        print(f"ERROR: topic {topic_id} not in pending queue.")
        sys.exit(1)
    return pending[0]  # top-scored, already sorted by score


def pick_related(cluster: str, all_posts: list, exclude_slug: str, n: int = 3) -> list[tuple[str, str]]:
    """Pick up to N recent posts in same cluster for the related-posts section."""
    same = [p for p in all_posts if p.get("cluster") == cluster and p["slug"] != exclude_slug]
    same.sort(key=lambda p: p.get("date", ""), reverse=True)
    return [(p["slug"], p["title"]) for p in same[:n]]


def step_research(client: LLMClient, topic: dict) -> dict:
    print(f"[1/9] Research pass for: {topic['topic'][:70]}")
    trusted = load_trusted_urls_for_cluster(topic.get("cluster", ""))
    # Compress trusted to just url+tags+why to save tokens
    compressed = [{"url": e["url"], "tags": e.get("topic_tags", []), "why": e.get("why", "")} for e in trusted]
    user = json.dumps({
        "topic": topic["topic"],
        "cluster": topic["cluster"],
        "search_intent": topic.get("search_intent", "informational"),
        "rationale": topic.get("rationale", ""),
        "trusted_urls_disponibles": compressed,  # LLM picks from this, never invents
    }, ensure_ascii=False)
    brief = client.call_json(
        ["00_voice.md", "01_research.md"],
        user_input=user,
        temperature=0.3,
        max_tokens=4000,
    )
    return brief


def load_trusted_urls_for_cluster(cluster: str) -> list[dict]:
    """Return the trusted-urls entries for a cluster (or [] if missing)."""
    if not TRUSTED_URLS.exists():
        print(f"  [WARN] {TRUSTED_URLS} missing — external links will be empty.")
        return []
    data = json.loads(TRUSTED_URLS.read_text(encoding="utf-8"))
    return data.get("by_cluster", {}).get(cluster, [])


def step_verify_links(brief: dict, client: LLMClient, topic_title: str) -> dict:
    """HEAD + Wayback + LLM relevance check. Topic is the article's title for relevance."""
    print(f"[2/9] Verifying {len(brief.get('external_authority_targets', []))} external links (HEAD + Wayback + LLM relevance)…")
    targets = brief.get("external_authority_targets", [])
    if not targets:
        brief["external_authority_targets_verified"] = []
        return brief
    # Relevance check is the most expensive — only run if HEAD passes (saves time)
    verified = []
    for t in targets:
        url = t.get("url", "")
        if not url:
            continue
        r = check_with_relevance(url, topic_title, client=client, min_relevance=5)
        if r["ok"]:
            tag = "OK"
            if r.get("relevance_reason"):
                tag += f" rel={r['relevance']}/10"
            print(f"  ✓ [{r['status']}] {tag} {url[:70]}")
            verified.append({**t, "ok": True, "status": r["status"],
                             "relevance": r.get("relevance", 0),
                             "relevance_reason": r.get("relevance_reason", "")})
        elif r.get("wayback"):
            print(f"  ↪ [wayback] {url[:70]}")
            verified.append({**t, "ok": False, "wayback": r["wayback"], "status": r["status"]})
        else:
            reason = r.get("fail_reason", str(r["status"]))
            print(f"  ✗ [{r['status']}] ({reason}) {url[:70]}")
    brief["external_authority_targets_verified"] = verified
    return brief


def step_write(client: LLMClient, topic: dict, brief: dict, internal_links: list[dict]) -> dict:
    print("[3/9] Writing article (markdown mode for M3 speed)…")
    user = json.dumps({
        "topic": topic["topic"],
        "cluster": topic["cluster"],
        "research": brief,
        "internal_links": internal_links,
    }, ensure_ascii=False)
    md = client.call(
        ["00_voice.md", "03_write_es.md"],
        user_input=user,
        temperature=0.5,
        max_tokens=12000,  # M3 thinking ~3K; actual output ~1.5K; cap at 16K in client
        json_mode=False,
        save_raw_path=".last-write-raw.md",
    )
    parsed = parse_md(md)
    if not parsed.get("title"):
        # Partial recovery: try to extract title from first heading
        for line in md.splitlines()[:5]:
            if line.strip().startswith("# "):
                parsed["title"] = line.strip("# ").strip()
                break
    if not parsed.get("title"):
        raise LLMError("markdown parser produced empty title; check .last-write-raw.md")
    return parsed


def step_audit(client: LLMClient, llm: dict, topic: dict, brief: dict) -> dict:
    print("[4/9] Auditing article…")
    user = (
        f"Topic: {topic['topic']}\n"
        f"Research brief: {json.dumps(brief, ensure_ascii=False)[:1500]}\n"
        f"Article draft: {json.dumps(llm, ensure_ascii=False)[:14000]}"
    )
    audit = client.call_json(
        ["00_voice.md", "02_audit.md"],
        user_input=user,
        temperature=0.1,
        max_tokens=1500,
    )
    return audit


def step_write_with_feedback(client: LLMClient, topic: dict, brief: dict, internal_links: list[dict],
                             feedback: str) -> dict:
    print(f"  [rewrite] Applying feedback: {feedback[:80]}…")
    user = json.dumps({
        "topic": topic["topic"],
        "cluster": topic["cluster"],
        "research": brief,
        "internal_links": internal_links,
        "feedback_from_audit": feedback,
    }, ensure_ascii=False)
    md = client.call(
        ["00_voice.md", "03_write_es.md"],
        user_input=user,
        temperature=0.5,
        max_tokens=12000,
        json_mode=False,
        save_raw_path=".last-write-raw.md",
    )
    return parse_md(md)


def step_assemble(llm: dict, topic: dict, posts_index: dict, related: list, template_str: str) -> str:
    print("[5/9] Assembling HTML…")
    by_slug = {p["slug"]: p for p in posts_index["posts"]}
    meta = {
        "slug": topic["slug"],
        "title": llm["title"],
        "meta_description": llm["meta_description"],
        "date": topic.get("publish_date", datetime.now().strftime("%Y-%m-%d")),
        "category": topic.get("category", "Estrategia"),
        "keywords_secundarias": [],  # could be added later
    }
    return build_post_html(llm, meta, template_str, related, by_slug)


def step_persist(html: str, topic: dict, llm: dict, posts_index: dict) -> Path:
    print("[6/9] Persisting files…")
    out_path = BLOG / f"{topic['slug']}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  wrote: {out_path.relative_to(REPO)}")

    # Update posts.json
    new_entry = {
        "slug": topic["slug"],
        "path": f"/blog/{topic['slug']}.html",
        "url": f"https://www.daybydayconsulting.com/blog/{topic['slug']}.html",
        "title": llm["title"],
        "description": llm["meta_description"],
        "category": topic.get("category", "Estrategia"),
        "date": topic.get("publish_date", datetime.now().strftime("%Y-%m-%d")),
        "reading_time_min": max(1, int(llm.get("word_count_estimate", 1500)) // 220),
        "language": "es",
        "word_count": llm.get("word_count_estimate", 1500),
        "faqs_count": len(llm.get("faqs", [])),
        "cluster": topic.get("cluster", "paid-media-foundations"),
        "canonical": f"https://www.daybydayconsulting.com/blog/{topic['slug']}.html",
        "file_mtime": datetime.now(timezone.utc).isoformat(),
        "generated_by": "scripts/generate_post.py",
    }
    # Don't duplicate
    posts_index["posts"] = [p for p in posts_index["posts"] if p["slug"] != topic["slug"]]
    posts_index["posts"].insert(0, new_entry)
    posts_index["posts"].sort(key=lambda p: (p.get("date", ""), p["slug"]), reverse=True)
    posts_index["total_posts"] = len(posts_index["posts"])
    save_posts_index(posts_index)
    print(f"  updated: data/posts.json ({posts_index['total_posts']} posts)")
    return out_path


def step_update_queue(queue: dict, topic: dict) -> None:
    print("[7/9] Updating topic queue…")
    queue["pending_tasks"] = [t for t in queue["pending_tasks"] if t["id"] != topic["id"]]
    completed = queue.setdefault("completed_tasks", [])
    completed.append({
        "id": topic["id"],
        "slug": topic["slug"],
        "topic": topic["topic"],
        "cluster": topic.get("cluster"),
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "publish_date": topic.get("publish_date", datetime.now().strftime("%Y-%m-%d")),
    })
    save_queue(queue)


def step_regenerate_indexes() -> None:
    print("[8/9] Regenerating indexes (run scripts/regenerate_index.py)…")
    import subprocess
    r = subprocess.run(
        ["python3", str(REPO / "scripts" / "regenerate_index.py")],
        cwd=str(REPO),
    )
    if r.returncode != 0:
        print("WARN: regenerate_index.py failed; you can run it manually.")


def step_git_commit(topic: dict, llm: dict) -> None:
    print("[9/9] Git commit + push (no — manual, only when you've reviewed)…")
    # Not auto-committing. User reviews first.


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", help="Specific topic ID (e.g. T100). Default: top-scored pending.")
    ap.add_argument("--dry-run", action="store_true", help="Research + write to /tmp, don't write to repo.")
    ap.add_argument("--skip-audit", action="store_true", help="Skip the audit step (faster iteration).")
    ap.add_argument("--auto-accept", action="store_true", help="Accept any audit verdict (still run audit, don't fail).")
    args = ap.parse_args()

    queue = load_queue()
    posts_index = load_posts_index()
    topic = pick_topic(queue, args.topic)
    if not topic:
        print("No pending topics. Run scripts/build_topic_queue.py --seed or scripts/topic_research.py.")
        sys.exit(1)
    print(f"==> Topic {topic['id']} | {topic['cluster']} | score {topic['score']}")
    print(f"    {topic['topic']}")

    template_str = TEMPLATE.read_text(encoding="utf-8")

    client = LLMClient()

    # Step 1-2: research + verify (with LLM relevance)
    brief = step_research(client, topic)
    if not args.dry_run:
        brief = step_verify_links(brief, client, topic["topic"])
    # Map internal_link_targets to {slug, anchor} pairs from posts_index
    by_slug = {p["slug"]: p for p in posts_index["posts"]}
    internal_links = []
    for t in brief.get("internal_link_targets", []):
        if t in by_slug:
            p = by_slug[t]
            internal_links.append({"slug": t, "title": p["title"], "category": p.get("category", "")})

    # Step 3: write
    llm = step_write(client, topic, brief, internal_links)

    # Step 4: audit
    if not args.skip_audit:
        for attempt in range(1, 3):
            audit = step_audit(client, llm, topic, brief)
            score = audit.get("score_total", 0)
            verdict = audit.get("verdict", "reescribir")
            print(f"  [audit attempt {attempt}] score={score}/30 verdict={verdict} lista_negra={audit.get('lista_negra_count', '?')}")
            if score >= 22 and verdict == "publicar":
                break
            if args.auto_accept or attempt == 2:
                print(f"  [audit] accepting despite verdict={verdict} score={score}")
                break
            feedback = audit.get("feedback_especifico", "Reescribe aplicando el checklist de auditoría.")
            llm = step_write_with_feedback(client, topic, brief, internal_links, feedback)

    # Step 5: assemble
    related = pick_related(topic["cluster"], posts_index["posts"], topic["slug"], n=3)
    html = step_assemble(llm, topic, posts_index, related, template_str)

    if args.dry_run:
        dry = REPO / ".dry-run-post.html"
        dry.write_text(html, encoding="utf-8")
        print(f"\nDRY RUN: wrote to {dry.relative_to(REPO)}")
        print(f"Title: {llm['title']}")
        print(f"Description: {llm['meta_description']}")
        return

    # Step 6-9: persist + update indexes + queue
    step_persist(html, topic, llm, posts_index)
    step_update_queue(queue, topic)
    step_regenerate_indexes()
    step_git_commit(topic, llm)

    print(f"\n✓ Generated: blog/{topic['slug']}.html")
    print(f"  Title:   {llm['title']}")
    print(f"  Length:  {llm.get('word_count_estimate', '?')} words")
    print(f"  FAQs:     {len(llm.get('faqs', []))}")
    print(f"  Cluster: {topic['cluster']}")
    print(f"\nNext: review the file in your editor, then:")
    print(f"  git add blog/{topic['slug']}.html data/ && git commit -m 'post: {topic['slug']}' && git push")


if __name__ == "__main__":
    main()
