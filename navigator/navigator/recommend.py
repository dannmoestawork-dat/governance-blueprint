# SPDX-License-Identifier: Apache-2.0
"""Next-step recommendations.

Mechanical first: open findings and dependency roles are summarized into a
deterministic digest. If a model is configured, it turns the digest into
ranked plain-language recommendations; with the stub backend you still get
useful templated recommendations — the app never depends on a model to be
helpful.
"""

from __future__ import annotations

from . import db
from .depmap import roles
from .llm import LLMClient, LLMError

SYSTEM_PROMPT = (
    "You are a project-management assistant for a non-programmer. From the "
    "digest below, write the 5 to 8 most valuable next steps to improve the "
    "project tree's clarity, completeness, and efficacy. One step per line, "
    "formatted exactly as: STEP: <action> | WHY: <reason>. Plain language, "
    "no jargon, reference real paths from the digest only. If the digest "
    "contains USER STANDING ASKS, they are authoritative direction from the "
    "user: address each one with at least one step before generic cleanup."
)


def build_digest(conn) -> str:
    lines = ["OPEN FINDINGS BY ANALYZER:"]
    rows = conn.execute(
        "SELECT analyzer, severity, COUNT(*) AS n FROM findings "
        "WHERE status='open' GROUP BY analyzer, severity ORDER BY n DESC").fetchall()
    for r in rows:
        lines.append(f"  {r['analyzer']} [{r['severity']}]: {r['n']} open")
    lines.append("")
    lines.append("SAMPLE FINDINGS (worst first):")
    sample = conn.execute(
        "SELECT analyzer, severity, path, message FROM findings WHERE status='open' "
        "ORDER BY CASE severity WHEN 'error' THEN 0 WHEN 'warn' THEN 1 ELSE 2 END "
        "LIMIT 15").fetchall()
    for r in sample:
        lines.append(f"  [{r['severity']}] {r['path']}: {r['message']}")
    role_map = roles(conn)
    counts: dict[str, int] = {}
    for v in role_map.values():
        counts[v] = counts.get(v, 0) + 1
    lines.append("")
    lines.append("TOOL ROLES: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    hubs = [k for k, v in role_map.items() if v in ("root", "hub")][:10]
    if hubs:
        lines.append("MOST DEPENDED-ON TOOLS: " + ", ".join(hubs))
    notes = conn.execute(
        "SELECT scope, note FROM feedback ORDER BY id DESC LIMIT 20").fetchall()
    if notes:
        lines.append("")
        lines.append("USER STANDING ASKS & FEEDBACK (authoritative, newest first):")
        lines += [f"  [{n['scope']}] {n['note']}" for n in notes]
    return "\n".join(lines)


def _mechanical(conn) -> list[tuple[str, str]]:
    """Template fallback: top findings become recommendations directly."""
    recs = []
    rows = conn.execute(
        "SELECT analyzer, path, message, COUNT(*) OVER (PARTITION BY analyzer) AS n "
        "FROM findings WHERE status='open' "
        "ORDER BY CASE severity WHEN 'error' THEN 0 WHEN 'warn' THEN 1 ELSE 2 END "
        "LIMIT 5").fetchall()
    for r in rows:
        recs.append((f"Address {r['analyzer']} finding at {r['path']}: {r['message']}",
                     f"{r['n']} open findings from this analyzer overall."))
    return recs


def generate(conn, cfg) -> list[dict]:
    digest = build_digest(conn)
    pairs: list[tuple[str, str]] = []
    if cfg.llm_backend != "stub":
        try:
            text = LLMClient(cfg).chat(SYSTEM_PROMPT, digest)
            for line in text.splitlines():
                if line.strip().upper().startswith("STEP:") and "| WHY:" in line.upper():
                    step, _, why = line.partition("|")
                    pairs.append((step.split(":", 1)[1].strip(),
                                  why.split(":", 1)[1].strip()))
        except LLMError:
            pairs = []
    if not pairs:
        pairs = _mechanical(conn)
    now = db.utcnow()
    out = []
    for body, rationale in pairs:
        conn.execute(
            "INSERT INTO recommendations(body, rationale, created) VALUES(?,?,?)",
            (body, rationale, now))
        out.append({"body": body, "rationale": rationale})
    conn.commit()
    return out
