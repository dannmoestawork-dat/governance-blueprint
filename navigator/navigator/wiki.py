# SPDX-License-Identifier: Apache-2.0
"""The navigator's own wiki: a plain-markdown record of everything it does
and learns. Lives in data/wiki/, uses ordinary markdown files (compatible
with any markdown note-taking tool), and is included as an index root — so
the navigator full-text searches its own past work and gets better at
repeating it.

  wiki/log/YYYY-MM-DD.md   — append-only daily action log
  wiki/pages/<slug>.md     — durable topic pages (processes, lessons)
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M")


def log_event(wiki_dir: Path, kind: str, detail: str) -> Path:
    log_dir = wiki_dir / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    day_file = log_dir / f"{_today()}.md"
    if not day_file.exists():
        day_file.write_text(f"# Navigator log — {_today()}\n\n", encoding="utf-8")
    with open(day_file, "a", encoding="utf-8") as f:
        f.write(f"- **{_now()} UTC — {kind}:** {detail}\n")
    return day_file


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:80]


def write_page(wiki_dir: Path, title: str, body: str) -> Path:
    pages = wiki_dir / "pages"
    pages.mkdir(parents=True, exist_ok=True)
    page = pages / f"{slugify(title)}.md"
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    page.write_text(f"# {title}\n\n_Updated: {stamp}_\n\n{body}\n", encoding="utf-8")
    return page
