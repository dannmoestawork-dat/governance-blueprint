# SPDX-License-Identifier: Apache-2.0
"""Work orders: findings become delegation briefs for agents.

Navigator is a manager, not a laborer — it never writes into your tree.
For each analyzer with open findings it emits a work order: a brief any
agent (a coding-assistant session or a scheduled job) can execute, plus a
machine-readable JSON manifest of the targets. Fully deterministic.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

MAINT_LOG_SECTIONS = (
    "1. **Error Log** — date-stamped errors, root causes, resolutions.\n"
    "2. **Script & Approach Reasoning** — why each script exists, "
    "alternatives considered.\n"
    "3. **Dependencies** — libraries, versions, install locations.\n"
    "4. **Session Handoff Notes** — end-of-session summary and next steps.")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")


def _grouped(rows) -> dict[str, list]:
    groups: dict[str, list] = {}
    for r in rows:
        parts = (r["path"] or "").split("/")
        key = "/".join(parts[:2]) if len(parts) >= 2 else (r["path"] or "(tree-wide)")
        groups.setdefault(key, []).append(r)
    return dict(sorted(groups.items()))


def write_work_orders(conn, cfg) -> list[Path]:
    out_dir = cfg.data_dir / "outbox"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _stamp()
    paths: list[Path] = []

    docs = conn.execute(
        "SELECT path, message FROM findings "
        "WHERE status='open' AND analyzer='missing_docs' ORDER BY path").fetchall()
    if docs:
        required = ", ".join(cfg.required_docs)
        lines = [
            f"# WORK ORDER — create missing maintenance docs — {stamp} UTC",
            "## [AI-GENERATED] — issued by Navigator; for execution by an agent",
            "",
            f"**Task:** each directory listed below contains scripts but is "
            f"missing its required documentation ({required}). Create the "
            "missing doc(s) in each directory.",
            "",
            "**Direction to the agent (read before starting):**",
            "- Read the scripts in the directory FIRST; the doc must describe "
            "what actually exists, never boilerplate.",
            "- Use the house format with these sections:",
            MAINT_LOG_SECTIONS,
            "- Keep entries concise. Tag the file `[AI-GENERATED]` — a human "
            "has not reviewed it yet.",
            "- Do not modify any script. Docs only.",
            "- Work one project group at a time; report back per group.",
            "",
            f"**Targets: {len(docs)} directories**, grouped by project:",
            "",
        ]
        target_list = []
        for group, rows in _grouped(docs).items():
            lines.append(f"## {group}  ({len(rows)})")
            for r in rows:
                lines.append(f"- {r['path']}  ({r['message']})")
                target_list.append(r["path"])
            lines.append("")
        md = out_dir / f"WORK_ORDER_missing_docs_{stamp}.md"
        md.write_text("\n".join(lines), encoding="utf-8")
        manifest = out_dir / f"WORK_ORDER_missing_docs_{stamp}.json"
        manifest.write_text(json.dumps(
            {"order": md.name, "task": "create_missing_docs",
             "required_docs": cfg.required_docs, "targets": target_list},
            indent=2), encoding="utf-8")
        paths += [md, manifest]

    for analyzer, task_line in (
        ("broken_refs", "Fix or remove each stale file reference (the file it "
                        "points at no longer exists). Confirm intent before "
                        "deleting any reference."),
        ("doc_drift", "Update the directory's docs to reflect the recent "
                      "script changes (docs are significantly older than the "
                      "newest script)."),
    ):
        rows = conn.execute(
            "SELECT path, message FROM findings "
            "WHERE status='open' AND analyzer=? ORDER BY path", (analyzer,)).fetchall()
        if not rows:
            continue
        lines = [
            f"# WORK ORDER — {analyzer} — {stamp} UTC",
            "## [AI-GENERATED] — issued by Navigator; for execution by an agent",
            "",
            f"**Task:** {task_line}",
            "",
            f"**Targets: {len(rows)}**",
            "",
        ]
        for group, grows in _grouped(rows).items():
            lines.append(f"## {group}  ({len(grows)})")
            lines += [f"- {r['path']}: {r['message']}" for r in grows]
            lines.append("")
        md = out_dir / f"WORK_ORDER_{analyzer}_{stamp}.md"
        md.write_text("\n".join(lines), encoding="utf-8")
        paths.append(md)

    return paths
