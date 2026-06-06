#!/usr/bin/env python3
"""
topic_research.py — weekly scrape of Reddit, Quora, ES marketing blogs.

Sources:
  - Reddit JSON:    https://www.reddit.com/r/<sub>/top.json?t=week (no auth)
  - Quora:          Google site-search fallback via DuckDuckGo HTML (no API key)
  - ES blog RSS:    marketing4ecommerce, brainsins, emprendedor digital, IAB Spain

Output: appends 6-10 candidate topics to data/topic-queue.json.

Run from repo root:
  python3 scripts/topic_research.py            # full pass
  python3 scripts/topic_research.py --dry      # preview only
  python3 scripts/topic_research.py --source reddit   # only one source
"""
import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

DATA = REPO / "data"
QUEUE = DATA / "topic-queue.json"
POSTS = DATA / "posts.json"

REDDIT_SUBS = [
    ("PPC", 0.6), ("FacebookAds", 1.0), ("GoogleAds", 0.7), ("marketing", 0.5),
    ("Shopify", 0.6), ("ecommerce", 0.5), ("marketingdigital_es", 1.0),
]

REDDIT_KEYWORDS = {
    "PPC": "paid-media-foundations",
    "FacebookAds": "paid-media-foundations",
    "GoogleAds": "paid-media-foundations",
    "marketing": "paid-media-foundations",
    "Shopify": "attribution-tracking",
    "ecommerce": "unit-economics",
    "marketingdigital_es": "paid-media-foundations",
}

ES_BLOGS_RSS = [
    ("https://marketing4ecommerce.net/feed/", "marketing4ecommerce", 0.9),
    ("https://iabspain.es/feed/", "iab-spain", 1.0),
    ("https://www.marketingdirecto.com/feed", "marketing-directo", 0.7),
]

# Google News RSS queries — work even when Reddit blocks us.
# `site:reddit.com` surfaces Reddit threads, `site:quora.com` surfaces Quora Qs.
GNEWS_QUERIES = [
    ("site:reddit.com/r/PPC meta ads españa", 0.7, "reddit"),
    ("site:reddit.com/r/FacebookAds ROAS 2026", 0.9, "reddit"),
    ("site:reddit.com/r/marketingdigital_es paid media", 0.9, "reddit"),
    ("site:reddit.com/r/Shopify CAPI conversions api", 0.8, "reddit"),
    ("site:reddit.com/r/Googleads pmax vs meta", 0.7, "reddit"),
    ("site:quora.com CAPI Meta Ads Shopify", 0.7, "quora"),
    ("site:quora.com agencia paid media españa", 0.7, "quora"),
    ("site:quora.com ROAS ecommerce españa 2026", 0.6, "quora"),
    ("meta ads españa 2026 tendencias", 0.6, "google-news"),
    ("CAPI conversions api setup 2026", 0.6, "google-news"),
    ("advantage+ shopping campaign 2026 d2c", 0.6, "google-news"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

UA = "DayByDay-BlogBot/1.0 (+https://daybydayconsulting.com) research; +respects noindex"


def fetch(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9áéíóúñü\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:80]


def is_duplicate(topic: str, posts: list) -> bool:
    topic_slug = slugify(topic)
    if len(topic_slug) < 10:
        return True
    for p in posts:
        if p["slug"] == topic_slug:
            return True
        title_slug = slugify(p["title"])
        if topic_slug in title_slug or title_slug in topic_slug:
            if len(topic_slug) > 10:
                return True
    return False


def is_question(s: str) -> bool:
    s = s.strip()
    return bool(s) and (
        s.endswith("?") or s.lower().startswith(("cómo ", "como ", "qué ", "que ", "por ", "cuál ", "cual ", "cuándo ", "cuando ", "dónde ", "donde "))
    )


# ---------------------------------------------------------------------------
# Reddit (via Google News RSS — Reddit blocks direct API access in 2026)
# ---------------------------------------------------------------------------

def scrape_reddit(limit: int = 8) -> list[dict]:
    out = []
    for query, weight, source_label in GNEWS_QUERIES:
        if source_label != "reddit":
            continue
        url = (
            "https://news.google.com/rss/search?"
            + urllib.parse.urlencode({"q": query, "hl": "es", "gl": "ES", "ceid": "ES:es"})
        )
        try:
            xml = fetch(url, timeout=10)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            print(f"  [gnews-reddit] {query[:40]}: {e}")
            continue
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as e:
            print(f"  [gnews-reddit] parse: {e}")
            continue
        for item in root.findall(".//item")[:limit]:
            title_el = item.find("title")
            link_el = item.find("link")
            if title_el is None or not title_el.text:
                continue
            raw_title = re.sub(r"\s+-\s+[^-]+$", "", title_el.text).strip()  # strip " - Source"
            if len(raw_title) < 12:
                continue
            link = link_el.text if link_el is not None else ""
            out.append({
                "topic": _title_to_topic(raw_title),
                "cluster": "paid-media-foundations",
                "search_intent": "commercial" if is_question(raw_title) else "informational",
                "rationale": f"Google News Reddit: {query}",
                "source": f"gnews:{query[:60]}",
                "source_url": link,
                "engagement": 40 * weight,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            })
        time.sleep(0.6)
    return out


def _title_to_topic(title: str) -> str:
    """Convert Reddit post title to a topic phrasing suitable for an article."""
    title = re.sub(r"^\[?[A-Z]{2,5}\]?:?\s*", "", title)
    title = title.rstrip(".?!")
    if title:
        title = title[0].upper() + title[1:]
    return title


# ---------------------------------------------------------------------------
# Quora (via Google News site-search)
# ---------------------------------------------------------------------------

def scrape_quora(limit_per_query: int = 3) -> list[dict]:
    out = []
    for query, weight, source_label in GNEWS_QUERIES:
        if source_label != "quora":
            continue
        url = (
            "https://news.google.com/rss/search?"
            + urllib.parse.urlencode({"q": query, "hl": "es", "gl": "ES", "ceid": "ES:es"})
        )
        try:
            xml = fetch(url, timeout=10)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            print(f"  [gnews-quora] {query[:40]}: {e}")
            continue
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as e:
            print(f"  [gnews-quora] parse: {e}")
            continue
        for item in root.findall(".//item")[:limit_per_query]:
            title_el = item.find("title")
            link_el = item.find("link")
            if title_el is None or not title_el.text:
                continue
            raw_title = re.sub(r"\s+-\s+[^-]+$", "", title_el.text).strip()
            if len(raw_title) < 12 or not is_question(raw_title):
                continue
            link = link_el.text if link_el is not None else ""
            out.append({
                "topic": raw_title.rstrip("?"),
                "cluster": "paid-media-foundations",
                "search_intent": "commercial",
                "rationale": f"Google News Quora: {query}",
                "source": f"gnews:{query[:60]}",
                "source_url": link,
                "engagement": 30 * weight,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            })
        time.sleep(0.6)
    return out


# ---------------------------------------------------------------------------
# ES marketing blogs via RSS
# ---------------------------------------------------------------------------

def scrape_es_blogs(limit: int = 5) -> list[dict]:
    out = []
    for url, label, weight in ES_BLOGS_RSS:
        try:
            rss = fetch(url, timeout=10)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            print(f"  [blog] {label}: {e}")
            continue
        try:
            root = ET.fromstring(rss)
        except ET.ParseError as e:
            print(f"  [blog] {label} parse: {e}")
            continue
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = list(root.findall(".//item")) or list(root.findall(".//atom:entry", ns))
        for item in items[:limit]:
            title_el = item.find("title")
            if title_el is None:
                title_el = item.find("atom:title", ns)
            link_el = item.find("link")
            if link_el is None:
                link_el = item.find("atom:link", ns)
            if title_el is None or title_el.text is None:
                continue
            title = re.sub(r"\s+", " ", title_el.text).strip()
            if len(title) < 12:
                continue
            link = ""
            if link_el is not None:
                link = link_el.text or link_el.attrib.get("href", "")
            if not link and item.find("guid") is not None:
                link = item.find("guid").text or ""
            # Filter out non-paid-media content (e.g. "se busca community manager")
            if not _looks_paid_media(title):
                continue
            out.append({
                "topic": title.rstrip(".?!"),
                "cluster": "paid-media-foundations",  # default; LLM can re-classify
                "search_intent": "informational",
                "rationale": f"Trending en {label} esta semana",
                "source": f"blog:{label}",
                "source_url": link,
                "engagement": 25 * weight,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            })
        time.sleep(0.4)
    return out


_PAID_MEDIA_KW = (
    "ads", "meta", "google", "tiktok", "linkedin", "paid", "capi", "pixel",
    "roas", "cpa", "ctr", "ecommerce", "shopify", "d2c", "conversiones",
    "atribución", "atr", "creatividad", "creatividades", "performance max",
    "advantage+", "compra", "venta", "ventas", "crm", "automation",
    "automatización", "ia", "ai", "agencia", "campaña", "campañas",
    "audiencia", "audiencias", "lookalike", "retargeting", "remarketing",
    "growth", "embudo", "escala", "métrica", "kpi", "tracker", "tracking",
    "ga4", "gtm", "gtag", "shopify", "klaviyo",
)
_BLOG_NEGATIVE_KW = (
    "se busca", "oferta de empleo", "concurso", "premio", "evento presencial",
    "sorteo", "ebook gratis",
)


def _looks_paid_media(title: str) -> bool:
    t = title.lower()
    if any(k in t for k in _BLOG_NEGATIVE_KW):
        return False
    return any(k in t for k in _PAID_MEDIA_KW)


# ---------------------------------------------------------------------------
# Scoring + dedup + push
# ---------------------------------------------------------------------------

def rank(candidates: list[dict]) -> list[dict]:
    """Sort by engagement desc."""
    return sorted(candidates, key=lambda c: c.get("engagement", 0), reverse=True)


def push_to_queue(candidates: list[dict], posts: list, max_new: int = 10) -> int:
    if not QUEUE.exists():
        print(f"ERROR: {QUEUE} missing — run scripts/build_topic_queue.py --seed first.")
        return 0
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    existing_slugs = {t["slug"] for t in q.get("pending_tasks", [])}
    existing_slugs |= {t["slug"] for t in q.get("completed_tasks", [])}
    added = 0
    for c in candidates:
        if added >= max_new:
            break
        if is_duplicate(c["topic"], posts):
            continue
        slug = slugify(c["topic"])
        if slug in existing_slugs or len(slug) < 10:
            continue
        # Compute priority score
        score = min(100, int(c.get("engagement", 0) / 5) + 50)
        c["slug"] = slug
        c["score"] = score
        c["status"] = "pending"
        next_id = 100 + len(q.get("pending_tasks", [])) + len(q.get("completed_tasks", [])) + added
        c["id"] = f"T{next_id:03d}"
        q.setdefault("pending_tasks", []).append(c)
        existing_slugs.add(slug)
        added += 1
    q["last_updated"] = datetime.now(timezone.utc).isoformat()
    q["total_pending"] = len(q["pending_tasks"])
    q["total_completed"] = len(q.get("completed_tasks", []))
    QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="Don't write; print summary.")
    ap.add_argument("--source", choices=["reddit", "quora", "blogs", "all"], default="all")
    ap.add_argument("--max-new", type=int, default=8, help="Max topics to add.")
    args = ap.parse_args()

    posts = []
    if POSTS.exists():
        posts = json.loads(POSTS.read_text(encoding="utf-8"))["posts"]

    candidates: list[dict] = []

    if args.source in ("reddit", "all"):
        print("== Reddit ==")
        candidates += scrape_reddit()
        print(f"  collected: {len(candidates)}")

    if args.source in ("quora", "all"):
        print("== Quora (via DDG) ==")
        before = len(candidates)
        candidates += scrape_quora()
        print(f"  collected: {len(candidates) - before}")

    if args.source in ("blogs", "all"):
        print("== ES marketing blogs ==")
        before = len(candidates)
        candidates += scrape_es_blogs()
        print(f"  collected: {len(candidates) - before}")

    candidates = rank(candidates)
    print(f"\nTotal candidates: {len(candidates)}")
    for c in candidates[:15]:
        eng = int(c.get("engagement", 0))
        print(f"  [{eng:4d}] {c['source']:35s} | {c['topic'][:70]}")

    if args.dry:
        print("\nDRY RUN — no files written.")
        return

    added = push_to_queue(candidates, posts, max_new=args.max_new)
    print(f"\nAdded {added} new topics to {QUEUE.relative_to(REPO)}")


if __name__ == "__main__":
    main()
