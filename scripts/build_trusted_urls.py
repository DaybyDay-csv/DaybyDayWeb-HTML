#!/usr/bin/env python3
"""
build_trusted_urls.py — verify and produce data/trusted-urls.json.

The seed list below is hand-curated. We then:
  1. HEAD-verify each URL.
  2. Group by cluster.
  3. Persist with last-verified timestamp.
  4. Optionally try to expand via sitemaps (currently disabled — too noisy).

The LLM in step_research/03_write reads this JSON to pick URLs.
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from lib.authority_link_checker import _is_trusted, _head  # reuse internals

DATA = REPO / "data"
OUT = DATA / "trusted-urls.json"
UA = "DayByDay-BlogBot/1.0 (+https://daybydayconsulting.com) trusted-urls audit"

# -----------------------------------------------------------------------------
# Hand-curated seed
# Each entry: (url, cluster, topic_tags, why)
# topic_tags are short keywords the LLM can match against the topic to pick.
# -----------------------------------------------------------------------------

SEED = [
    # === Meta Help Center (docs.business.facebook.com / www.facebook.com/business/help) ===
    ("https://www.facebook.com/business/help/421906290152553", "attribution-tracking", ["capi", "conversions api", "meta", "tracking"], "Meta CAPI overview"),
    ("https://www.facebook.com/business/help/169316596175124", "attribution-tracking", ["emq", "event match quality", "meta"], "Meta EMQ explanation"),
    ("https://www.facebook.com/business/help/1488409651585626", "attribution-tracking", ["pixel", "capi", "deduplication", "meta"], "Pixel + CAPI deduplication"),
    ("https://www.facebook.com/business/help/1426236512972090", "attribution-tracking", ["ga4", "meta", "events manager"], "Connect GA4 to Meta"),
    ("https://business.facebook.com/business/help/169316596175124", "attribution-tracking", ["emq", "meta"], "EMQ docs"),

    # === Meta for Developers (developers.facebook.com) ===
    ("https://developers.facebook.com/docs/marketing-api/conversions-api", "attribution-tracking", ["capi", "developers", "meta"], "CAPI developer reference"),
    ("https://developers.facebook.com/docs/marketing-api/conversions-api/parameters", "attribution-tracking", ["capi", "parameters", "meta"], "CAPI parameter reference"),
    ("https://developers.facebook.com/docs/marketing-api/conversions-api/deduplication", "attribution-tracking", ["capi", "deduplication", "event_id"], "CAPI deduplication guide"),

    # === Meta Ads (campaign management) ===
    ("https://www.facebook.com/business/help/430291176997024", "paid-media-foundations", ["cbo", "campaign budget optimization", "meta"], "CBO explanation"),
    ("https://www.facebook.com/business/help/3971033805044420", "paid-media-foundations", ["advantage+", "shopping", "meta"], "Advantage+ Shopping Campaign"),
    ("https://www.facebook.com/business/help/263980900807067", "paid-media-foundations", ["lookalike", "audiences", "meta"], "Lookalike audiences"),
    ("https://www.facebook.com/business/help/1670944254683867", "paid-media-foundations", ["broad", "targeting", "audiences", "meta"], "Broad targeting"),
    ("https://www.facebook.com/business/help/289260651495255", "paid-media-foundations", ["ab testing", "experiments", "meta"], "A/B test experiments"),
    ("https://www.facebook.com/business/help/430291176997024", "paid-media-foundations", ["budget", "cbo", "meta"], "Campaign budget"),
    ("https://www.facebook.com/business/help/466024386882094", "paid-media-foundations", ["roas", "return on ad spend", "meta"], "ROAS in Meta Ads Manager"),
    ("https://www.facebook.com/business/help/431829847254471", "paid-media-foundations", ["retargeting", "custom audiences", "meta"], "Retargeting with custom audiences"),
    ("https://www.facebook.com/business/help/341746126413053", "paid-media-foundations", ["creative", "ad formats", "meta"], "Ad creative formats"),
    ("https://www.facebook.com/business/help/2221112508194999", "paid-media-foundations", ["instagram", "feed", "placements", "meta"], "Instagram placements"),

    # === Google Ads Help ===
    ("https://support.google.com/google-ads/answer/6167101", "paid-media-foundations", ["google ads", "overview", "campaign"], "About Google Ads"),
    ("https://support.google.com/google-ads/answer/14090408", "paid-media-foundations", ["performance max", "pmax", "google"], "Performance Max guide"),
    ("https://support.google.com/google-ads/answer/6357362", "paid-media-foundations", ["bidding", "smart bidding", "google"], "Smart bidding strategies"),
    ("https://support.google.com/google-ads/answer/14090391", "paid-media-foundations", ["assets", "ad assets", "google"], "Ad assets"),
    ("https://support.google.com/google-ads/answer/6167094", "paid-media-foundations", ["conversion tracking", "google", "tracking"], "Conversion tracking"),
    ("https://support.google.com/google-ads/answer/9175566", "paid-media-foundations", ["audiences", "remarketing", "google"], "Audience manager"),

    # === GA4 ===
    ("https://support.google.com/analytics/answer/10089681", "attribution-tracking", ["ga4", "events", "analytics"], "GA4 events"),
    ("https://support.google.com/analytics/answer/12195621", "attribution-tracking", ["ga4", "conversions", "analytics"], "GA4 conversions"),
    ("https://support.google.com/analytics/answer/9539598", "attribution-tracking", ["ga4", "server-side", "tagging"], "Server-side tagging"),
    ("https://developers.google.com/analytics/devguides/collection/ga4", "attribution-tracking", ["ga4", "developers", "api"], "GA4 Measurement Protocol"),

    # === GTM ===
    ("https://support.google.com/tagmanager/answer/3441262", "attribution-tracking", ["gtm", "tag manager", "tags"], "GTM tags overview"),
    ("https://support.google.com/tagmanager/answer/9205819", "attribution-tracking", ["gtm", "ga4", "configuration"], "GA4 configuration tag"),
    ("https://developers.google.com/tag-platform/tag-manager/server-side", "attribution-tracking", ["gtm", "server-side", "sst"], "Server-side GTM"),

    # === Shopify ===
    ("https://help.shopify.com/en/manual/online-sales-channels/facebook", "attribution-tracking", ["shopify", "facebook", "channel"], "Shopify Facebook channel"),
    ("https://help.shopify.com/en/manual/privacy-and-security", "attribution-tracking", ["shopify", "privacy", "gdpr"], "Shopify privacy & GDPR"),
    ("https://shopify.dev/docs/apps/marketing/pixels", "attribution-tracking", ["shopify", "pixels", "customer events"], "Shopify customer events/pixels"),
    ("https://shopify.dev/docs/api/marketing", "paid-media-foundations", ["shopify", "marketing", "api"], "Shopify Marketing API"),
    ("https://help.shopify.com/en/manual/online-sales-channels", "paid-media-foundations", ["shopify", "sales channels", "overview"], "Shopify sales channels overview"),

    # === LinkedIn ===
    ("https://www.linkedin.com/help/lms/answer/a424238", "paid-media-foundations", ["linkedin", "ads", "campaign manager"], "LinkedIn Campaign Manager"),
    ("https://business.linkedin.com/advertise", "paid-media-foundations", ["linkedin", "ads", "advertise"], "LinkedIn Ads product page"),

    # === TikTok ===
    ("https://ads.tiktok.com/help/article/get-started", "paid-media-foundations", ["tiktok", "ads", "get started"], "TikTok Ads get started"),
    ("https://ads.tiktok.com/help/article/smart-performance-campaign", "paid-media-foundations", ["tiktok", "smart performance", "campaign"], "TikTok Smart Performance"),
    ("https://ads.tiktok.com/help/article/tiktok-shop", "paid-media-foundations", ["tiktok shop", "ecommerce", "d2c"], "TikTok Shop"),

    # === IAB Spain ===
    ("https://iabspain.es/", "paid-media-foundations", ["iab", "spain", "marketing digital"], "IAB Spain home"),
    ("https://iabspain.es/estudios-de-inversion-publicitaria/", "unit-economics", ["iab", "inversión", "publicidad", "spain"], "IAB Spain inversión publicitaria"),
    ("https://iabspain.es/topics/publicidad-digital/", "paid-media-foundations", ["iab", "publicidad digital", "spain"], "IAB Spain publicidad digital"),
    ("https://iabspain.es/topics/comercio-electronico/", "unit-economics", ["iab", "ecommerce", "spain"], "IAB Spain ecommerce"),

    # === Spanish data protection / legal ===
    ("https://www.aepd.es/es", "attribution-tracking", ["aepd", "gdpr", "privacidad", "spain"], "AEPD — Spanish data protection"),
    ("https://www.aeat.es/wps/internet/es_es/", "agency-selection", ["aeat", "fiscal", "tributos", "spain"], "AEAT — fiscal"),

    # === HBR (general business/marketing) ===
    ("https://hbr.org/topic/subject/marketing", "unit-economics", ["hbr", "marketing", "general"], "HBR marketing topic"),
    ("https://hbr.org/2007/10/how-to-sell-more-by-pricing-less", "unit-economics", ["hbr", "pricing", "elasticity"], "HBR pricing"),
    ("https://hbr.org/2014/09/a-refresher-on-marketing-mix-modeling", "unit-economics", ["hbr", "mmm", "marketing mix modeling"], "HBR MMM"),

    # === Creative / UGC / formats ===
    ("https://business.instagram.com/creators", "creative-testing", ["instagram", "creators", "ugc", "partnership ads"], "Instagram creators / partnership ads"),
    ("https://www.facebook.com/business/creative", "creative-testing", ["meta", "creative", "best practices"], "Meta Creative Shop"),
    ("https://www.thinkwithgoogle.com/intl/en-145/creative-asset-collection/", "creative-testing", ["google", "creative", "ads"], "Google creative examples"),

    # === Spanish blogs (industry voices) ===
    ("https://marketing4ecommerce.net/", "paid-media-foundations", ["marketing4ecommerce", "blog es", "d2c"], "Marketing4ecommerce"),
    ("https://www.brainsins.com/", "paid-media-foundations", ["brainsins", "blog es", "ecommerce"], "Brainsins"),
    ("https://www.iabspain.es/estudio-el-comercio-electronico-en-espana/", "unit-economics", ["iab", "ecommerce españa", "estudio"], "IAB Spain ecommerce study"),

    # === Unit economics & cohort ===
    ("https://www.shopify.com/blog/customer-acquisition-cost", "unit-economics", ["shopify", "cac", "customer acquisition cost"], "Shopify blog — CAC"),
    ("https://www.shopify.com/blog/lifetime-value", "unit-economics", ["shopify", "ltv", "lifetime value"], "Shopify blog — LTV"),

    # === OpenAI / AI for marketers ===
    ("https://platform.openai.com/docs/guides/embeddings", "creative-testing", ["openai", "ai", "embeddings"], "OpenAI embeddings guide"),
]


def verify(url: str, retries: int = 2) -> dict:
    """HEAD-verify with fallback. Returns {ok, status, final_url}."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=12) as r:
                return {"ok": 200 <= r.status < 400, "status": r.status, "final_url": r.url}
        except urllib.error.HTTPError as e:
            # Try GET range on 403/405/501
            if e.code in (403, 405, 501) and attempt == 0:
                try:
                    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA, "Range": "bytes=0-2048"})
                    with urllib.request.urlopen(req, timeout=12) as r:
                        return {"ok": 200 <= r.status < 400, "status": r.status, "final_url": r.url}
                except Exception:
                    pass
            return {"ok": False, "status": e.code, "final_url": url}
        except Exception:
            time.sleep(1)
    return {"ok": False, "status": 0, "final_url": url}


def main():
    if not SEED:
        print("ERROR: SEED list is empty — fill it before running.")
        return 1

    # De-dup by URL (keep first occurrence)
    seen = set()
    uniq = []
    for url, cluster, tags, why in SEED:
        if url in seen:
            continue
        seen.add(url)
        uniq.append((url, cluster, tags, why))

    print(f"Verifying {len(uniq)} URLs…")
    by_cluster: dict[str, list] = {}
    ok_count = 0
    fail_count = 0
    fail_urls: list[tuple[str, int, str]] = []
    for url, cluster, tags, why in uniq:
        r = verify(url)
        if r["ok"]:
            ok_count += 1
            entry = {
                "url": url,
                "topic_tags": tags,
                "why": why,
                "status": r["status"],
                "verified_at": datetime.now(timezone.utc).isoformat(),
            }
            by_cluster.setdefault(cluster, []).append(entry)
            print(f"  ✓ [{r['status']}] {cluster:25s} {url[:70]}")
        else:
            fail_count += 1
            fail_urls.append((url, r["status"], cluster))
            print(f"  ✗ [{r['status']}] {cluster:25s} {url[:70]}")
        time.sleep(0.2)  # be nice

    out = {
        "schema_version": "1.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_urls": ok_count,
        "total_failed": fail_count,
        "by_cluster": by_cluster,
        "failed_urls": [{"url": u, "status": s, "cluster": c} for u, s, c in fail_urls],
        "notes": "Re-run quarterly. Update after a URL is consistently 404. Add new URLs by editing the SEED list in scripts/build_trusted_urls.py.",
    }
    DATA.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print(f"Verified OK: {ok_count} / {len(uniq)}  ({fail_count} failed)")
    print(f"By cluster:")
    for c, items in sorted(by_cluster.items()):
        print(f"  {c:25s} {len(items)} URLs")
    print(f"\nWrote {OUT.relative_to(REPO)}")
    if fail_urls:
        print(f"\nFailed URLs (update SEED or remove):")
        for u, s, c in fail_urls:
            print(f"  [{s}] {c:20s} {u}")

    return 0 if fail_count == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
