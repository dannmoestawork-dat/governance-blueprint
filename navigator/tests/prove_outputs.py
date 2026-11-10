# SPDX-License-Identifier: Apache-2.0
"""Proofs for the manager layer: findings report, memory report, work
orders (delegate), and the ask executor (work)."""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixture import build, make_tmp  # noqa: E402
from navigator import db, delegate, depmap, indexer, report, sense, work  # noqa: E402
from navigator.analyzers import get_registry, run_analyzer  # noqa: E402

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
    sense.summarize(conn, cfg, scope)
    sense.add_feedback(conn, scope, "ToolA serves the Phoenix project.")

    # --- findings report ---
    p1 = report.write_report(conn, cfg)
    text = p1.read_text(encoding="utf-8")
    check("report: file written to outbox", p1.is_file() and "outbox" in str(p1))
    check("report: carries counts", "Files indexed:" in text and "missing_docs" in text)
    check("report: lists summary statuses", "[corrected]" in text, text)
    p2 = report.write_report(conn, cfg)
    check("report: second run shows delta",
          "Change since last report" in p2.read_text(encoding="utf-8"))

    # --- memory report ---
    pm = report.write_memory_report(conn, cfg)
    mtext = pm.read_text(encoding="utf-8")
    check("memory: believes + taught sections present",
          "What it believes" in mtext and "Phoenix" in mtext)
    check("memory: analyzer history present", "missing_docs:" in mtext, mtext)

    # --- delegate (work orders) ---
    paths = delegate.write_work_orders(conn, cfg)
    names = [p.name for p in paths]
    md = next(p for p in paths if "missing_docs" in p.name and p.suffix == ".md")
    dtext = md.read_text(encoding="utf-8")
    check("delegate: missing_docs order written", "WORK ORDER" in dtext)
    check("delegate: house log sections included",
          "Error Log" in dtext and "Session Handoff Notes" in dtext)
    check("delegate: targets listed", "ToolB" in dtext, dtext)
    check("delegate: never instructs tree edits by Navigator itself",
          "for execution by an agent" in dtext)
    mf = next(p for p in paths if p.suffix == ".json")
    data = json.loads(mf.read_text(encoding="utf-8"))
    check("delegate: JSON manifest parses with targets",
          data["task"] == "create_missing_docs" and len(data["targets"]) >= 2, data)

    # --- work (ask executor) ---
    sense.add_feedback(conn, scope, "Standing ask: write a one-page memo on ToolA's data flow.")
    asks = work.list_asks(conn)
    check("work: only Standing ask notes are asks", len(asks) == 1, [dict(a) for a in asks])
    result = work.run_ask(conn, cfg, asks[0])
    wtext = result["path"].read_text(encoding="utf-8")
    check("work: artifact written to outbox", result["path"].is_file())
    check("work: labeled perceived with the ask restated",
          "[perceived]" in wtext and "one-page memo" in wtext)
    check("work: evidence manifest lists real files",
          "Evidence manifest" in wtext and "ToolA/main.py" in wtext, wtext)
    check("work: stub model output embedded", "[STUB:" in wtext)

    bogus = {"id": 99, "scope": "Nope/Nothing", "note": "Standing ask: x", "created": ""}
    try:
        work.run_ask(conn, cfg, bogus)
        check("work: empty scope refused", False)
    except sense.NoEvidenceError:
        check("work: empty scope refused", True)
    conn.close()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\nprove_outputs: {PASS}/{PASS + FAIL}")
sys.exit(1 if FAIL else 0)
