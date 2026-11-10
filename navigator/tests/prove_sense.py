# SPDX-License-Identifier: Apache-2.0
"""Proofs for the narration layer: stub LLM, sense-making + the feedback
loop, recommendations, wiki, and offline-safe web fetch."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixture import build, make_tmp  # noqa: E402
from navigator import db, depmap, indexer, recommend, sense, webfetch, wiki  # noqa: E402
from navigator.analyzers import get_registry, run_analyzer  # noqa: E402
from navigator.llm import LLMClient  # noqa: E402

PASS = 0
FAIL = 0


def check(label, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}  {detail}")


tmp = make_tmp()
try:
    cfg = build(tmp)
    conn = db.connect(cfg.db_path)
    indexer.index(conn, cfg)
    depmap.map_deps(conn)
    for a in get_registry().values():
        run_analyzer(conn, cfg, a)
    scope = f"{cfg.roots[0].name}/ToolA"

    # --- stub LLM ---
    client = LLMClient(cfg)
    out1 = client.chat("sys", "user prompt")
    out2 = client.chat("sys", "user prompt")
    check("llm: stub is deterministic", out1 == out2)
    check("llm: stub self-identifies", "[STUB:" in out1, out1)

    # --- evidence pack is real data, deterministically assembled ---
    ev = sense.build_evidence(conn, scope)
    check("evidence: lists real files", "ToolA/main.py" in ev)
    check("evidence: includes doc excerpt", "widget data" in ev)
    check("evidence: includes dep edges", "[import]" in ev)

    # --- summary lifecycle: perceived -> corrected -> regenerated -> confirmed ---
    s1 = sense.summarize(conn, cfg, scope)
    check("sense: new summary is 'perceived'", s1["status"] == "perceived")
    row = sense.get_summary(conn, scope)
    check("sense: stored with model tag", row["model"] == "stub:llama3", dict(row))

    sense.add_feedback(conn, scope, "ToolA actually serves the Phoenix project.")
    row = sense.get_summary(conn, scope)
    check("feedback: summary becomes 'corrected'", row["status"] == "corrected")
    ev2 = sense.build_evidence(conn, scope)
    check("feedback: durable and authoritative in evidence",
          "Phoenix" in ev2 and "authoritative" in ev2)

    s2 = sense.summarize(conn, cfg, scope)
    check("sense: regeneration resets to 'perceived'", s2["status"] == "perceived")
    check("sense: regeneration consumed the feedback", s2["body"] != s1["body"])
    notes = conn.execute("SELECT COUNT(*) AS n FROM feedback WHERE scope=?",
                         (scope,)).fetchone()["n"]
    check("feedback: survives regeneration", notes == 1)

    sense.confirm(conn, scope)
    row = sense.get_summary(conn, scope)
    check("sense: confirm marks human-verified", row["status"] == "confirmed")

    # --- the empty-scope gate (refuse to narrate with no evidence) ---
    try:
        sense.summarize(conn, cfg, "Nonexistent/Scope")
        check("sense: empty scope refused before any model call", False)
    except sense.NoEvidenceError as e:
        check("sense: empty scope refused before any model call",
              "No indexed files" in str(e), e)
    check("sense: refusal stores no summary",
          sense.get_summary(conn, "Nonexistent/Scope") is None)

    # --- recommendations (stub backend -> mechanical fallback) ---
    recs = recommend.generate(conn, cfg)
    check("recommend: produced from open findings", 1 <= len(recs) <= 5, recs)
    check("recommend: carries rationale", all(r["rationale"] for r in recs))
    digest = recommend.build_digest(conn)
    check("recommend: digest names analyzers", "missing_docs" in digest)
    check("recommend: digest carries standing asks/feedback",
          "STANDING ASKS" in digest and "Phoenix" in digest, digest)

    # --- wiki ---
    day = wiki.log_event(cfg.wiki_dir, "test", "first event")
    wiki.log_event(cfg.wiki_dir, "test", "second event")
    content = day.read_text(encoding="utf-8")
    check("wiki: daily log appends", content.count("test:") == 2, content)
    page = wiki.write_page(cfg.wiki_dir, "Reusable Process: Indexing!", "body text")
    check("wiki: page slugged", page.name == "reusable-process-indexing.md", page.name)

    # wiki becomes part of the index -> the app can search its own history
    indexer.index(conn, cfg)
    hits = db.search(conn, "reusable")
    check("wiki: self-indexed and searchable",
          any("pages" in h["path"] for h in hits), [dict(h) for h in hits])

    # --- web fetch: offline never crashes ---
    cfg.searx_url = ""
    result = webfetch.fetch(cfg, "http://127.0.0.1:1/unreachable", timeout=2)
    check("web: unreachable + no cache -> graceful error dict",
          result["status"] == 0 and "error" in result, result)
    check("web: no searx configured -> empty search",
          webfetch.search(cfg, "anything") == [])
    conn.close()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\nprove_sense: {PASS}/{PASS + FAIL}")
sys.exit(1 if FAIL else 0)
