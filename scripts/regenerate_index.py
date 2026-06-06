#!/usr/bin/env python3
"""
regenerate_index.py — rebuild derived artifacts from data/posts.json.

Outputs:
  - blog.html          (the post index, ES)
  - sitemap.xml        (deduped, with lastmod)
  - feed.xml           (RSS 2.0 with full content excerpts)
  - llms-full.txt      (first 200 words of each post, indexed by cluster, for AI ingestion)

Does NOT regenerate llms.txt (managed manually for stability) or en/ folder (out of scope).

Run from repo root.
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from html import escape, unescape

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
POSTS = DATA / "posts.json"
CLUSTERS = DATA / "clusters.json"

BLOG_HTML = REPO / "blog.html"
SITEMAP = REPO / "sitemap.xml"
FEED = REPO / "feed.xml"
LLMS_FULL = REPO / "llms-full.txt"
BLOG_DIR = REPO / "blog"
SITE = "https://www.daybydayconsulting.com"

# Per-cluster color
CLUSTER_COLORS = {
    "paid-media-foundations": "#6366f1",
    "attribution-tracking": "#10b981",
    "creative-testing": "#ec4899",
    "unit-economics": "#14b8a6",
    "agency-selection": "#ef4444",
}


def first_n_words(html: str, n: int = 200) -> str:
    """Strip HTML, take first n words, return plain text."""
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()
    return " ".join(words[:n])


def extract_post_excerpt(post: dict, n_words: int = 50) -> str:
    """Read the post HTML, get first paragraph of article body, truncated."""
    path = REPO / post["path"].lstrip("/")
    if not path.exists():
        return post.get("description", "")
    try:
        html = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return post.get("description", "")
    m = re.search(r'<p class="abstract"[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
    if not m:
        return post.get("description", "")
    return first_n_words(m.group(1), n_words)


def posts_by_category(posts: list) -> list[tuple[str, list]]:
    """Group posts by category, sorted within each group by date desc."""
    buckets = defaultdict(list)
    for p in posts:
        buckets[p.get("category", "Sin categoría")].append(p)
    out = []
    for cat in sorted(buckets.keys(), key=lambda c: (-len(buckets[c]), c)):
        out.append((cat, sorted(buckets[cat], key=lambda p: (p.get("date", ""), p["slug"]), reverse=True)))
    return out


# -----------------------------------------------------------------------------
# blog.html
# -----------------------------------------------------------------------------

BLOG_HTML_HEAD = """<!DOCTYPE html>
<html lang="es" data-theme="dark" data-mood="default">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog de Growth Marketing | DayByDay Consulting</title>
  <meta name="description" content="Artículos sobre paid media, automation y growth strategy para D2C en España. Escritos por founders, no por AI.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://www.daybydayconsulting.com/blog.html">
  <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="DayByDay Blog RSS">
  <link rel="icon" href="/favicon.ico">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/theme.css">
  <link rel="stylesheet" href="/css/sparkles.css">
  <link rel="stylesheet" href="/css/modern.css">
  <link rel="stylesheet" href="/css/pages.css">
  <style>
    :root {{ --accent-color: #6366f1; }}
    .blog-grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap:1.25rem; margin-bottom:3rem; }}
    .blog-card {{ display:block; background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:1.5rem; text-decoration:none; transition:all 0.2s ease; }}
    .blog-card:hover {{ border-color:var(--accent-color,#6366f1); transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,0.3); }}
    .blog-card-meta {{ display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem; flex-wrap:wrap; }}
    .blog-card-category {{ background:#6366f11a; border:1px solid #6366f140; color:#6366f1; font-size:0.65rem; font-weight:600; padding:0.2rem 0.5rem; border-radius:9999px; text-transform:uppercase; letter-spacing:0.05em; }}
    .blog-card-time, .blog-card-date {{ color:var(--text-muted); font-size:0.75rem; }}
    .blog-card-title {{ font-size:1rem; font-weight:700; color:var(--text-primary); margin-bottom:0.5rem; line-height:1.4; }}
    .blog-card-desc {{ font-size:0.85rem; color:var(--text-secondary); line-height:1.5; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }}
    .blog-category-section {{ margin-bottom:3rem; }}
    .blog-category-title {{ font-size:1.25rem; font-weight:700; color:var(--text-primary); margin-bottom:1.25rem; display:flex; align-items:center; gap:0.75rem; }}
    .blog-category-count {{ background:var(--bg-elevated); border:1px solid var(--border); color:var(--text-muted); font-size:0.75rem; font-weight:500; padding:0.15rem 0.6rem; border-radius:9999px; }}
    .hero-badge {{ background:#6366f11a; border:1px solid #6366f140; color:#6366f1; }}
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Saltar al contenido principal</a>
  <nav class="main-nav">
    <a href="/" class="nav-logo">DayByDay</a>
    <div class="nav-menu">
      <ul class="nav-links">
        <li class="nav-dropdown">
          <button class="nav-dropdown-btn">Lo que cubre</button>
          <div class="nav-dropdown-content mega">
            <div class="mega-grid" style="grid-template-columns:repeat(3,1fr);">
              <div class="mega-section">
                <div class="mega-section-title">Áreas</div>
                <a href="/lo-que-cubre.html#paid-media">Paid media</a>
                <a href="/lo-que-cubre.html#tracking">Tracking &amp; Analytics</a>
                <a href="/lo-que-cubre.html#automation">Automation</a>
                <a href="/lo-que-cubre.html#agentic-ai">Agentic AI</a>
                <a href="/lo-que-cubre.html#estrategia">Estrategia</a>
                <a href="/lo-que-cubre.html" class="highlight">Ver todo →</a>
              </div>
              <div class="mega-section">
                <div class="mega-section-title">Servicios</div>
                <a href="/meta-ads.html">Meta Ads</a>
                <a href="/google-ads.html">Google Ads</a>
                <a href="/tiktok-ads.html">TikTok Ads</a>
                <a href="/linkedin-ads.html">LinkedIn Ads</a>
                <a href="/automatizacion.html">Automatización</a>
                <a href="/analytics.html">Analytics</a>
                <a href="/agentic-ai.html">Agentic AI</a>
                <a href="/growth-strategy.html">Growth Strategy</a>
              </div>
              <div class="mega-section">
                <div class="mega-section-title">Stack</div>
                <a href="/tech/ga4.html">GA4</a>
                <a href="/tech/gtm.html">GTM</a>
                <a href="/tech/gsc.html">Search Console</a>
                <a href="/tech/capi.html">CAPI</a>
                <a href="/tech/n8n.html">n8n</a>
                <a href="/tech/azure.html">Azure</a>
                <a href="/tech/shopify.html">Shopify</a>
                <a href="/tech/dsp.html">DSP</a>
              </div>
            </div>
          </div>
        </li>
        <li><a href="/como-trabajamos.html">Cómo trabajamos</a></li>
        <li><a href="/resultados.html">Casos</a></li>
        <li><a href="/blog.html" aria-current="page">Blog</a></li>
        <li><a href="/contacto.html" class="nav-cta">Pedir auditoría</a></li>
      </ul>
    </div>
  </nav>

  <div style="height:64px;"></div>

  <main id="main" class="page-wrapper">
    <section style="padding:4rem 0 2rem;">
      <div class="container">
        <div style="max-width:760px;">
          <span class="hero-badge" style="display:inline-block;padding:0.3rem 0.75rem;border-radius:9999px;font-size:0.7rem;font-weight:600;letter-spacing:0.05em;margin-bottom:1rem;">BLOG · {total_posts} ARTÍCULOS</span>
          <h1 style="font-size:clamp(2.2rem,5vw,3.2rem);font-weight:800;line-height:1.1;letter-spacing:-0.02em;margin-bottom:1rem;">Paid media, attribution y growth para D2C España.</h1>
          <p style="font-size:1.15rem;color:var(--text-secondary);line-height:1.6;max-width:640px;">Lo que aprendemos auditando cuentas de eCommerce D2C en España, escrito por Pablo y Jorge, los socios que operan cada cuenta. Sin playbooks genéricos.</p>
        </div>
      </div>
    </section>

    <section style="padding:2rem 0 4rem;">
      <div class="container">
        <div class="section-header" style="margin-bottom:2.5rem;">
          <h2 style="font-size:1.5rem;font-weight:700;">Todos los artículos</h2>
          <p style="color:var(--text-secondary);font-size:0.95rem;margin-top:0.25rem;">{total_posts} artículos en {num_categories} categorías</p>
        </div>
"""

BLOG_HTML_FOOT = """
      </div>
    </section>
  </main>

  <footer class="footer">
    <a href="/">Inicio</a>
    <a href="/servicios.html">Servicios</a>
    <a href="/blog.html">Blog</a>
    <p>© 2026 DayByDay Consulting · partner de crecimiento para D2C España</p>
  </footer>
  <script src="/js/main.js"></script>
</body>
</html>
"""


def build_blog_html(posts: list) -> str:
    by_cat = posts_by_category(posts)
    total = len(posts)
    n_cat = len(by_cat)
    head = BLOG_HTML_HEAD.format(total_posts=total, num_categories=n_cat)
    body_parts = []
    for cat, cat_posts in by_cat:
        body_parts.append(
            f'<section class="blog-category-section">\n'
            f'  <h2 class="blog-category-title">{escape(cat)} <span class="blog-category-count">{len(cat_posts)}</span></h2>\n'
            f'  <div class="blog-grid">'
        )
        for p in cat_posts:
            body_parts.append(
                f'    <a href="{escape(p["path"])}" class="blog-card">\n'
                f'      <div class="blog-card-meta">\n'
                f'        <span class="blog-card-category">{escape(p.get("category", cat))}</span>\n'
                f'        <span class="blog-card-time">{p.get("reading_time_min", 0)} min</span>\n'
                f'        <span class="blog-card-date">{p.get("date", "")}</span>\n'
                f'      </div>\n'
                f'      <h3 class="blog-card-title">{escape(p["title"])}</h3>\n'
                f'      <p class="blog-card-desc">{escape(p.get("description", ""))}</p>\n'
                f'    </a>'
            )
        body_parts.append("  </div>\n</section>")
    return head + "\n".join(body_parts) + BLOG_HTML_FOOT


# -----------------------------------------------------------------------------
# sitemap.xml (deduped)
# -----------------------------------------------------------------------------

SITEMAP_HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""

SITEMAP_FOOT = "</urlset>\n"


def build_sitemap(posts: list) -> str:
    # Static pages
    static_pages = [
        ("/", "weekly", "1.0", "2026-06-06"),
        ("/problema.html", "monthly", "0.9", "2026-06-06"),
        ("/como-trabajamos.html", "monthly", "0.9", "2026-06-06"),
        ("/resultados.html", "monthly", "0.9", "2026-06-06"),
        ("/growth-partner.html", "monthly", "0.9", "2026-06-06"),
        ("/lo-que-cubre.html", "monthly", "0.9", "2026-06-06"),
        ("/servicios.html", "monthly", "0.6", "2026-06-06"),
        ("/contacto.html", "monthly", "0.9", "2026-06-06"),
        ("/blog.html", "weekly", "0.8", "2026-06-06"),
        ("/meta-ads.html", "monthly", "0.85", "2026-06-06"),
        ("/google-ads.html", "monthly", "0.85", "2026-06-06"),
        ("/tiktok-ads.html", "monthly", "0.8", "2026-06-06"),
        ("/linkedin-ads.html", "monthly", "0.8", "2026-06-06"),
        ("/automatizacion.html", "monthly", "0.85", "2026-06-06"),
        ("/analytics.html", "monthly", "0.85", "2026-06-06"),
        ("/agentic-ai.html", "monthly", "0.85", "2026-06-06"),
        ("/growth-strategy.html", "monthly", "0.85", "2026-06-06"),
        ("/llms.txt", "monthly", "0.3", "2026-06-06"),
        ("/humans.txt", "yearly", "0.2", "2026-06-06"),
        ("/feed.xml", "weekly", "0.4", "2026-06-06"),
    ]
    tech_pages = [
        "tech/meta-ads.html", "tech/google-ads-tech.html", "tech/tiktok-ads.html",
        "tech/linkedin-ads.html", "tech/shopify.html", "tech/ga4.html",
        "tech/gtm.html", "tech/gsc.html", "tech/n8n.html", "tech/capi.html",
        "tech/azure.html", "tech/dsp.html",
    ]
    for tp in tech_pages:
        static_pages.append((f"/{tp}", "monthly", "0.6", "2026-06-06"))

    # Dedup posts by slug (in case posts.json has dups)
    seen_slugs = set()
    deduped = []
    for p in sorted(posts, key=lambda p: (p.get("date", ""), p["slug"]), reverse=True):
        if p["slug"] in seen_slugs:
            continue
        seen_slugs.add(p["slug"])
        deduped.append(p)

    parts = [SITEMAP_HEAD]
    for path, freq, prio, lm in static_pages:
        parts.append(
            f'  <url><loc>{SITE}{path}</loc><changefreq>{freq}</changefreq>'
            f'<priority>{prio}</priority><lastmod>{lm}</lastmod></url>'
        )
    for p in deduped:
        lm = p.get("date") or p.get("file_mtime", "")[:10] or "2026-06-06"
        parts.append(
            f'  <url><loc>{SITE}/blog/{p["slug"]}.html</loc>'
            f'<changefreq>monthly</changefreq><priority>0.55</priority>'
            f'<lastmod>{lm}</lastmod></url>'
        )
    parts.append(SITEMAP_FOOT)
    return "\n".join(parts) + "\n"


# -----------------------------------------------------------------------------
# feed.xml — RSS 2.0
# -----------------------------------------------------------------------------

def build_feed(posts: list) -> str:
    deduped = sorted({p["slug"]: p for p in posts}.values(),
                     key=lambda p: (p.get("date", ""), p["slug"]), reverse=True)
    recent = deduped[:20]
    last_build = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    items = []
    for p in recent:
        excerpt = extract_post_excerpt(p, n_words=80)
        items.append(f"""    <item>
      <title>{escape(p['title'])}</title>
      <link>{SITE}/blog/{p['slug']}.html</link>
      <guid isPermaLink="true">{SITE}/blog/{p['slug']}.html</guid>
      <pubDate>{_rfc822(p.get('date', '2026-06-06'))}</pubDate>
      <category>{escape(p.get('category', ''))}</category>
      <description><![CDATA[{excerpt}…]]></description>
    </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>DayByDay Consulting · Blog</title>
    <link>{SITE}/blog.html</link>
    <description>Paid media, attribution y growth para eCommerce D2C en España. Por Pablo y Jorge, los socios que operan cada cuenta.</description>
    <language>es-ES</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml" />
{chr(10).join(items)}
  </channel>
</rss>
"""


def _rfc822(date_iso: str) -> str:
    try:
        d = datetime.strptime(date_iso, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return d.strftime("%a, %d %b %Y 00:00:00 +0000")
    except ValueError:
        return date_iso


# -----------------------------------------------------------------------------
# llms-full.txt — first 200 words of each post, indexed by cluster
# -----------------------------------------------------------------------------

def build_llms_full(posts: list) -> str:
    # Group by cluster
    by_cluster = defaultdict(list)
    for p in posts:
        by_cluster[p.get("cluster", "paid-media-foundations")].append(p)

    out = [
        "# DayByDay Consulting — Full Content for LLM Ingestion",
        "# > Cada artículo indexado por cluster. AI engines (Perplexity, ChatGPT, Claude) pueden usar este",
        "# > archivo para citar el contenido sin necesidad de fetch por URL.",
        "# > Generated: " + datetime.now(timezone.utc).isoformat(),
        "",
        "## Acerca de DayByDay",
        "",
        "DayByDay Consulting es partner de crecimiento para marcas D2C en España. Operado por el equipo",
        "fundador: Pablo Santirso (paid media, estrategia, operaciones) y Jorge González (CTO, automation,",
        "agentic AI). Vendemos un solo servicio — Growth Partner — con manifiestos en paid media, tracking,",
        "automation, agentic AI y estrategia. NO vendemos servicios técnicos por separado.",
        "",
        "Tagline maestro: 3,2M€ generados a marcas D2C (200K–3M€) en 12 meses · Growth Partner: analizamos,",
        "ejecutamos y acompañamos al fundador · Paid media + automation + agentic AI.",
        "",
    ]
    for cluster_id, cluster_posts in sorted(by_cluster.items()):
        cluster_posts_sorted = sorted(cluster_posts, key=lambda p: (p.get("date", ""), p["slug"]), reverse=True)
        title = cluster_id.replace("-", " ").title()
        out.append(f"## {title} ({len(cluster_posts_sorted)} artículos)")
        out.append("")
        for p in cluster_posts_sorted:
            out.append(f"### {p['title']}")
            out.append(f"URL: {SITE}/blog/{p['slug']}.html")
            out.append(f"Fecha: {p.get('date', '')} · Categoría: {p.get('category', '')} · {p.get('reading_time_min', 0)} min")
            excerpt = extract_post_excerpt(p, n_words=200)
            out.append("")
            out.append(excerpt)
            out.append("")
            out.append("---")
            out.append("")
    return "\n".join(out)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def update_llms_txt(posts: list) -> None:
    """Append a curated top-posts section to llms.txt, keeping the head untouched."""
    LLMS = REPO / "llms.txt"
    if not LLMS.exists():
        print("  [skip] llms.txt not found")
        return
    head = LLMS.read_text(encoding="utf-8").rstrip() + "\n\n"
    # Remove any prior [Articulos] section we appended
    head = re.split(r"\n## Art[íi]culos destacados.*?(?=\n## |\Z)", head, maxsplit=1, flags=re.DOTALL)[0].rstrip() + "\n"

    # Top 30 by date (most recent)
    recent = sorted({p["slug"]: p for p in posts}.values(),
                    key=lambda p: (p.get("date", ""), p["slug"]), reverse=True)[:30]
    sections = ["## Artículos destacados (top 30 más recientes)\n"]
    for p in recent:
        sections.append(
            f"- [{escape(p['title'])}]({SITE}/blog/{p['slug']}.html) — "
            f"{escape(p.get('category', ''))} · {p.get('date', '')}"
        )
    sections.append("")
    sections.append("Lista completa en [sitemap.xml](https://www.daybydayconsulting.com/sitemap.xml).")
    sections.append("RSS: [feed.xml](https://www.daybydayconsulting.com/feed.xml).")
    sections.append("Contenido íntegro para AI ingestion: [llms-full.txt](https://www.daybydayconsulting.com/llms-full.txt).")
    sections.append("")
    new = head + "\n".join(sections)
    LLMS.write_text(new, encoding="utf-8")
    print(f"  updated: llms.txt (+Artículos top 30)")


def main():
    if not POSTS.exists():
        print("ERROR: data/posts.json missing — run scripts/build_posts_index.py")
        sys.exit(1)
    data = json.loads(POSTS.read_text(encoding="utf-8"))
    posts = data["posts"]

    print(f"Regenerating indexes for {len(posts)} posts…")

    blog_html = build_blog_html(posts)
    BLOG_HTML.write_text(blog_html, encoding="utf-8")
    print(f"  wrote: blog.html ({len(blog_html):,} bytes)")

    sitemap = build_sitemap(posts)
    SITEMAP.write_text(sitemap, encoding="utf-8")
    print(f"  wrote: sitemap.xml ({len(sitemap):,} bytes)")

    feed = build_feed(posts)
    FEED.write_text(feed, encoding="utf-8")
    print(f"  wrote: feed.xml ({len(feed):,} bytes)")

    llms_full = build_llms_full(posts)
    LLMS_FULL.write_text(llms_full, encoding="utf-8")
    print(f"  wrote: llms-full.txt ({len(llms_full):,} bytes)")

    update_llms_txt(posts)


if __name__ == "__main__":
    main()
