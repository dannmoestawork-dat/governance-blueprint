# SPDX-License-Identifier: Apache-2.0
"""Optional web access with an offline-first cache.

Every successful fetch is cached on disk; when the network is unreachable
the cache answers instead, so nothing in the app hard-depends on being
online. If a SearXNG URL is configured (e.g. a self-hosted instance),
`search()` works too.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import httpx


def _cache_key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def fetch(cfg, url: str, timeout: int = 30) -> dict:
    cache = Path(cfg.web_cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    entry = cache / f"{_cache_key(url)}.json"
    try:
        r = httpx.get(url, timeout=timeout, follow_redirects=True)
        r.raise_for_status()
        data = {"url": url, "status": r.status_code, "text": r.text[:500_000],
                "from_cache": False}
        entry.write_text(json.dumps(data), encoding="utf-8")
        return data
    except httpx.HTTPError as e:
        if entry.exists():
            data = json.loads(entry.read_text(encoding="utf-8"))
            data["from_cache"] = True
            return data
        return {"url": url, "status": 0, "text": "", "from_cache": False,
                "error": str(e)}


def search(cfg, query: str, timeout: int = 30) -> list[dict]:
    if not cfg.searx_url:
        return []
    url = f"{cfg.searx_url.rstrip('/')}/search?q={httpx.QueryParams({'q': query})['q']}&format=json"
    data = fetch(cfg, url, timeout)
    try:
        results = json.loads(data["text"]).get("results", [])
        return [{"title": r.get("title", ""), "url": r.get("url", ""),
                 "snippet": r.get("content", "")} for r in results[:10]]
    except (json.JSONDecodeError, KeyError):
        return []
