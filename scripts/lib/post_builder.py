#!/usr/bin/env python3
"""
post_builder.py — assemble the final HTML for a blog post from LLM output.

Inputs:
  - llm_output: dict (from 03_write_es.md prompt)
  - meta: dict (slug, date, category, reading_time, cluster, accent_color, ...)
  - related_slugs: list of (slug, title) tuples for related-posts section
  - template_str: rendered template (loaded by caller)

Output:
  - final HTML string
"""
import json
import re
from datetime import datetime
from html import escape

# Accent color per category
ACCENT_BY_CATEGORY = {
    "Estrategia": "#6366f1",
    "Meta Ads": "#1877f2",
    "Google Ads": "#4285f4",
    "TikTok Ads": "#ff0050",
    "LinkedIn Ads": "#0a66c2",
    "Tracking": "#10b981",
    "Métricas": "#f59e0b",
    "Creatividades": "#ec4899",
    "Unit Economics": "#14b8a6",
    "Automatización": "#8b5cf6",
    "Agencias": "#ef4444",
    "Casos de éxito": "#22c55e",
    "CRO": "#f97316",
    "Reporting": "#06b6d4",
    "Ecommerce": "#84cc16",
    "Estrategia D2C": "#6366f1",
    "Decisiones de negocio": "#64748b",
    "Marketing Digital": "#0ea5e9",
    "IA y Automatización": "#a855f7",
    "Investigación": "#0891b2",
    "Operaciones": "#475569",
    "Paid Media": "#6366f1",
    "Canales emergentes": "#f43f5e",
    "Estacional": "#eab308",
    "Internacionalización": "#0d9488",
    "Estructura de cuenta": "#7c3aed",
    "Medición": "#0d9488",
    "Technical Setup": "#2563eb",
    "Sin categoría": "#6366f1",
}


def _accent(category: str) -> str:
    return ACCENT_BY_CATEGORY.get(category, "#6366f1")


def _date_display(date_iso: str) -> str:
    """Convert 2026-06-06 to 6 de junio de 2026."""
    if not date_iso:
        return ""
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    try:
        d = datetime.strptime(date_iso, "%Y-%m-%d")
        return f"{d.day} de {months[d.month - 1]} de {d.year}"
    except ValueError:
        return date_iso


# Directive prefixes the LLM sometimes leaks into title/meta fields.
# The parser should strip them, but we also defend in depth here so the
# final HTML never ships with "TITLE:" or "META:" visible to users.
_LEAKED_PREFIXES = (
    "TITLE:", "Title:", "title:",
    "META:", "META DESCRIPTION:", "Meta:", "Meta Description:",
    "# ", "## ", "### ",
)


def _scrub_title(t: str) -> str:
    """Defensively strip leaked LLM directive prefixes from a title."""
    if not t:
        return ""
    t = t.strip()
    # Iteratively strip if multiple prefixes stacked
    changed = True
    while changed:
        changed = False
        for p in _LEAKED_PREFIXES:
            if t.startswith(p):
                t = t[len(p):].lstrip()
                changed = True
    # Strip suffix the template will add anyway
    t = re.sub(r"\s*\|\s*DayByDay Consulting\s*$", "", t)
    return t.strip()


def _word_count_estimate(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())


def _build_article_body(llm: dict) -> str:
    """Concatenate h2_blocks with paragraphs, h3, optional table/list inside each."""
    parts = []
    for blk in llm.get("h2_blocks", []):
        parts.append(f"<h2>{escape(blk.get('h2',''))}</h2>")
        if blk.get("paragraphs_html"):
            parts.append(blk["paragraphs_html"])
        for h3 in blk.get("h3_blocks", []):
            parts.append(f"<h3>{escape(h3.get('h3',''))}</h3>")
            if h3.get("paragraphs_html"):
                parts.append(h3["paragraphs_html"])
        if blk.get("table_html"):
            parts.append(blk["table_html"])
        if blk.get("list_html"):
            parts.append(blk["list_html"])
    return "\n".join(parts)


def _build_related(related_slugs: list, all_posts_by_slug: dict) -> str:
    if not related_slugs:
        return ""
    cards = []
    for slug, title in related_slugs[:3]:
        p = all_posts_by_slug.get(slug, {})
        cat = p.get("category", "Artículo")
        date = p.get("date", "")
        try:
            d = datetime.strptime(date, "%Y-%m-%d")
            date_str = d.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            date_str = date
        cards.append(
            f'<a class="related-card" href="/blog/{slug}.html">'
            f'<div class="related-card-title">{escape(title)}</div>'
            f'<div class="related-card-meta">{escape(cat)} · {date_str}</div>'
            f"</a>"
        )
    return (
        '<div class="related-posts">'
        '<div class="related-posts-title">Sigue leyendo</div>'
        + "\n".join(cards) +
        "</div>"
    )


def _build_faqs(faqs: list) -> str:
    parts = []
    for f in faqs:
        q = escape(f.get("q", ""))
        a = f.get("a", "")
        # Allow <strong> in a, but escape otherwise
        a_safe = re.sub(r"<script.*?</script>", "", a, flags=re.DOTALL)
        parts.append(f'<div class="faq-item"><h3>{q}</h3>{a_safe}</div>')
    return "\n".join(parts)


def _jsonld_article(meta: dict, llm: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta["title"],
        "description": meta["meta_description"],
        "datePublished": meta["date"],
        "dateModified": meta["date"],
        "inLanguage": "es-ES",
        "author": {
            "@type": "Person",
            "name": "Pablo Santirso",
            "url": "https://es.linkedin.com/in/pablo-santirso-perez",
            "jobTitle": "Founder, DayByDay Consulting",
            "worksFor": {"@type": "Organization", "name": "DayByDay Consulting"},
        },
        "publisher": {
            "@type": "Organization",
            "name": "DayByDay Consulting",
            "url": "https://www.daybydayconsulting.com",
            "logo": {
                "@type": "ImageObject",
                "url": "https://www.daybydayconsulting.com/favicon.ico",
            },
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": meta["canonical"],
        },
        "articleSection": meta["category"],
        "keywords": ", ".join([meta["title"].split(":")[0].strip()] + meta.get("keywords_secundarias", [])),
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def _jsonld_faq(faqs: list) -> str:
    if not faqs:
        return "{}"
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in faqs
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def _jsonld_breadcrumb(meta: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.daybydayconsulting.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.daybydayconsulting.com/blog.html"},
            {"@type": "ListItem", "position": 3, "name": meta["title"], "item": meta["canonical"]},
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def _jsonld_person() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Pablo Santirso",
        "url": "https://www.daybydayconsulting.com",
        "sameAs": [
            "https://es.linkedin.com/in/pablo-santirso-perez",
        ],
        "jobTitle": "Founder, DayByDay Consulting",
        "worksFor": {
            "@type": "Organization",
            "name": "DayByDay Consulting",
            "url": "https://www.daybydayconsulting.com",
        },
        "knowsAbout": [
            "Meta Ads", "Google Ads", "TikTok Ads", "LinkedIn Ads",
            "Conversions API", "Server-side tracking", "GA4",
            "Unit Economics", "D2C eCommerce", "Paid Media",
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def build(llm: dict, meta: dict, template_str: str, related_slugs: list, all_posts_by_slug: dict) -> str:
    accent = _accent(meta["category"])
    date_display = _date_display(meta["date"])
    canonical = f"https://www.daybydayconsulting.com/blog/{meta['slug']}.html"
    # Defensive scrub of any LLM-leaked prefixes
    meta = {**meta, "title": _scrub_title(meta.get("title", ""))}
    og_title = meta["title"]

    article_body = _build_article_body(llm)
    main_table = llm.get("table_main_html", "")
    ranking = llm.get("ranking_list_html", "")
    contrarian = llm.get("contrarian_block_html", "")
    related = _build_related(related_slugs, all_posts_by_slug)
    faqs_html = _build_faqs(llm.get("faqs", []))

    word_count = _word_count_estimate(article_body + (main_table or "") + (ranking or ""))
    reading_time = max(1, round(word_count / 220))

    jsonld_article = _jsonld_article({**meta, "canonical": canonical}, llm)
    jsonld_faq = _jsonld_faq(llm.get("faqs", []))
    jsonld_breadcrumb = _jsonld_breadcrumb({"title": meta["title"], "canonical": canonical})
    jsonld_person = _jsonld_person()

    html = template_str
    subs = {
        "lang": "es",
        "title": meta["title"],
        "og_title": og_title,
        "meta_description": meta["meta_description"],
        "date": meta["date"],
        "date_display": date_display,
        "canonical": canonical,
        "category": meta["category"],
        "reading_time": reading_time,
        "accent_color": accent,
        "abstract_html": llm.get("abstract_html", ""),
        "key_takeaways_html": llm.get("key_takeaways_html", ""),
        "article_body_html": article_body,
        "main_table_html": main_table,
        "ranking_list_html": ranking,
        "contrarian_block_html": contrarian,
        "related_posts_html": related,
        "faqs_html": faqs_html,
        "jsonld_article": jsonld_article,
        "jsonld_faq": jsonld_faq,
        "jsonld_breadcrumb": jsonld_breadcrumb,
        "jsonld_person": jsonld_person,
    }
    for k, v in subs.items():
        html = html.replace(f"${{{k}}}", str(v))

    # Sanity: any unreplaced ${} should be flagged
    leftover = re.findall(r"\$\{([a-z_]+)\}", html)
    if leftover:
        import sys
        print(f"WARN: unreplaced template vars: {leftover}", file=sys.stderr)

    return html
