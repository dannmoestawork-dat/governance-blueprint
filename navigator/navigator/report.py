# SPDX-License-Identifier: Apache-2.0
"""Written deliverables: the findings report and the memory report.

Navigator is a manager — its output is files you can open tomorrow, not
terminal scroll. Both reports are fully deterministic (no model) and land
in the outbox with a timestamped name. The findings report also tracks the
delta since the previous report, so iteration is visible.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from . import db
from .depmap import roles


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")


def _outbox(cfg) -> Path:
    out = cfg.data_dir / "outbox"
    out.mkdir(parents=True, exist_ok=True)
    return out


def write_report(conn, cfg) -> Path:
    n_files = conn.execute("SELECT COUNT(*) AS n FROM files").fetchone()["n"]
    n_edges = conn.execute("SELECT COUNT(*) AS n FROM deps").fetchone()["n"]
    n_open = conn.execute(
        "SELECT COUNT(*) AS n FROM findings WHERE status='open'").fetchone()["n"]
    last = conn.execute("SELECT value FROM meta WHERE key='last_index'").fetchone()

    lines = [
        f"# Navigator findings report — {_stamp()} UTC",
        "## [AI-GENERATED] (deterministic — no model involved)",
        "",
        f"- Files indexed: **{n_files}**  (last index: {last['value'] if last else 'never'})",
        f"- Dependency edges: **{n_edges}**",
        f"- Open findings: **{n_open}**",
    ]

    prev_row = conn.execute(
        "SELECT value FROM meta WHERE key='last_report_stats'").fetchone()
    if prev_row:
        prev = json.loads(prev_row["value"])
        lines.append(
            f"- Change since last report: files {n_files - prev['files']:+d}, "
            f"edges {n_edges - prev['edges']:+d}, "
            f"open findings {n_open - prev['open']:+d}")
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES('last_report_stats', ?)",
        (json.dumps({"files": n_files, "edges": n_edges, "open": n_open}),))
    conn.commit()

    role_counts: dict[str, int] = {}
    for v in roles(conn).values():
        role_counts[v] = role_counts.get(v, 0) + 1
    lines += ["", "## Tool roles",
              ", ".join(f"{k}: {v}" for k, v in sorted(role_counts.items()))]

    lines += ["", "## Open findings by analyzer"]
    for r in conn.execute(
            "SELECT analyzer, severity, COUNT(*) AS n FROM findings "
            "WHERE status='open' GROUP BY analyzer, severity ORDER BY n DESC"):
        lines.append(f"- {r['analyzer']} [{r['severity']}]: {r['n']}")

    lines += ["", "## Hotspots (most open findings by project area)"]
    spots: dict[str, int] = {}
    for r in conn.execute("SELECT path FROM findings WHERE status='open'"):
        parts = (r["path"] or "").split("/")
        if len(parts) >= 2:
            spots["/".join(parts[:2])] = spots.get("/".join(parts[:2]), 0) + 1
    for scope, n in sorted(spots.items(), key=lambda kv: -kv[1])[:10]:
        lines.append(f"- {scope}: {n}")

    lines += ["", "## Understanding (summaries by status)"]
    for r in conn.execute(
            "SELECT scope, status, updated FROM summaries ORDER BY status, scope"):
        lines.append(f"- [{r['status']}] {r['scope']}  (updated {r['updated']})")
    if not conn.execute("SELECT 1 FROM summaries LIMIT 1").fetchone():
        lines.append("- none yet — run `navigator sense <scope>`")

    lines += ["", "## Latest recommendations"]
    recs = conn.execute(
        "SELECT body, rationale FROM recommendations ORDER BY id DESC LIMIT 8").fetchall()
    lines += [f"- {r['body']}  _(why: {r['rationale']})_" for r in recs] or ["- none yet"]

    path = _outbox(cfg) / f"REPORT_{_stamp()}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_memory_report(conn, cfg) -> Path:
    """The knowledge dump: everything Navigator currently believes and was told."""
    lines = [
        f"# Navigator memory report — {_stamp()} UTC",
        "## [AI-GENERATED] (deterministic — this is the database, made readable)",
        "",
        "## What it believes (summaries)",
    ]
    rows = conn.execute(
        "SELECT scope, status, model, updated, body FROM summaries ORDER BY scope").fetchall()
    for r in rows:
        lines += [f"### [{r['status']}] {r['scope']}",
                  f"_model: {r['model']} · updated: {r['updated']}_", "",
                  r["body"] or "(empty)", ""]
    if not rows:
        lines.append("Nothing yet — no scope has been summarized.")

    lines += ["## What you taught it (feedback, by scope — durable)"]
    fb = conn.execute(
        "SELECT scope, note, created FROM feedback ORDER BY scope, id").fetchall()
    cur_scope = None
    for r in fb:
        if r["scope"] != cur_scope:
            cur_scope = r["scope"]
            lines.append(f"### {cur_scope}")
        lines.append(f"- [{r['created']}] {r['note']}")
    if not fb:
        lines.append("No feedback recorded yet.")

    lines += ["", "## What it has done (last 12 analyzer runs)"]
    for r in conn.execute(
            "SELECT analyzer, finished, status, findings FROM analyzer_runs "
            "ORDER BY id DESC LIMIT 12"):
        lines.append(f"- {r['finished']}  {r['analyzer']}: {r['status']}, "
                     f"{r['findings']} findings")

    wiki_pages = sorted((cfg.wiki_dir / "pages").glob("*.md")) \
        if (cfg.wiki_dir / "pages").is_dir() else []
    logs = sorted((cfg.wiki_dir / "log").glob("*.md")) \
        if (cfg.wiki_dir / "log").is_dir() else []
    lines += ["", "## Its own wiki",
              f"- {len(logs)} daily action logs, {len(wiki_pages)} topic pages "
              f"(in {cfg.wiki_dir})"]

    path = _outbox(cfg) / f"MEMORY_REPORT_{_stamp()}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
