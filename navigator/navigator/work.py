# SPDX-License-Identifier: Apache-2.0
"""The ask executor: turns `Standing ask:` feedback notes into finished
deliverables — one combined memo/artifact per ask, written to the outbox.

This is the anti-chatbot module. The model is instructed to PRODUCE the
deliverable (the memo, the comparison, the drafted prompt), never advice
about producing it. Evidence is full file text, mechanically selected and
fully manifested in the artifact — including a count of what was NOT read,
so coverage is never silently overstated.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from .llm import LLMClient
from .sense import NoEvidenceError
from .wiki import slugify

MAX_FILES = 15
MAX_CHARS_PER_FILE = 6000

# When a scope is too big to read whole, prefer plan-shaped and fresh files.
PLAN_HINTS = re.compile(r"plan|roadmap|queue|todo|next|board|runbook|brief", re.I)

WORK_PROMPT = (
    "You are a working analyst producing a FINISHED deliverable for a "
    "non-programmer manager. The user's standing ask is below, followed by "
    "real evidence (full file texts). Produce the deliverable itself — the "
    "memo, the comparison, or the drafted prompt the ask requests — NOT "
    "advice about producing it, NOT a plan to do it later, and no offers of "
    "further help. Use only the evidence; cite real file paths for every "
    "claim; where the evidence is insufficient for part of the ask, name "
    "exactly what is missing. Plain language, headed sections, ready to use."
)


def list_asks(conn):
    return conn.execute(
        "SELECT id, scope, note, created FROM feedback "
        "WHERE note LIKE 'Standing ask:%' ORDER BY id").fetchall()


def _gather_evidence(conn, scope: str):
    like = scope.rstrip("/") + "/%"
    rows = conn.execute(
        "SELECT f.path AS path, f.mtime AS mtime, files_fts.content AS content "
        "FROM files_fts JOIN files f ON f.id = files_fts.rowid "
        "WHERE (f.path LIKE ? OR f.path = ?) AND f.kind='text'",
        (like, scope)).fetchall()
    if not rows:
        raise NoEvidenceError(
            f"No indexed text files under '{scope}' — cannot work this ask. "
            "Run `navigator index` or check the ask's scope.")
    ranked = sorted(rows, key=lambda r: (
        0 if PLAN_HINTS.search(r["path"].rsplit("/", 1)[-1]) else 1, -r["mtime"]))
    chosen = ranked[:MAX_FILES]
    omitted = len(rows) - len(chosen)
    blocks, manifest = [], []
    for r in chosen:
        text = (r["content"] or "")[:MAX_CHARS_PER_FILE]
        truncated = " (truncated)" if len(r["content"] or "") > MAX_CHARS_PER_FILE else ""
        manifest.append(f"- {r['path']}{truncated}")
        blocks.append(f"=== FILE: {r['path']}{truncated} ===\n{text}")
    return "\n\n".join(blocks), manifest, omitted


def run_ask(conn, cfg, ask) -> dict:
    evidence, manifest, omitted = _gather_evidence(conn, ask["scope"])
    user = (f"STANDING ASK: {ask['note']}\n"
            f"SCOPE: {ask['scope']}\n\n"
            f"EVIDENCE ({len(manifest)} files read in full, {omitted} more "
            f"files exist in scope but were not read):\n\n{evidence}")
    body = LLMClient(cfg).chat(WORK_PROMPT, user)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    slug = slugify(ask["note"].removeprefix("Standing ask:"))[:50]
    out_dir = cfg.data_dir / "outbox"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"WORK_{ask['id']:03d}_{slug}_{stamp}.md"
    header = [
        f"# Work product — [perceived] — ask #{ask['id']}",
        f"**Ask:** {ask['note']}",
        f"**Scope:** {ask['scope']} · **Generated:** {stamp} UTC · "
        f"**Model:** {cfg.llm_backend}:{cfg.llm_model}",
        f"**Evidence:** {len(manifest)} files read in full"
        + (f"; **{omitted} files in scope were NOT read** "
           "(selection: plan-shaped names first, then newest)" if omitted else ""),
        "",
        "---",
        "",
    ]
    footer = ["", "---", "", "## Evidence manifest"] + manifest
    path.write_text("\n".join(header) + body + "\n".join(footer) + "\n",
                    encoding="utf-8")
    return {"ask_id": ask["id"], "path": path, "files_read": len(manifest),
            "omitted": omitted}
