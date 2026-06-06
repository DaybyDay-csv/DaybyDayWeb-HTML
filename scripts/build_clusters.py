#!/usr/bin/env python3
"""
Build data/clusters.json and data/internal-links.json from data/posts.json.

Clusters: 5 thematic buckets.
Assignment: keyword scoring against title + description.
Edges: seed graph from same-cluster + category co-occurrence.
"""
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent
POSTS = REPO / "data" / "posts.json"
CLUSTERS_OUT = REPO / "data" / "clusters.json"
LINKS_OUT = REPO / "data" / "internal-links.json"

# Cluster definitions: name, description, strong keywords (1.0), weak (0.5)
CLUSTERS = [
    {
        "id": "paid-media-foundations",
        "name_es": "Paid Media Foundations",
        "name_es_short": "Fundamentos Paid Media",
        "description": "Conceptos base de paid media en Meta/Google/TikTok/LinkedIn para D2C España.",
        "keywords_strong": [
            "meta ads", "google ads", "tiktok ads", "linkedin ads", "paid media",
            "meta-ads", "cbo", "abo", "advantage+", "advantage plus",
            "estructura de cuenta", "campañas", "públicos", "audiencias",
            "retargeting", "remarketing", "pixel", "capi", "conversions api",
            "creatividades", "creative testing", "embudo", "full funnel",
        ],
        "keywords_weak": [
            "publicidad", "anuncios", "performance max", "performance max",
            "broad", "lookalike", "intereses", "presupuesto", "spend", "cpa",
        ],
    },
    {
        "id": "attribution-tracking",
        "name_es": "Attribution & Tracking",
        "name_es_short": "Tracking y Atribución",
        "description": "Implementación técnica de tracking, atribución, GA4, GTM, server-side.",
        "keywords_strong": [
            "tracking", "atribución", "attribution", "ga4", "gtm", "google tag manager",
            "server-side", "server side", "conversions api", "capi", "pixel",
            "ios 14", "ios atribucion", "atribución ios", "modelos de atribución",
            "marketing mix modeling", "mmm", "incrementality", "incrementality testing",
            "emq", "event quality", "first-party data", "cookieless",
        ],
        "keywords_weak": [
            "medición", "medicion", "analytics", "dashboards", "kpis",
            "reportes", "report", "métricas", "metri",
        ],
    },
    {
        "id": "creative-testing",
        "name_es": "Creative & UGC",
        "name_es_short": "Creatividades y UGC",
        "description": "Producción de creatividades, testing, UGC, hooks, formatos ganadores.",
        "keywords_strong": [
            "ugc", "creatividad", "creatividades", "creative testing", "creative",
            "hooks", "hook", "guion", "storytelling", "video", "vídeo",
            "formato", "reel", "tiktok", "spark ads", "partnership ads",
            "meta ads library", "ad library", "benchmark creativo", "fatiga creativa",
            "ad fatigue",
        ],
        "keywords_weak": [
            "contenido", "imagen", "diseño", "branding", "marca",
        ],
    },
    {
        "id": "unit-economics",
        "name_es": "Unit Economics & Strategy",
        "name_es_short": "Unit Economics y Estrategia",
        "description": "CAC, LTV, MER, payback, márgenes, pricing, escalado, unit economics.",
        "keywords_strong": [
            "cac", "ltv", "mer", "payback", "roas", "aov", "margen",
            "unit economics", "cohorte", "cohorte", "cohort", "cohort analysis",
            "escalar", "escala", "scaling", "unit economics",
            "pricing", "precio", "decisión de precio",
            "cash conversion", "cash-conversion", "flujo de caja",
            "presupuesto mínimo", "sueldo", "rentabilidad",
        ],
        "keywords_weak": [
            "estrategia", "crecimiento", "growth", "kpi", "benchmark", "sector",
        ],
    },
    {
        "id": "agency-selection",
        "name_es": "Agency Selection & Operations",
        "name_es_short": "Agencias y Operaciones",
        "description": "Elegir agencia, comparar in-house vs agencia, media buyer freelance, costes.",
        "keywords_strong": [
            "agencia", "agencias", "media buyer", "media-buyer", "freelance",
            "in-house", "inhouse", "in house", "contratar", "coste", "costes",
            "honorarios", "precio agencia", "red flags", "señales",
            "operaciones", "operativa", "framework",
        ],
        "keywords_weak": [
            "consultor", "consultora", "proveedor", "decisión", "decisiones de negocio",
            "automatización", "operations",
        ],
    },
]


def score_post(post: dict) -> dict:
    text = (post["title"] + " " + post["description"] + " " + post.get("category", "")).lower()
    scores = {}
    for c in CLUSTERS:
        s = 0
        for kw in c["keywords_strong"]:
            if kw in text:
                s += 2.0
        for kw in c["keywords_weak"]:
            if kw in text:
                s += 0.5
        scores[c["id"]] = s
    return scores


def assign(scores: dict) -> str:
    best = max(scores.values())
    if best == 0:
        return "paid-media-foundations"  # default
    # Tie-break: first cluster with max score
    for cid, s in scores.items():
        if s == best:
            return cid
    return "paid-media-foundations"


def slug_to_anchor(slug: str) -> str:
    """Best-effort human-readable anchor from slug."""
    s = slug.replace("-", " ")
    # Spanish diacritics recovery for common ones
    repl = {
        "meta ads": "Meta Ads", "google ads": "Google Ads", "tiktok ads": "TikTok Ads",
        "linkedin ads": "LinkedIn Ads", "capi": "CAPI", "cac": "CAC", "ltv": "LTV",
        "roas": "ROAS", "aov": "AOV", "mer": "MER", "ugc": "UGC",
        "ai": "AI", "ia": "IA", "d2c": "D2C", "ecommerce": "eCommerce",
        "espana": "España", "guia": "guía", "metodologia": "metodología",
        "audiencias": "audiencias", "lookalike": "lookalike", "performance max": "Performance Max",
    }
    out = []
    for word in s.split():
        out.append(repl.get(word.lower(), word))
    return " ".join(out)


def main():
    if not POSTS.exists():
        print(f"ERROR: {POSTS} missing — run build_posts_index.py first")
        return 1
    data = json.loads(POSTS.read_text(encoding='utf-8'))
    posts = data["posts"]

    # Cluster assignment
    cluster_buckets = defaultdict(list)
    for p in posts:
        scores = score_post(p)
        cid = assign(scores)
        p["cluster"] = cid
        p["cluster_scores"] = scores
        cluster_buckets[cid].append(p["slug"])

    # Save clusters
    clusters_doc = {
        "schema_version": "1.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_clusters": len(CLUSTERS),
        "clusters": [
            {
                **c,
                "post_count": len(cluster_buckets.get(c["id"], [])),
                "members": sorted(cluster_buckets.get(c["id"], [])),
            }
            for c in CLUSTERS
        ],
    }
    CLUSTERS_OUT.write_text(json.dumps(clusters_doc, ensure_ascii=False, indent=2), encoding='utf-8')

    # Build internal links graph: edges within same cluster (most recent N pairs)
    edges = []
    seen = set()
    for cid, members in cluster_buckets.items():
        members_sorted = sorted(
            [p for p in posts if p["slug"] in set(members)],
            key=lambda p: p["date"] or "",
            reverse=True,
        )
        # For each post, suggest links to 2 most recent older posts in same cluster
        for i, src in enumerate(members_sorted):
            targets = []
            # newer (forward links)
            for j, tgt in enumerate(members_sorted[:i]):
                if len(targets) >= 2:
                    break
                if tgt["slug"] != src["slug"]:
                    targets.append(tgt)
            for tgt in targets:
                key = tuple(sorted([src["slug"], tgt["slug"]]))
                if key in seen:
                    continue
                seen.add(key)
                edges.append({
                    "from": src["slug"],
                    "to": tgt["slug"],
                    "anchor": slug_to_anchor(tgt["slug"]),
                    "context": f"same_cluster:{cid}",
                    "auto_generated": True,
                })

    # Write posts.json back with cluster field
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    POSTS.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    # Links
    links_doc = {
        "schema_version": "1.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_edges": len(edges),
        "edges": edges,
    }
    LINKS_OUT.write_text(json.dumps(links_doc, ensure_ascii=False, indent=2), encoding='utf-8')

    # Summary
    print(f"Clusters: {len(CLUSTERS)}")
    for c in CLUSTERS:
        n = len(cluster_buckets.get(c['id'], []))
        print(f"  {c['id']:30s} {n:3d} posts")
    print(f"\nInternal edges: {len(edges)}")


if __name__ == "__main__":
    main()
