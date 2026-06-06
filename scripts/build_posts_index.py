#!/usr/bin/env python3
"""
Build data/posts.json by scanning /blog/*.html and extracting metadata.
Run from repo root. Stdlib only.
"""
import json
import re
import os
import sys
from pathlib import Path
from html import unescape
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent
BLOG_DIR = REPO / "blog"
DATA = REPO / "data"
OUT = DATA / "posts.json"

# Match inside <article class="article-body">...</article> for word/FAQ counts
RE_ARTICLE = re.compile(r'<article[^>]*>(.*?)</article>', re.DOTALL | re.IGNORECASE)
RE_FAQ_Q = re.compile(r'class="faq-q"[^>]*>([^<]+)<', re.IGNORECASE)
RE_FAQ_BLOCK = re.compile(r'<section[^>]*faq-section[^>]*>(.*?)</section>', re.DOTALL | re.IGNORECASE)
RE_TITLE = re.compile(r'<title>([^<]+)</title>', re.IGNORECASE)
RE_DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.IGNORECASE)
RE_CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE)
RE_CAT = re.compile(r'<span\s+class="category-badge"[^>]*>([^<]+)</span>', re.IGNORECASE)
RE_READ = re.compile(r'<span\s+class="reading-time"[^>]*>([^<]+)</span>', re.IGNORECASE)
RE_DATE = re.compile(r'<span\s+class="article-date"[^>]*>([^<]+)</span>', re.IGNORECASE)


def strip_html(s: str) -> str:
    s = re.sub(r'<[^>]+>', ' ', s)
    s = unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def word_count(html: str) -> int:
    art = RE_ARTICLE.search(html)
    body = art.group(1) if art else html
    text = strip_html(body)
    return len(text.split()) if text else 0


def faq_count(html: str) -> int:
    faq_block = RE_FAQ_BLOCK.search(html)
    if not faq_block:
        return 0
    return len(RE_FAQ_Q.findall(faq_block.group(1)))


def extract(post_path: Path) -> dict:
    html = post_path.read_text(encoding='utf-8', errors='replace')

    title_m = RE_TITLE.search(html)
    desc_m = RE_DESC.search(html)
    canon_m = RE_CANONICAL.search(html)
    cat_m = RE_CAT.search(html)
    read_m = RE_READ.search(html)
    date_m = RE_DATE.search(html)

    title = title_m.group(1).strip() if title_m else ""
    # Strip "| DayByDay Consulting" suffix
    title = re.sub(r'\s*\|\s*DayByDay Consulting\s*$', '', title).strip()

    description = desc_m.group(1).strip() if desc_m else ""
    canonical = canon_m.group(1).strip() if canon_m else ""

    category = cat_m.group(1).strip() if cat_m else "Sin categoría"
    reading_raw = read_m.group(1).strip() if read_m else "0 min de lectura"
    minutes = int(re.search(r'(\d+)', reading_raw).group(1)) if re.search(r'(\d+)', reading_raw) else 0

    date_raw = date_m.group(1).strip() if date_m else ""
    # Normalize date to YYYY-MM-DD
    date_norm = ""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            date_norm = datetime.strptime(date_raw, fmt).strftime("%Y-%m-%d")
            break
        except (ValueError, TypeError):
            continue
    if not date_norm and date_raw:
        date_norm = date_raw  # leave as-is if no format matched

    slug = post_path.stem  # e.g. abtesting-meta-ads-que-testar-primero

    return {
        "slug": slug,
        "path": f"/blog/{post_path.name}",
        "url": f"https://www.daybydayconsulting.com/blog/{post_path.name}",
        "title": title,
        "description": description,
        "category": category,
        "date": date_norm,
        "reading_time_min": minutes,
        "language": "es",
        "word_count": word_count(html),
        "faqs_count": faq_count(html),
        "canonical": canonical,
        "file_mtime": datetime.fromtimestamp(
            post_path.stat().st_mtime, tz=timezone.utc
        ).isoformat(),
    }


def main():
    if not BLOG_DIR.is_dir():
        print(f"ERROR: {BLOG_DIR} not found", file=sys.stderr)
        sys.exit(1)
    DATA.mkdir(exist_ok=True)
    files = sorted(BLOG_DIR.glob("*.html"))
    posts = [extract(p) for p in files]
    posts.sort(key=lambda p: (p["date"] or "", p["slug"]), reverse=True)

    out = {
        "schema_version": "1.0",
        "site": "https://www.daybydayconsulting.com",
        "language": "es",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(posts),
        "categories": sorted({p["category"] for p in posts if p["category"]}),
        "posts": posts,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote {len(posts)} posts to {OUT}")
    # Quick sanity
    no_date = [p["slug"] for p in posts if not p["date"]]
    no_title = [p["slug"] for p in posts if not p["title"]]
    if no_date:
        print(f"WARN: {len(no_date)} posts without parseable date: {no_date[:5]}")
    if no_title:
        print(f"WARN: {len(no_title)} posts without title: {no_title[:5]}")


if __name__ == "__main__":
    main()
