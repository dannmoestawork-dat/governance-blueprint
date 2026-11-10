# SPDX-License-Identifier: Apache-2.0
"""Gap-analyzer framework.

An analyzer is a small class with a name, a plain-language description, and a
run() that returns Findings. Every run is recorded (analyzer_runs) and every
finding deduplicated (findings), so the dashboard can show what ran, when,
and what it found. Add a new analyzer by subclassing Analyzer and listing it
in REGISTRY.
"""

from __future__ import annotations

from dataclasses import dataclass

from .. import db


@dataclass
class Finding:
    severity: str        # 'info' | 'warn' | 'error'
    path: str            # DB path key (or '' for tree-wide findings)
    message: str


class Analyzer:
    name = "base"
    description = ""

    def run(self, conn, cfg) -> list[Finding]:  # pragma: no cover
        raise NotImplementedError


def run_analyzer(conn, cfg, analyzer: Analyzer) -> dict:
    cur = conn.execute(
        "INSERT INTO analyzer_runs(analyzer, started, status) VALUES(?,?,'running')",
        (analyzer.name, db.utcnow()))
    run_id = cur.lastrowid
    try:
        findings = analyzer.run(conn, cfg)
        status = "ok"
    except Exception as e:  # record the failure instead of dying
        findings = [Finding("error", "", f"analyzer crashed: {e}")]
        status = "failed"
    new = 0
    for f in findings:
        cur = conn.execute(
            "INSERT OR IGNORE INTO findings(run_id, analyzer, severity, path, message) "
            "VALUES(?,?,?,?,?)",
            (run_id, analyzer.name, f.severity, f.path, f.message))
        new += cur.rowcount
    conn.execute(
        "UPDATE analyzer_runs SET finished=?, status=?, findings=? WHERE id=?",
        (db.utcnow(), status, len(findings), run_id))
    conn.commit()
    return {"analyzer": analyzer.name, "status": status,
            "findings": len(findings), "new": new}


def get_registry() -> dict[str, Analyzer]:
    from .missing_docs import MissingDocs
    from .broken_refs import BrokenRefs
    from .doc_drift import DocDrift
    items = [MissingDocs(), BrokenRefs(), DocDrift()]
    return {a.name: a for a in items}
