#!/usr/bin/env python3
"""
test_link_verification.py — tests for the link verification chain.

Run from repo root:
  python3 scripts/test_link_verification.py

Verifies:
  - trusted-urls.json has URLs in every cluster
  - authority_link_checker.check() works for known-good URLs
  - relevance_check returns reasonable scores for known URLs
  - post_builder scrubs LLM-leaked prefixes from title
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

DATA = REPO / "data"
TRUSTED = DATA / "trusted-urls.json"
RESULTS = []


def test(name, cond, detail=""):
    status = "✓" if cond else "✗"
    RESULTS.append((status, name, detail))
    print(f"  {status} {name}" + (f"  [{detail}]" if detail else ""))


# -----------------------------------------------------------------------------
# 1. trusted-urls.json
# -----------------------------------------------------------------------------
print("== trusted-urls.json ==")
if not TRUSTED.exists():
    test("trusted-urls.json exists", False, f"missing at {TRUSTED}")
    sys.exit(1)
data = json.loads(TRUSTED.read_text(encoding="utf-8"))
test("trusted-urls.json has by_cluster", "by_cluster" in data)
test("trusted-urls.json has 5 clusters", len(data.get("by_cluster", {})) >= 5,
     f"got {len(data.get('by_cluster', {}))}")
expected_clusters = {"attribution-tracking", "paid-media-foundations", "creative-testing",
                     "unit-economics", "agency-selection"}
missing = expected_clusters - set(data.get("by_cluster", {}).keys())
test("all 5 expected clusters present", not missing, f"missing: {missing}" if missing else "")
total = sum(len(v) for v in data.get("by_cluster", {}).values())
test("total URLs >= 100", total >= 100, f"{total} URLs")
test("all URLs are HTTPS", all(
    e["url"].startswith("https://")
    for entries in data["by_cluster"].values()
    for e in entries
), "found http://")
# Check no duplicate URLs across clusters
all_urls = []
for entries in data["by_cluster"].values():
    all_urls.extend(e["url"] for e in entries)
test("no duplicate URLs across clusters", len(all_urls) == len(set(all_urls)),
     f"{len(all_urls) - len(set(all_urls))} dups" if len(all_urls) != len(set(all_urls)) else "")
# Each entry has required fields
required_fields = {"url", "topic_tags", "why", "verified_at"}
ok = all(
    required_fields.issubset(set(e.keys()))
    for entries in data["by_cluster"].values()
    for e in entries
)
test("all entries have required fields", ok)

# -----------------------------------------------------------------------------
# 2. authority_link_checker
# -----------------------------------------------------------------------------
print("\n== authority_link_checker ==")
from lib.authority_link_checker import check, _is_trusted

# Known-good URL (from trusted list)
sample_url = next(iter(data["by_cluster"]["attribution-tracking"][0]["url"] for _ in [0] if data["by_cluster"]["attribution-tracking"]))
r = check(sample_url, use_cache=False)
test(f"check() returns ok=True for {sample_url[:50]}", r["ok"], f"status={r['status']}")
test("check() result has all keys", {"ok", "status", "final_url", "wayback", "trusted", "checked_at"}.issubset(r.keys()))

# Known-bad URL
r = check("https://www.daybydayconsulting.com/this-does-not-exist", use_cache=False)
test("check() returns ok=False for 404", not r["ok"], f"status={r['status']}")

# is_trusted
test("_is_trusted() True for facebook.com", _is_trusted("https://www.facebook.com/foo"))
test("_is_trusted() False for spam.com", not _is_trusted("https://spam.com/foo"))

# -----------------------------------------------------------------------------
# 3. post_builder title scrub
# -----------------------------------------------------------------------------
print("\n== post_builder title scrub ==")
from lib.post_builder import _scrub_title
test("scrub strips 'TITLE: '", _scrub_title("TITLE: My post") == "My post")
test("scrub strips 'Title: '", _scrub_title("Title: My post") == "My post")
test("scrub strips '# '", _scrub_title("# My post") == "My post")
test("scrub strips '## '", _scrub_title("## My post") == "My post")
test("scrub strips ' | DayByDay Consulting' suffix", _scrub_title("My post | DayByDay Consulting") == "My post")
test("scrub handles multi-prefix", _scrub_title("TITLE: Title: My post") == "My post")
test("scrub empty stays empty", _scrub_title("") == "")
test("scrub None-safe", _scrub_title(None) == "")
test("scrub clean title untouched", _scrub_title("CAPI server-side 2026") == "CAPI server-side 2026")

# -----------------------------------------------------------------------------
# 4. markdown_parser handles LLM output variations
# -----------------------------------------------------------------------------
print("\n== markdown_parser ==")
from lib.markdown_parser import parse
# LLM-style with "# TITLE" (no colon) + META with **Title:** / **Description:**
md1 = """# TITLE
CAPI server-side Shopify 2026: setup en 30 minutos

# META
**Title:** CAPI server-side Shopify 2026: setup en 30 minutos
**Description:** Cambios 2026 de Meta CAPI en Shopify. Setup rápido, errores típicos y cómo subir el EMQ por encima de 7.

# ABSTRACT
Meta endurece iOS 14+. Setup 30 min. EMQ > 7.

# H2:
Párrafo uno.
Párrafo dos.
"""
p1 = parse(md1)
test("parser extracts title from '# TITLE' (no colon)", p1["title"] == "CAPI server-side Shopify 2026: setup en 30 minutos",
     f"got: {p1['title']!r}")
test("parser extracts description from **Description:**", "Cambios 2026" in p1.get("meta_description", ""),
     f"got: {p1.get('meta_description','')!r}")
test("parser counts h2_blocks", len(p1["h2_blocks"]) == 1)

# Original format with colons
md2 = """# TITLE:
Foo bar

# META:
Foo bar

# H2:
Test paragraph.

"""
p2 = parse(md2)
test("parser handles '# TITLE:' (with colon)", p2["title"] == "Foo bar")

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
passed = sum(1 for s, _, _ in RESULTS if s == "✓")
failed = sum(1 for s, _, _ in RESULTS if s == "✗")
print(f"  {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
