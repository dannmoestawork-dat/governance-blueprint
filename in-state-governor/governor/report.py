# SPDX-License-Identifier: Apache-2.0
"""Render findings as a markdown drift ledger or JSON."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone

from .rules import Finding, SEVERITIES

_DECISION_LINE = "Decision: [ ] Accept [ ] Reject [ ] Defer"


def to_json(findings: list[Finding], *, root: str = "") -> str:
    """Serialize findings to a stable JSON document."""
    payload = {
        "tool": "in-state-governor",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": root,
        "summary": _severity_counts(findings),
        "count": len(findings),
        "findings": [f.to_dict() for f in findings],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def to_markdown(findings: list[Finding], *, root: str = "") -> str:
    """Render a markdown drift ledger.

    Layout: a severity rollup table, then findings grouped by rule. Each
    finding carries ``path:line``, its message, and a blank decision line so a
    human reviewer adjudicates every deviation — the ledger is the seam where a
    person accepts or rejects drift, deterministically surfaced by the checker.
    """
    out: list[str] = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out.append("# Governance Drift Ledger")
    out.append("")
    out.append(f"- Generated (UTC): {ts}")
    if root:
        out.append(f"- Scanned root: `{root}`")
    out.append(f"- Total findings: **{len(findings)}**")
    out.append("")

    # Severity rollup table.
    counts = _severity_counts(findings)
    out.append("## Severity rollup")
    out.append("")
    out.append("| Severity | Count |")
    out.append("| --- | --- |")
    for sev in SEVERITIES:
        out.append(f"| {sev} | {counts.get(sev, 0)} |")
    out.append(f"| **total** | **{len(findings)}** |")
    out.append("")

    if not findings:
        out.append("No drift detected. All enabled rules passed.")
        out.append("")
        return "\n".join(out)

    # Group by rule.
    by_rule: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        by_rule[f.rule_id].append(f)

    out.append("## Findings by rule")
    out.append("")
    for rule_id in sorted(by_rule):
        rule_findings = by_rule[rule_id]
        out.append(f"### `{rule_id}` ({len(rule_findings)})")
        out.append("")
        for f in rule_findings:
            loc = f"`{f.path}`" if f.line == 0 else f"`{f.path}:{f.line}`"
            out.append(f"- [{f.severity}] {loc} — {f.message}")
            out.append(f"  - {_DECISION_LINE}")
        out.append("")

    return "\n".join(out)


def _severity_counts(findings: list[Finding]) -> dict[str, int]:
    c = Counter(f.severity for f in findings)
    return {sev: c.get(sev, 0) for sev in SEVERITIES}
