#!/usr/bin/env python3
"""
inject_backlinks.py — for each new post, propose reverse links from old posts in same cluster.

Output: data/backlink-proposals.json (human reviewable).
Apply with:  python3 scripts/inject_backlinks.py --apply

Algorithm (per new post):
  1. Find old posts in same cluster (top 3 by date, within last 6 months).
  2. For each, ask the LLM to suggest:
     - insertion_h2_index (which H2 to target)
     - anchor_text (descriptive, 2-5 words)
     - context_sentence (verbatim sentence to find in the H2 block)
     - justification (why this link is relevant)
  3. Verify the context_sentence exists in the source HTML. If not, skip.
  4. Replace the source sentence with itself + " (<a href='/blog/<new>.html'>anchor</a>)".
  5. Write to a proposal JSON. On --apply, write the modified HTML to disk.

Run weekly, ideally after each new post is generated.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from html import escape

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from lib.llm_client import LLMClient, LLMError

DATA = REPO / "data"
POSTS_JSON = DATA / "posts.json"
PROPOSALS = DATA / "backlink-proposals.json"
BLOG = REPO / "blog"


def load_posts() -> list:
    return json.loads(POSTS_JSON.read_text(encoding="utf-8"))["posts"]


def find_new_posts(posts: list, days: int = 14) -> list:
    """Posts with generated_by set, or posted in the last N days."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    out = []
    for p in posts:
        if p.get("generated_by") or p.get("date", "") >= cutoff:
            out.append(p)
    return out


def find_targets(posts: list, new_post: dict, max_targets: int = 3) -> list:
    """Find old posts in same cluster, recent first, not the same slug."""
    same = [p for p in posts
            if p["slug"] != new_post["slug"]
            and p.get("cluster") == new_post.get("cluster")
            and p.get("language", "es") == "es"]
    same.sort(key=lambda p: (p.get("date", ""), p["slug"]), reverse=True)
    return same[:max_targets]


def get_h2_blocks(html: str) -> list[dict]:
    """Return list of {h2, start, end, body} from the article body."""
    m = re.search(r'<article[^>]*class="article-body"[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    body = m.group(1)
    # Strip script blocks
    body = re.sub(r'<script.*?</script>', '', body, flags=re.DOTALL)
    # Split on H2
    parts = re.split(r'(<h2[^>]*>.*?</h2>)', body, flags=re.IGNORECASE | re.DOTALL)
    blocks = []
    h2 = None
    content_start = 0
    for i, p in enumerate(parts):
        if re.match(r'<h2[^>]*>.*?</h2>', p, re.IGNORECASE | re.DOTALL):
            if h2 is not None:
                blocks.append({"h2": h2, "content": "".join(parts[content_start:i])})
            h2 = re.sub(r'<[^>]+>', '', p).strip()
            content_start = i + 1
    if h2 is not None:
        blocks.append({"h2": h2, "content": "".join(parts[content_start:])})
    return blocks


def suggest_injection(client: LLMClient, new_post: dict, old_post: dict) -> dict | None:
    """Ask the LLM where in the old post to insert a link to the new post."""
    target_path = REPO / old_post["path"].lstrip("/")
    if not target_path.exists():
        return None
    html = target_path.read_text(encoding="utf-8", errors="replace")
    blocks = get_h2_blocks(html)
    if not blocks:
        return None
    blocks_summary = [{"h2": b["h2"], "preview": re.sub(r"\s+", " ", b["content"])[:200]} for b in blocks[:8]]

    user = json.dumps({
        "old_post_title": old_post["title"],
        "old_post_h2_blocks": blocks_summary,
        "new_post_title": new_post["title"],
        "new_post_url": f"/blog/{new_post['slug']}.html",
        "new_post_summary": (new_post.get("description") or "")[:200],
    }, ensure_ascii=False)

    schema = {
        "selected_h2_index": 0,  # int
        "context_sentence_verbatim": "string from the h2 content",
        "anchor_text": "2-5 word anchor, descriptive, no 'click aquí'",
        "justification": "one sentence explaining the link relevance",
    }
    prompt = (
        "Suggest ONE natural place to insert a link to a new blog post in an older blog post.\n"
        "Return ONLY JSON with: selected_h2_index (0-based), context_sentence_verbatim "
        "(EXACT substring from the chosen h2's content), anchor_text, justification.\n"
        "If no good insertion point exists, return {\"skip\": true}.\n\n"
        + user
    )
    try:
        result = client.call_json(
            ["00_voice.md"],
            user_input=prompt,
            temperature=0.2,
            max_tokens=600,
        )
    except LLMError as e:
        print(f"  [skip] LLM error: {e}")
        return None
    if result.get("skip"):
        return None
    return result


def apply_injection(html: str, proposal: dict) -> str | None:
    """Find context_sentence_verbatim in html, append the link."""
    sentence = proposal.get("context_sentence_verbatim", "").strip()
    if not sentence:
        return None
    # Strip HTML from sentence for matching
    sentence_text = re.sub(r"<[^>]+>", "", sentence)
    sentence_text = re.sub(r"\s+", " ", sentence_text).strip()
    if not sentence_text:
        return None
    # Find the sentence in html (allow for whitespace variation)
    pattern = re.escape(sentence_text[:60])  # first 60 chars as anchor
    # Find the first occurrence
    m = re.search(pattern, html, re.IGNORECASE)
    if not m:
        return None
    # Build the link suffix
    anchor = escape(proposal.get("anchor_text", "sigue leyendo"))
    url = proposal.get("new_post_url", "")
    if not url:
        return None
    insertion = (
        f' <a href="{escape(url)}" '
        f'style="color:var(--accent-color,#6366f1);text-decoration:underline;">'
        f'Lee también: {anchor} →</a>'
    )
    # Insert after the matched sentence
    end = m.end()
    return html[:end] + insertion + html[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply the proposals and write modified HTML files.")
    ap.add_argument("--days", type=int, default=14, help="Consider posts from last N days as 'new'.")
    ap.add_argument("--max-targets", type=int, default=3, help="Max reverse links per new post.")
    args = ap.parse_args()

    if not POSTS_JSON.exists():
        print("ERROR: data/posts.json missing.")
        sys.exit(1)
    posts = load_posts()
    new_posts = find_new_posts(posts, days=args.days)
    if not new_posts:
        print("No new posts in the last", args.days, "days. Nothing to do.")
        return

    print(f"New posts ({len(new_posts)}):")
    for p in new_posts:
        print(f"  - {p['slug']} ({p.get('date', '?')})")
    print()

    try:
        client = LLMClient()
    except LLMError as e:
        print("ERROR:", e)
        sys.exit(1)

    proposals = []
    for new in new_posts:
        print(f"==> {new['slug']}")
        targets = find_targets(posts, new, max_targets=args.max_targets)
        for old in targets:
            print(f"  -> target: {old['slug']} ({old.get('date', '?')})")
            prop = suggest_injection(client, new, old)
            if not prop:
                print("    [skip] no good insertion point")
                continue
            prop["new_post_slug"] = new["slug"]
            prop["new_post_url"] = f"/blog/{new['slug']}.html"
            prop["old_post_slug"] = old["slug"]
            prop["old_post_path"] = old["path"]
            proposals.append(prop)
            print(f"    proposed: h2#{prop.get('selected_h2_index')} anchor='{prop.get('anchor_text')}'")

    PROPOSALS.write_text(json.dumps({"last_updated": datetime.now(timezone.utc).isoformat(),
                                     "proposals": proposals}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(proposals)} proposals to {PROPOSALS.relative_to(REPO)}")

    if args.apply:
        if not proposals:
            print("No proposals to apply.")
            return
        applied = 0
        for prop in proposals:
            target = REPO / prop["old_post_path"].lstrip("/")
            if not target.exists():
                continue
            html = target.read_text(encoding="utf-8", errors="replace")
            new_html = apply_injection(html, prop)
            if new_html is None:
                print(f"  [skip] {prop['old_post_slug']}: context sentence not found")
                continue
            target.write_text(new_html, encoding="utf-8")
            print(f"  [applied] {prop['old_post_slug']} ← {prop['new_post_slug']}")
            applied += 1
        print(f"\nApplied {applied} injections. Run `git diff` to review.")
    else:
        print("\nRun with --apply to write the changes. Recommend: review proposals first.")


if __name__ == "__main__":
    main()
