# SPDX-License-Identifier: Apache-2.0
"""Directory indexer.

Walks each configured root, prunes excluded directories, and records every
file's metadata. Text files (by extension, under a size cap) are full-text
indexed via SQLite FTS5; everything else is cataloged metadata-only — so a
tree full of large PDFs and spreadsheets indexes fast and the catalog is
still complete.

Incremental: a file whose size and mtime are unchanged is skipped. Files
that vanished from disk are removed from the index.
"""

from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from . import db
from .config import Config


def store_path(root: Path, abs_path: Path) -> str:
    """DB key for a file: '<root-name>/<relative posix path>'."""
    return f"{root.name}/{abs_path.relative_to(root).as_posix()}"


def _extract_text(path: Path, cap: int) -> str:
    try:
        with open(path, "rb") as f:
            raw = f.read(cap)
        return raw.decode("utf-8", errors="replace")
    except OSError:
        return ""


def index(conn, cfg: Config, progress=None) -> dict:
    """Index all roots. Returns counts: scanned/added_or_updated/unchanged/removed."""
    stats = {"scanned": 0, "updated": 0, "unchanged": 0, "removed": 0}
    known = {row["path"]: (row["size"], row["mtime"])
             for row in conn.execute("SELECT path, size, mtime FROM files")}
    seen: set[str] = set()

    roots = list(cfg.roots) + [cfg.wiki_dir] if cfg.wiki_dir.is_dir() else list(cfg.roots)
    for root in roots:
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in cfg.exclude_dirs]
            for name in filenames:
                abs_path = Path(dirpath) / name
                key = store_path(root, abs_path)
                rel = abs_path.relative_to(root).as_posix()
                if any(fnmatch.fnmatch(rel, g) or fnmatch.fnmatch(name, g)
                       for g in cfg.exclude_globs):
                    continue
                try:
                    st = abs_path.stat()
                except OSError:
                    continue
                stats["scanned"] += 1
                seen.add(key)
                if key in known and known[key] == (st.st_size, st.st_mtime):
                    stats["unchanged"] += 1
                    continue
                ext = abs_path.suffix.lower()
                is_text = ext in cfg.text_exts
                content = _extract_text(abs_path, cfg.max_text_bytes) if is_text else ""
                db.upsert_file(conn, key, ext, st.st_size, st.st_mtime,
                               "text" if is_text else "binary", content)
                stats["updated"] += 1
                if progress and stats["updated"] % 500 == 0:
                    progress(stats)

    gone = [p for p in known if p not in seen]
    db.remove_files(conn, gone)
    stats["removed"] = len(gone)
    conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES('last_index', ?)",
                 (db.utcnow(),))
    conn.commit()
    return stats


def resolve_store_path(cfg: Config, key: str) -> Path | None:
    """Turn a DB key back into an absolute path on this machine."""
    for root in list(cfg.roots) + [cfg.wiki_dir]:
        head, _, rel = key.partition("/")
        if head == root.name:
            p = root / rel
            if p.exists():
                return p
    return None
