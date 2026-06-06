#!/usr/bin/env python3
"""
authority_link_checker.py — HEAD-verify external URLs with Wayback fallback.

Returns a list of (url, ok, status, final_url) tuples.
Cache: data/link_check_cache.json (24h TTL).
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone, timedelta

REPO = Path(__file__).resolve().parent.parent.parent
DATA = REPO / "data"
CACHE = DATA / "link_check_cache.json"

# Trusted domain allowlist (DR >= 70 or first-party docs for tools)
TRUSTED_DOMAINS = {
    # Meta / Facebook
    "facebook.com", "business.facebook.com", "developers.facebook.com",
    "meta.com", "about.meta.com",
    # Google
    "google.com", "support.google.com", "developers.google.com",
    "ads.google.com", "analytics.google.com",
    # Microsoft
    "microsoft.com", "learn.microsoft.com", "azure.microsoft.com",
    # Apple developer (iOS attribution)
    "developer.apple.com",
    # Spanish official
    "iabspain.es", "aeat.es", "aepd.es", "economia.gob.es", "boe.es",
    "aeec.es", "red.es", "incibe.es", "osimga.gal",
    # Ecommerce / dev
    "shopify.dev", "shopify.com", "help.shopify.com",
    # No-code / automation
    "n8n.io", "docs.n8n.io", "zapier.com", "make.com",
    # Authority content
    "hbr.org", "mckinsey.com", "nielsen.com", "statista.com",
    "searchengineland.com", "moz.com", "semrush.com", "ahrefs.com",
    "backlinko.com", "ahrefs.com",
    # News / business (ES)
    "eleconomista.es", "cincodias.elpais.es", "expansion.com",
    "emprendedores.es", "marketing4ecommerce.net", "brainsins.com",
    # Other
    "wikipedia.org", "schema.org", "w3.org",
    "openai.com", "anthropic.com", "perplexity.ai", "claude.com",
}


def _load_cache() -> dict:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_cache(c: dict):
    DATA.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")


def _is_trusted(url: str) -> bool:
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
    except Exception:
        return False
    if host.startswith("www."):
        host = host[4:]
    return host in TRUSTED_DOMAINS or any(host.endswith("." + d) for d in TRUSTED_DOMAINS)


def _head(url: str, timeout: int = 12) -> tuple[bool, int, str]:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={
            "User-Agent": "DayByDay-BlogBot/1.0 (+https://daybydayconsulting.com)"
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return (200 <= r.status < 400, r.status, r.url)
    except urllib.error.HTTPError as e:
        # Some servers reject HEAD — try GET range
        if e.code in (403, 405, 501):
            try:
                req2 = urllib.request.Request(url, method="GET", headers={
                    "User-Agent": "DayByDay-BlogBot/1.0",
                    "Range": "bytes=0-2048",
                })
                with urllib.request.urlopen(req2, timeout=timeout) as r2:
                    return (200 <= r2.status < 400, r2.status, r2.url)
            except Exception as e2:
                return (False, getattr(e2, "code", 0) or 0, url)
        return (False, e.code, url)
    except Exception:
        return (False, 0, url)


def _wayback(url: str) -> str | None:
    """Return a stable wayback URL if available, else None."""
    try:
        api = f"https://archive.org/wayback/available?url={urllib.parse.quote(url, safe='')}"
        with urllib.request.urlopen(api, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        snap = data.get("archived_snapshots", {}).get("closest", {})
        if snap and snap.get("available") and snap.get("url"):
            return snap["url"]
    except Exception:
        pass
    return None


def check(url: str, use_cache: bool = True, ttl_hours: int = 24) -> dict:
    """Check one URL. Returns {ok, status, final_url, wayback, trusted, checked_at}."""
    cache = _load_cache() if use_cache else {}
    now = datetime.now(timezone.utc)
    cached = cache.get(url)
    if cached and use_cache:
        try:
            ts = datetime.fromisoformat(cached["checked_at"])
            if now - ts < timedelta(hours=ttl_hours):
                return cached
        except (KeyError, ValueError):
            pass

    trusted = _is_trusted(url)
    ok, status, final = _head(url)
    wayback = None if ok else _wayback(url)
    result = {
        "ok": ok,
        "status": status,
        "final_url": final,
        "wayback": wayback,
        "trusted": trusted,
        "checked_at": now.isoformat(),
    }
    if use_cache:
        cache[url] = result
        _save_cache(cache)
    return result


def filter_survivors(urls: list[dict], min_ok: int = 2) -> list[dict]:
    """Given a list of {url, anchor, why}, return those that pass head-check.
    If too many fail, the function still returns at least min_ok that pass.
    """
    results = []
    for entry in urls:
        url = entry["url"]
        r = check(url)
        entry = {**entry, **r}
        results.append(entry)
    # Sort: ok=True first, then by trusted, then wayback fallback
    results.sort(key=lambda e: (not e["ok"], not e.get("trusted", False), not e.get("wayback")))
    ok_results = [e for e in results if e["ok"]]
    if len(ok_results) >= min_ok:
        return ok_results
    # Add wayback-fallback for the rest
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+", help="URLs to check")
    args = ap.parse_args()
    for u in args.urls:
        r = check(u)
        print(f"{'OK ' if r['ok'] else 'FAIL'} [{r['status']}] {u}  trusted={r['trusted']}  wayback={r.get('wayback') or '-'}")
