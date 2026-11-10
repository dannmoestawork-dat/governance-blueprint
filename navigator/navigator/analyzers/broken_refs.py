# SPDX-License-Identifier: Apache-2.0
"""Flags file paths referenced in code/docs that no longer exist.

Conservative on purpose: a literal is only flagged when its parent directory
IS in the index but the file is not — that's the signature of a reference
that used to work and went stale, and it avoids flagging templates,
examples, and outputs that scripts create at runtime.
"""

from __future__ import annotations

from . import Analyzer, Finding
from ..depmap import _PATH_LIT, _texts


class BrokenRefs(Analyzer):
    name = "broken_refs"
    description = "File references in code/docs whose target no longer exists."

    def run(self, conn, cfg) -> list[Finding]:
        texts = _texts(conn)
        all_keys = {r["path"] for r in conn.execute("SELECT path FROM files")}
        all_dirs = {k.rsplit("/", 1)[0] for k in all_keys if "/" in k}

        findings = []
        for src, content in texts.items():
            src_dir = src.rsplit("/", 1)[0] if "/" in src else ""
            seen: set[str] = set()
            for m in _PATH_LIT.finditer(content):
                cand = m.group(1).replace("\\", "/").lstrip("./")
                if cand in seen or "/" not in cand:
                    continue
                seen.add(cand)
                guesses = [f"{src_dir}/{cand}" if src_dir else cand, cand]
                if any(g in all_keys for g in guesses):
                    continue
                # only flag if the parent dir exists in-tree (stale, not template)
                stale = next((g for g in guesses
                              if g.rsplit("/", 1)[0] in all_dirs), None)
                if stale:
                    findings.append(Finding(
                        "warn", src, f"references missing file: {cand}"))
        return findings
