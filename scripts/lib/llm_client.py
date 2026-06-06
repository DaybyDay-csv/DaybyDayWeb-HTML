#!/usr/bin/env python3
"""
llm_client.py — MiniMax M3 client with modular prompt assembly and retry.

Strategy to avoid the M2.7 empty-response bug:
- Keep each call's total prompt < 16KB by composing from small modules.
- Retry on empty response, JSON parse error, or rate limit (429).
- Surface a structured error on permanent failure.

Usage:
    from lib.llm_client import LLMClient
    client = LLMClient()
    raw = client.call([("00_voice.md", "..."), ("03_write_es.md", "...")], temperature=0.4)
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent.parent
PROMPTS = REPO / "scripts" / "lib" / "prompts"

API_BASE = os.environ.get("MINIMAX_API_BASE", "https://api.minimax.io/anthropic")
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MODEL = os.environ.get("MINIMAX_MODEL", "MiniMax-M3")


class LLMError(Exception):
    pass


class LLMClient:
    def __init__(self, api_key: str | None = None, model: str | None = None, base: str | None = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise LLMError(
                "MINIMAX_API_KEY no está en el entorno. "
                "Añade 'export MINIMAX_API_KEY=...' en tu shell o en ~/.zshrc."
            )
        self.model = model or MODEL
        self.base = base or API_BASE

    def load_prompt(self, name: str) -> str:
        path = PROMPTS / name
        if not path.exists():
            raise LLMError(f"Prompt module missing: {path}")
        return path.read_text(encoding="utf-8")

    def assemble(self, modules: Iterable[str]) -> str:
        parts = []
        total = 0
        for name in modules:
            body = self.load_prompt(name)
            parts.append(f"## {name}\n\n{body}")
            total += len(body)
        if total > 16_000:
            sys.stderr.write(f"WARN: prompt {total} bytes > 16KB. M2.7 may return empty.\n")
        return "\n\n---\n\n".join(parts)

    def call(
        self,
        modules: Iterable[str],
        user_input: str = "",
        temperature: float = 0.4,
        max_tokens: int = 8000,
        max_retries: int = 3,
        json_mode: bool = True,
        save_raw_path: str | None = None,
    ) -> str:
        """Single LLM call. Returns raw text content. Auto-retries on empty/429.

        M3 is Anthropic-compatible — uses messages API with system field.
        save_raw_path: if set, writes the raw response to this file (debug aid).
        """
        system = self.assemble(modules)
        if json_mode:
            system = system + "\n\nResponde SOLO JSON válido. Sin markdown, sin ```json, sin texto adicional."
        messages = []
        if user_input:
            messages.append({"role": "user", "content": user_input})

        body = {
            "model": self.model,
            "system": system,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        last_err = None
        for attempt in range(1, max_retries + 1):
            # Adaptive timeout: scale with max_tokens (M3 is slow on long outputs)
            timeout_s = max(180, int(body.get("max_tokens", 2000) * 0.08))
            try:
                req = urllib.request.Request(
                    f"{self.base}/v1/messages",
                    data=json.dumps(body).encode("utf-8"),
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                # Anthropic format: content is a list of blocks (thinking + text)
                blocks = payload.get("content", [])
                content = ""
                for b in blocks:
                    if isinstance(b, dict) and b.get("type") == "text":
                        content += b.get("text", "")
                    elif isinstance(b, str):
                        content += b
                if not content or not content.strip():
                    last_err = "empty_response"
                    sys.stderr.write(f"[LLM] empty response (attempt {attempt}/{max_retries}, timeout={timeout_s}s)\n")
                    time.sleep(2 * attempt)
                    continue
                # Save raw if requested
                if save_raw_path:
                    try:
                        Path(save_raw_path).parent.mkdir(parents=True, exist_ok=True)
                        Path(save_raw_path).write_text(content, encoding="utf-8")
                    except Exception as e:
                        sys.stderr.write(f"[LLM] failed to save raw: {e}\n")
                # Check truncation — bump and retry, but max out at 16K
                stop_reason = payload.get("stop_reason", "")
                if stop_reason == "max_tokens":
                    new_max = min(16000, int(body.get("max_tokens", 2000) * 1.5))
                    if new_max <= body.get("max_tokens", 2000):
                        # Already at cap, return what we have
                        sys.stderr.write(f"[LLM] truncated at max cap {body.get('max_tokens')}. Returning partial.\n")
                        return content
                    sys.stderr.write(f"[LLM] truncated at {body.get('max_tokens')}. Bumping to {new_max}.\n")
                    body["max_tokens"] = new_max
                    last_err = "truncated"
                    time.sleep(1)
                    continue
                return content
            except urllib.error.HTTPError as e:
                body_txt = e.read().decode("utf-8", errors="replace")[:300]
                if e.code == 429:
                    last_err = f"429_rate_limit: {body_txt}"
                    sys.stderr.write(f"[LLM] 429 (attempt {attempt}/{max_retries}). Esperando {2**attempt}s.\n")
                    time.sleep(2 ** attempt)
                    continue
                last_err = f"http_{e.code}: {body_txt}"
                if e.code in (400, 401, 403):
                    raise LLMError(f"Perm/auth error {e.code}: {body_txt}")
                sys.stderr.write(f"[LLM] HTTP {e.code} (attempt {attempt}/{max_retries})\n")
                time.sleep(2 * attempt)
            except (urllib.error.URLError, TimeoutError) as e:
                last_err = f"network/timeout: {e}"
                sys.stderr.write(f"[LLM] {last_err} (attempt {attempt}/{max_retries}, timeout={timeout_s}s)\n")
                time.sleep(2 * attempt)
            except json.JSONDecodeError as e:
                last_err = f"json_decode: {e}"
                sys.stderr.write(f"[LLM] json decode (attempt {attempt}/{max_retries})\n")
                time.sleep(1)
        raise LLMError(f"LLM call failed after {max_retries} attempts: {last_err}")

    def call_json(
        self,
        modules: Iterable[str],
        user_input: str = "",
        temperature: float = 0.3,
        max_tokens: int = 8000,
        max_retries: int = 6,
    ) -> dict:
        """Call expecting JSON. Strips markdown fences if present, then parses."""
        text = self.call(modules, user_input, temperature, max_tokens, max_retries, json_mode=True)
        return parse_json_relaxed(text)


def parse_json_relaxed(text: str) -> dict:
    """Strip ```json fences, find first { and last }, parse."""
    s = text.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s)
    s = re.sub(r"\s*```$", "", s)
    # Find outermost JSON object
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise LLMError(f"No JSON object found in response. First 200 chars: {text[:200]!r}")
    candidate = s[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        # Try to fix common issues: trailing commas, unescaped quotes
        cleaned = re.sub(r",\s*([}\]])", r"\1", candidate)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            raise LLMError(
                f"JSON parse failed: {e}. First 500 chars of candidate: {candidate[:500]!r}"
            )


if __name__ == "__main__":
    # Smoke test
    if not API_KEY:
        print("Set MINIMAX_API_KEY to run smoke test.")
        sys.exit(0)
    client = LLMClient()
    out = client.call_json(
        ["00_voice.md", "01_research.md"],
        user_input='Devuelve JSON con {"ok": true, "msg": "pong"}',
        max_tokens=200,
    )
    print("Smoke test OK:", out)
