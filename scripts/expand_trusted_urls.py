#!/usr/bin/env python3
"""
expand_trusted_urls.py — discover URLs from official sitemaps and add to trusted-urls.json.

Strategy:
  1. Recursively follow sitemap indexes (sitemapindex -> sitemap -> urls).
  2. Filter URLs by cluster-specific keyword lists.
  3. HEAD-verify each.
  4. Add to data/trusted-urls.json, deduped.

Sources (sitemaps we know are public + parseable):
  - shopify.dev (developer docs)
  - shopify.com (blog, marketing, help)
  - iabspain.es (industry research)
  - developers.facebook.com (Meta docs)

The script is conservative — only adds URLs that pass HEAD and contain a cluster keyword.
Run quarterly to refresh.
"""
import json
import re
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
TRUSTED = DATA / "trusted-urls.json"
UA = "Mozilla/5.0 (compatible; DayByDay-BlogBot/1.0; +https://daybydayconsulting.com)"

# (sitemap_root, max_depth, cluster, keyword_filter)
# keyword_filter: list of substrings; URL must contain at least one
SOURCES = [
    ("https://shopify.dev/sitemap.xml", 2, "attribution-tracking",
     ["pixel", "capi", "tracking", "analytics", "consent", "privacy", "customer-event", "web-pixel"]),
    ("https://shopify.dev/sitemap.xml", 2, "paid-media-foundations",
     ["marketing", "shop", "storefront", "sales-channel", "api/marketing"]),
    ("https://www.shopify.com/sitemap.xml", 1, "paid-media-foundations",
     ["paid", "ads", "marketing", "google", "meta", "facebook", "instagram", "tiktok", "ads"]),
    ("https://www.shopify.com/sitemap.xml", 1, "unit-economics",
     ["cac", "ltv", "lifetime", "customer-acquisition", "retention", "pricing", "cohort", "aov"]),
    ("https://www.shopify.com/sitemap.xml", 1, "creative-testing",
     ["creative", "ugc", "video", "creator", "content"]),
    ("https://iabspain.es/post-sitemap.xml", 1, "paid-media-foundations",
     ["publicidad", "marketing", "digital", "redes-sociales", "agencia", "comercio"]),
    ("https://iabspain.es/post-sitemap.xml", 1, "unit-economics",
     ["inversion", "estudio", "ecommerce", "negocio", "roi", "presupuesto"]),
    ("https://iabspain.es/post-sitemap.xml", 1, "attribution-tracking",
     ["medicion", "datos", "analytics", "tracking", "atribucion", "atribución"]),
    ("https://iabspain.es/post-sitemap.xml", 1, "agency-selection",
     ["agencia", "proveedor", "consultora", "sector"]),
]

MAX_URLS_PER_CLUSTER = 30
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    # Handle gzipped sitemaps
    if url.endswith(".gz") or r.headers.get("Content-Encoding") == "gzip":
        import gzip
        try:
            return gzip.decompress(data).decode("utf-8", errors="replace")
        except Exception:
            pass
    return data.decode("utf-8", errors="replace")


def head(url: str, timeout: int = 12) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200 <= r.status < 400
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            try:
                req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA, "Range": "bytes=0-2048"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return 200 <= r.status < 400
            except Exception:
                return False
        return False
    except Exception:
        return False


def parse_sitemap(xml_text: str) -> tuple[list[str], list[str]]:
    """Return (sub_sitemap_urls, urls)."""
    sub_sitemaps = []
    urls = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return [], []
    # Detect sitemapindex vs urlset. Walk recursively because <url> may be nested.
    def walk(el):
        for child in el:
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag == "sitemap":
                loc_el = child.find("sm:loc", NS)
                if loc_el is None:
                    loc_el = child.find("loc")
                if loc_el is not None and loc_el.text:
                    sub_sitemaps.append(loc_el.text.strip())
            elif tag == "url":
                loc_el = child.find("sm:loc", NS)
                if loc_el is None:
                    loc_el = child.find("loc")
                if loc_el is not None and loc_el.text:
                    urls.append(loc_el.text.strip())
    walk(root)
    return sub_sitemaps, urls


def collect_urls(sitemap_url: str, depth: int) -> list[str]:
    """Recursively collect all leaf URLs from a sitemap root."""
    out = []
    try:
        xml = fetch(sitemap_url, timeout=12)
    except Exception as e:
        print(f"    [sitemap] fetch fail {sitemap_url}: {e}")
        return []
    subs, urls = parse_sitemap(xml)
    out.extend(urls)
    if depth > 0:
        for sub in subs:
            time.sleep(0.3)
            out.extend(collect_urls(sub, depth - 1))
    return out


def cluster_match(url: str, keywords: list[str]) -> bool:
    path = url.lower()
    return any(k in path for k in keywords)


def main():
    if not TRUSTED.exists():
        print("ERROR: data/trusted-urls.json missing — run scripts/build_trusted_urls.py first.")
        return 1
    trusted = json.loads(TRUSTED.read_text(encoding="utf-8"))
    existing_urls = {entry["url"] for cluster_data in trusted.get("by_cluster", {}).values() for entry in cluster_data}

    # Build cluster -> (source, depth, keywords) index
    by_cluster = trusted.get("by_cluster", {})
    for cid in by_cluster:
        by_cluster[cid] = [e for e in by_cluster[cid] if e.get("url")]

    # Apply cap on existing
    def cap(cluster, items):
        if len(items) >= MAX_URLS_PER_CLUSTER:
            return items[:MAX_URLS_PER_CLUSTER]
        return items

    for cid in by_cluster:
        by_cluster[cid] = cap(cid, by_cluster[cid])

    new_by_cluster: dict[str, list] = defaultdict(list)
    for sitemap_url, depth, cluster, keywords in SOURCES:
        cap_now = len(by_cluster.get(cluster, []))
        if cap_now >= MAX_URLS_PER_CLUSTER:
            print(f"[skip] {cluster} already at cap ({cap_now})")
            continue
        print(f"==> {cluster:25s} <- {sitemap_url}")
        try:
            all_urls = collect_urls(sitemap_url, depth)
        except Exception as e:
            print(f"    [skip] {e}")
            continue
        print(f"    collected {len(all_urls)} URLs from sitemap")
        # Filter by cluster keywords
        candidates = [u for u in all_urls if cluster_match(u, keywords)]
        # De-dup
        candidates = list(dict.fromkeys(candidates))
        print(f"    after filter: {len(candidates)} candidates for {cluster}")
        # Verify
        added = 0
        for u in candidates:
            if u in existing_urls:
                continue
            if not head(u):
                continue
            new_by_cluster[cluster].append({
                "url": u,
                "topic_tags": keywords,
                "why": f"Auto-discovered from {sitemap_url}",
                "status": 200,
                "verified_at": datetime.now(timezone.utc).isoformat(),
            })
            existing_urls.add(u)
            added += 1
            if len(by_cluster.get(cluster, [])) + added >= MAX_URLS_PER_CLUSTER:
                break
            time.sleep(0.2)
        print(f"    added {added} new URLs to {cluster}")

    # Merge
    for cid, items in new_by_cluster.items():
        by_cluster.setdefault(cid, []).extend(items)
        by_cluster[cid] = by_cluster[cid][:MAX_URLS_PER_CLUSTER]

    trusted["by_cluster"] = by_cluster
    trusted["last_updated"] = datetime.now(timezone.utc).isoformat()
    total = sum(len(v) for v in by_cluster.values())
    trusted["total_urls"] = total
    TRUSTED.write_text(json.dumps(trusted, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== FINAL ===")
    for c, items in sorted(by_cluster.items()):
        print(f"  {c:25s} {len(items):3d} URLs")
    print(f"  Total: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
