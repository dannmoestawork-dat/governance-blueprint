# SPDX-License-Identifier: Apache-2.0
"""Flags directories whose scripts have moved well past their docs —
the newest script is N+ days newer than the directory's newest required doc."""

from __future__ import annotations

from . import Analyzer, Finding
from ..depmap import SCRIPT_EXTS

DAY = 86400.0


class DocDrift(Analyzer):
    name = "doc_drift"
    description = "Docs lagging code: scripts changed long after their docs."

    def run(self, conn, cfg) -> list[Finding]:
        rows = conn.execute("SELECT path, mtime FROM files").fetchall()
        newest_script: dict[str, float] = {}
        newest_doc: dict[str, float] = {}
        for r in rows:
            d, _, name = r["path"].rpartition("/")
            if "." + name.rsplit(".", 1)[-1] in SCRIPT_EXTS:
                newest_script[d] = max(newest_script.get(d, 0.0), r["mtime"])
            if name in cfg.required_docs:
                newest_doc[d] = max(newest_doc.get(d, 0.0), r["mtime"])
        findings = []
        for d, script_m in sorted(newest_script.items()):
            if d not in newest_doc:
                continue  # missing_docs covers absent docs
            lag_days = (script_m - newest_doc[d]) / DAY
            if lag_days >= cfg.drift_days:
                findings.append(Finding(
                    "info", d,
                    f"docs are ~{int(lag_days)} days older than the newest script"))
        return findings
