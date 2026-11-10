# SPDX-License-Identifier: Apache-2.0
"""Flags directories that contain scripts but lack their required docs
(default: MAINTENANCE_LOG.md — configurable per clone)."""

from __future__ import annotations

from . import Analyzer, Finding
from ..depmap import SCRIPT_EXTS


class MissingDocs(Analyzer):
    name = "missing_docs"
    description = "Script directories missing required documentation files."

    def run(self, conn, cfg) -> list[Finding]:
        rows = conn.execute("SELECT path FROM files").fetchall()
        dirs_with_scripts: set[str] = set()
        files_by_dir: dict[str, set[str]] = {}
        for r in rows:
            path = r["path"]
            d, _, name = path.rpartition("/")
            files_by_dir.setdefault(d, set()).add(name)
            if "." + name.rsplit(".", 1)[-1] in SCRIPT_EXTS:
                dirs_with_scripts.add(d)
        findings = []
        for d in sorted(dirs_with_scripts):
            missing = [doc for doc in cfg.required_docs
                       if doc not in files_by_dir.get(d, set())]
            if missing:
                findings.append(Finding(
                    "warn", d,
                    f"contains scripts but is missing: {', '.join(missing)}"))
        return findings
