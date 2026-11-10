# SPDX-License-Identifier: Apache-2.0
"""Sense-making layer: living, plain-language summaries of what each part of
the tree appears to be FOR, refined by user feedback.

The contract (and the trust model):
  - The machine assembles REAL evidence (file listing, doc excerpts, dep
    edges) — deterministically.
  - The model narrates that evidence in plain language. Its output is stored
    with status 'perceived'.
  - The user confirms ('confirmed') or corrects ('corrected' + a note).
    Feedback notes are durable: every later regeneration feeds them back to
    the model and they are always displayed alongside the summary.
"""

from __future__ import annotations

from . import db
from .llm import LLMClient


class NoEvidenceError(RuntimeError):
    """Raised instead of letting a model narrate an empty scope.

    Field lesson: running `sense` on a not-yet-indexed scope once handed the
    model an empty evidence pack, and it speculated from the directory name
    alone. Structure must refuse; instructions don't."""

SYSTEM_PROMPT = (
    "You are a plain-language analyst helping a non-programmer understand "
    "their own project tree. Using ONLY the evidence provided, describe what "
    "this part of the project appears to be for: its perceived goals, what "
    "its tools produce, and what they depend on. Clearly separate what the "
    "evidence shows from what you are inferring. Never invent files "
    "or facts not present in the evidence. If a USER FEEDBACK section is "
    "present, it is ground truth from the owner: your summary MUST restate "
    "the substance of EVERY feedback note (asks prefixed 'Standing ask:' "
    "may be acknowledged in one line instead), and feedback overrides any "
    "conflicting inference. 8 sentences maximum."
)

DOC_NAMES = {"README.md", "MAINTENANCE_LOG.md", "PROJECT_CONTEXT.md", "CONTEXT.md"}


def build_evidence(conn, scope: str, max_files: int = 60, excerpt_lines: int = 40) -> str:
    """Deterministic evidence pack for a scope (a path-key prefix)."""
    like = scope.rstrip("/") + "/%"
    files = conn.execute(
        "SELECT path, ext, size FROM files WHERE path LIKE ? OR path = ? "
        "ORDER BY path LIMIT ?", (like, scope, max_files + 1)).fetchall()
    lines = [f"SCOPE: {scope}", "", "FILES (name, bytes):"]
    for r in files[:max_files]:
        lines.append(f"  {r['path']}  {r['size']}")
    if len(files) > max_files:
        lines.append(f"  … (more files exist; listing truncated at {max_files})")

    for r in files:
        name = r["path"].rsplit("/", 1)[-1]
        if name in DOC_NAMES:
            row = conn.execute(
                "SELECT content FROM files_fts WHERE rowid="
                "(SELECT id FROM files WHERE path=?)", (r["path"],)).fetchone()
            if row and row["content"]:
                excerpt = "\n".join(row["content"].splitlines()[:excerpt_lines])
                lines += ["", f"DOC EXCERPT — {r['path']}:", excerpt]

    edges = conn.execute(
        "SELECT src, dst, kind FROM deps WHERE src LIKE ? OR dst LIKE ? LIMIT 40",
        (like, like)).fetchall()
    if edges:
        lines += ["", "DEPENDENCY EDGES (src -> dst [kind]):"]
        lines += [f"  {e['src']} -> {e['dst']} [{e['kind']}]" for e in edges]

    notes = conn.execute(
        "SELECT note, created FROM feedback WHERE scope=? ORDER BY id", (scope,)).fetchall()
    if notes:
        lines += ["", "USER FEEDBACK (authoritative — must be honored):"]
        lines += [f"  [{n['created']}] {n['note']}" for n in notes]
    return "\n".join(lines)


def summarize(conn, cfg, scope: str) -> dict:
    """(Re)generate the perceived-goals summary for a scope."""
    like = scope.rstrip("/") + "/%"
    n = conn.execute("SELECT COUNT(*) AS n FROM files WHERE path LIKE ? OR path = ?",
                     (like, scope)).fetchone()["n"]
    if n == 0:
        raise NoEvidenceError(
            f"No indexed files under '{scope}' — refusing to summarize without "
            "evidence. Run `navigator index` (then `map` and `analyze`) first, "
            "or check the scope name against `navigator status` / the "
            "dashboard's left pane.")
    evidence = build_evidence(conn, scope)
    client = LLMClient(cfg)
    body = client.chat(SYSTEM_PROMPT, evidence)
    now = db.utcnow()
    existing = conn.execute("SELECT id FROM summaries WHERE scope=?", (scope,)).fetchone()
    if existing:
        # regeneration resets status to 'perceived' — a human hasn't seen THIS text
        conn.execute(
            "UPDATE summaries SET body=?, status='perceived', model=?, updated=? WHERE scope=?",
            (body, f"{cfg.llm_backend}:{cfg.llm_model}", now, scope))
    else:
        conn.execute(
            "INSERT INTO summaries(scope, body, status, model, created, updated) "
            "VALUES(?,?,'perceived',?,?,?)",
            (scope, body, f"{cfg.llm_backend}:{cfg.llm_model}", now, now))
    conn.commit()
    return {"scope": scope, "body": body, "status": "perceived"}


def add_feedback(conn, scope: str, note: str) -> None:
    """Record a durable correction/refinement; mark the summary corrected."""
    conn.execute("INSERT INTO feedback(scope, note, created) VALUES(?,?,?)",
                 (scope, note, db.utcnow()))
    conn.execute("UPDATE summaries SET status='corrected', updated=? WHERE scope=?",
                 (db.utcnow(), scope))
    conn.commit()


def confirm(conn, scope: str) -> None:
    conn.execute("UPDATE summaries SET status='confirmed', updated=? WHERE scope=?",
                 (db.utcnow(), scope))
    conn.commit()


def get_summary(conn, scope: str):
    return conn.execute("SELECT * FROM summaries WHERE scope=?", (scope,)).fetchone()
