#!/usr/bin/env python3
"""
Build data/topic-queue.json — ranked list of candidate topics.

For the initial seed, this is populated manually from known D2C España trends.
The topic_research.py script extends this weekly by scraping Reddit, Quora,
Spanish marketing blogs, and Google Trends.

Run from repo root:  python3 scripts/build_topic_queue.py --seed
"""
import json
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
POSTS = DATA / "posts.json"
QUEUE = DATA / "topic-queue.json"


def load_posts() -> list:
    if not POSTS.exists():
        return []
    return json.loads(POSTS.read_text(encoding='utf-8'))["posts"]


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9áéíóúñü\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:80]


def is_duplicate(topic: str, posts: list) -> bool:
    """Fuzzy dedup: same slug stem, or topic is substring of a title."""
    topic_slug = slugify(topic)
    for p in posts:
        if p["slug"] == topic_slug:
            return True
        title_slug = slugify(p["title"])
        if topic_slug in title_slug or title_slug in topic_slug:
            if len(topic_slug) > 10:
                return True
    return False


# Seed topics — based on D2C España trends May/June 2026.
# Real sources: r/marketingdigital_es, r/PPC, marketing4ecommerce, IAB Spain.
SEED_TOPICS = [
    {
        "topic": "CAPI server-side y EMQ en 2026: qué cambia y cómo implementarlo en Shopify sin perder eventos",
        "cluster": "attribution-tracking",
        "search_intent": "transactional",
        "rationale": "Reddit r/FacebookAds top question May 2026: EMQ scores dropping. CAPI setup guide refresh needed.",
        "source": "reddit:r/FacebookAds",
        "score": 92,
    },
    {
        "topic": "Advantage+ Shopping vs campañas manuales en Meta Ads 2026: cuándo cada una rinde más",
        "cluster": "paid-media-foundations",
        "search_intent": "commercial",
        "rationale": "Quora top question — recurring debate since 2024. Updated 2026 data with case.",
        "source": "quora:meta-ads-espana",
        "score": 90,
    },
    {
        "topic": "TikTok Shop España 2026: funciona de verdad para D2C o es humo",
        "cluster": "paid-media-foundations",
        "search_intent": "commercial",
        "rationale": "Trending in r/Shopify and r/marketingdigital_es. Founders asking if it's worth the ops cost.",
        "source": "reddit:r/marketingdigital_es",
        "score": 88,
    },
    {
        "topic": "ROAS benchmark España 2026 por sector: moda, belleza, suplementos, hogar",
        "cluster": "unit-economics",
        "search_intent": "informational",
        "rationale": "Annual refresh of high-traffic benchmark post. Existing post from 2026-03 needs 2026-H1 data.",
        "source": "iab-spain:Q2-2026",
        "score": 86,
    },
    {
        "topic": "Generación de creatividades con IA para Meta Ads: qué funciona en 2026 y qué no",
        "cluster": "creative-testing",
        "search_intent": "commercial",
        "rationale": "Top question on r/PPC, r/marketing. AI creative tools (Midjourney, Runway, etc.) adoption in D2C.",
        "source": "reddit:r/PPC",
        "score": 85,
    },
    {
        "topic": "Estrategia first-party data post-cookies para D2C España en 2026",
        "cluster": "attribution-tracking",
        "search_intent": "informational",
        "rationale": "iOS 17/18 attribution + Chrome cookie deprecation. Practical D2C playbook.",
        "source": "marketing4ecommerce.net:2026-05",
        "score": 83,
    },
    {
        "topic": "Reels vs Stories para paid media en 2026: dónde está el ROAS",
        "cluster": "creative-testing",
        "search_intent": "commercial",
        "rationale": "Recurring Quora + Reddit question. Need a 2026-specific answer with current CPM data.",
        "source": "reddit:r/FacebookAds",
        "score": 80,
    },
    {
        "topic": "Broad targeting vs interest stacks en Meta Ads 2026: la decisión real",
        "cluster": "paid-media-foundations",
        "search_intent": "commercial",
        "rationale": "Ongoing debate. Meta's algorithm improvements make this a moving target.",
        "source": "reddit:r/PPC",
        "score": 78,
    },
    {
        "topic": "WhatsApp Business API + Meta Ads: cómo cerrar el funnel BOFU sin perder atribución",
        "cluster": "paid-media-foundations",
        "search_intent": "transactional",
        "rationale": "D2C founders in Spain asking how to integrate WhatsApp as a paid-conversion destination without breaking CAPI.",
        "source": "reddit:r/Shopify",
        "score": 76,
    },
    {
        "topic": "Server-side GTM con GA4 en 2026: la guía que Wish hubiera querido tener",
        "cluster": "attribution-tracking",
        "search_intent": "transactional",
        "rationale": "Existing post is high-level. Need a step-by-step implementation guide with screenshots-equivalents (ASCII diagrams).",
        "source": "marketing4ecommerce.net:2026-05",
        "score": 74,
    },
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", action="store_true", help="Seed initial 10 topics from SEED_TOPICS")
    ap.add_argument("--append", action="store_true", help="Append new topics (preserves queue)")
    args = ap.parse_args()

    DATA.mkdir(exist_ok=True)
    posts = load_posts()

    existing = {"completed_tasks": [], "pending_tasks": []}
    if QUEUE.exists() and args.append:
        existing = json.loads(QUEUE.read_text(encoding='utf-8'))

    if args.seed or not existing.get("pending_tasks"):
        # Dedup against existing posts
        new_topics = []
        for t in SEED_TOPICS:
            if is_duplicate(t["topic"], posts):
                print(f"  SKIP (dup): {t['topic'][:60]}")
                continue
            t["slug"] = slugify(t["topic"])
            t["discovered_at"] = datetime.now(timezone.utc).isoformat()
            t["status"] = "pending"
            t["id"] = f"T{100 + len(new_topics):03d}"
            new_topics.append(t)
        if args.append:
            existing["pending_tasks"] = new_topics + [
                p for p in existing.get("pending_tasks", []) if p["slug"] not in {t["slug"] for t in new_topics}
            ]
        else:
            existing["pending_tasks"] = new_topics
        existing["completed_tasks"] = existing.get("completed_tasks", [])
        existing["schema_version"] = "1.0"
        existing["last_updated"] = datetime.now(timezone.utc).isoformat()
        existing["total_pending"] = len(existing["pending_tasks"])
        existing["total_completed"] = len(existing["completed_tasks"])
        existing["source_note"] = "Seeded from D2C España trends May/June 2026. Extended weekly by scripts/topic_research.py."
        QUEUE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\nSeeded {len(new_topics)} topics to {QUEUE}")


if __name__ == "__main__":
    main()
