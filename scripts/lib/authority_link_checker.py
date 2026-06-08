#!/usr/bin/env python3
"""
authority_link_checker.py — HEAD-verify + LLM relevance-check external URLs.

3-stage pipeline:
  1. HEAD check (with GET range fallback for 403/405/501)
  2. Wayback Machine fallback if HEAD fails
  3. LLM relevance check: fetch first 2KB of HTML, ask LLM "is this about [topic]?"

Cache: data/link_check_cache.json (24h TTL for HEAD, 7d for relevance).
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
from datetime import datetime, timezone, timedelta
from html import unescape

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))
DATA = REPO / "data"
CACHE = DATA / "link_check_cache.json"

TRUSTED_DOMAINS = {
    "facebook.com", "business.facebook.com", "developers.facebook.com",
    "meta.com", "about.meta.com",
    "google.com", "support.google.com", "developers.google.com",
    "ads.google.com", "analytics.google.com",
    "microsoft.com", "learn.microsoft.com", "azure.microsoft.com",
    "developer.apple.com",
    "iabspain.es", "aeat.es", "aepd.es", "economia.gob.es", "boe.es",
    "aeec.es", "red.es", "incibe.es", "osimga.gal",
    "shopify.dev", "shopify.com", "help.shopify.com",
    "n8n.io", "docs.n8n.io", "zapier.com", "make.com",
    "hbr.org", "mckinsey.com", "nielsen.com", "statista.com",
    "searchengineland.com", "moz.com", "semrush.com", "ahrefs.com",
    "backlinko.com",
    "eleconomista.es", "cincodias.elpais.es", "expansion.com",
    "emprendedores.es", "marketing4ecommerce.net", "brainsins.com",
    "wikipedia.org", "schema.org", "w3.org",
    "openai.com", "anthropic.com", "perplexity.ai", "claude.com",
    "linkedin.com", "business.linkedin.com", "ads.linkedin.com",
    "tiktok.com", "ads.tiktok.com",
    "thinkwithgoogle.com", "youtube.com",
    "thinkapps.com",
    "kaggle.com", "github.com",
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
            "User-Agent": "Mozilla/5.0 (compatible; DayByDay-BlogBot/1.0; +https://daybydayconsulting.com)"
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return (200 <= r.status < 400, r.status, r.url)
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            try:
                req2 = urllib.request.Request(url, method="GET", headers={
                    "User-Agent": "Mozilla/5.0 (compatible; DayByDay-BlogBot/1.0)",
                    "Range": "bytes=0-2048",
                })
                with urllib.request.urlopen(req2, timeout=timeout) as r2:
                    return (200 <= r2.status < 400, r2.status, r2.url)
            except Exception:
                return (False, 0, url)
        return (False, e.code, url)
    except Exception:
        return (False, 0, url)


def _wayback(url: str) -> str | None:
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


def _fetch_text(url: str, max_bytes: int = 6000, timeout: int = 10) -> str:
    """Fetch first N bytes of a URL and return plain text (no HTML, no scripts)."""
    try:
        req = urllib.request.Request(url, method="GET", headers={
            "User-Agent": "Mozilla/5.0 (compatible; DayByDay-BlogBot/1.0)",
            "Range": f"bytes=0-{max_bytes}",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", errors="replace")
    except Exception:
        return ""
    # Strip script/style blocks
    raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = unescape(raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw[:2500]


def relevance_check(url: str, topic: str, client=None) -> dict:
    """Ask the LLM: is this page actually about the topic?

    Returns {relevance: 0-10, reason: str, checked_at: iso}.
    Cached 7 days. Skipped if no client passed.
    """
    if client is None:
        try:
            from lib.llm_client import LLMClient
            client = LLMClient()
        except Exception:
            return {"relevance": 5, "reason": "no_client", "checked_at": datetime.now(timezone.utc).isoformat()}

    cache = _load_cache()
    now = datetime.now(timezone.utc)
    cached = cache.get(url, {}).get("relevance_check")
    if cached:
        try:
            ts = datetime.fromisoformat(cached["checked_at"])
            if now - ts < timedelta(days=7):
                return cached
        except (KeyError, ValueError):
            pass

    snippet = _fetch_text(url)
    if not snippet:
        result = {"relevance": 0, "reason": "fetch_failed", "checked_at": now.isoformat()}
        cache.setdefault(url, {})["relevance_check"] = result
        _save_cache(cache)
        return result

    prompt = (
        "Eres un auditor SEO estricto. Recibirás un tema de artículo y el contenido "
        "extraído (snippet) de una URL. Responde SOLO JSON con {\"relevance\": 0-10, \"reason\": \"<1 frase>\"}.\n"
        "Criterio: relevance=10 = la página ES exactamente sobre ese tema con datos oficiales/autoritativos. "
        "relevance=5 = tangencialmente relacionado. relevance=1 = no relacionado. "
        "relevance=0 = no se pudo leer o el snippet no dice nada útil.\n\n"
        f"TEMA: {topic}\n\n"
        f"URL: {url}\n\n"
        f"SNIPPET (primeros 2.5KB):\n{snippet}\n"
    )
    try:
        text = client.call([], user_input=prompt, temperature=0.1, max_tokens=200, json_mode=True)
        from lib.llm_client import parse_json_relaxed
        data = parse_json_relaxed(text)
        relevance = int(data.get("relevance", 0))
        reason = str(data.get("reason", ""))[:200]
    except Exception as e:
        relevance = 5  # assume neutral on error
        reason = f"llm_error: {e}"

    result = {"relevance": relevance, "reason": reason, "checked_at": now.isoformat()}
    cache.setdefault(url, {})["relevance_check"] = result
    _save_cache(cache)
    return result


def check(url: str, use_cache: bool = True, ttl_hours: int = 24) -> dict:
    """Check one URL. Returns {ok, status, final_url, wayback, trusted, checked_at}."""
    cache = _load_cache() if use_cache else {}
    now = datetime.now(timezone.utc)
    cached = cache.get(url)
    if cached and use_cache and "checked_at" in cached:
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
        cache[url] = {**cached, **result} if cached else result
        _save_cache(cache)
    return result


def check_with_relevance(url: str, topic: str, client=None, min_relevance: int = 5) -> dict:
    """Full pipeline: HEAD + Wayback + LLM relevance check.

    Returns the check result merged with relevance_check result.
    Filter: if relevance < min_relevance, ok=False.
    """
    result = check(url)
    rel = relevance_check(url, topic, client=client)
    result["relevance"] = rel.get("relevance", 0)
    result["relevance_reason"] = rel.get("reason", "")
    if result["relevance"] < min_relevance:
        result["ok"] = False
        result["fail_reason"] = f"low_relevance:{rel.get('relevance')}"
    return result


def filter_survivors(urls: list[dict], topic: str, client=None,
                     min_ok: int = 2, min_relevance: int = 5) -> list[dict]:
    """Given a list of {url, anchor, why}, return those that pass HEAD + relevance.

    Sort: ok=True AND high-relevance first, then by trusted, then wayback fallback.
    """
    results = []
    for entry in urls:
        url = entry["url"]
        r = check_with_relevance(url, topic, client=client, min_relevance=min_relevance)
        results.append({**entry, **r})
    results.sort(key=lambda e: (
        not e["ok"],
        -(e.get("relevance", 0)),
        not e.get("trusted", False),
        not e.get("wayback"),
    ))
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+", help="URLs to check")
    ap.add_argument("--topic", help="Topic for relevance check")
    ap.add_argument("--relevance", action="store_true", help="Run LLM relevance check")
    args = ap.parse_args()
    for u in args.urls:
        if args.relevance and args.topic:
            r = check_with_relevance(u, args.topic)
            print(f"{'OK ' if r['ok'] else 'FAIL'} [{r['status']}] rel={r.get('relevance', '?')} {u[:60]}  reason={r.get('relevance_reason','')[:60]}")
        else:
            r = check(u)
            print(f"{'OK ' if r['ok'] else 'FAIL'} [{r['status']}] {u}  trusted={r['trusted']}  wayback={r.get('wayback') or '-'}")
