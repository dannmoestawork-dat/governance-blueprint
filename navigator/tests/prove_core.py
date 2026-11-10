# SPDX-License-Identifier: Apache-2.0
"""Proofs for the mechanical core: config, db, indexer, search, depmap,
analyzers. Prints PASS/FAIL per check and a final count."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixture import build, make_tmp  # noqa: E402
from navigator import db, depmap, indexer  # noqa: E402
from navigator.analyzers import get_registry, run_analyzer  # noqa: E402
from navigator.config import load_config  # noqa: E402

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
    # --- config ---
    cfg_file = tmp / "config.toml"
    cfg_file.write_text(
        f'[index]\nroots = ["{(tmp / "fixture").as_posix()}"]\n'
        '[data]\ndir = "navdata"\n[llm]\nbackend = "stub"\n')
    (tmp / "fixture").mkdir()
    loaded = load_config(cfg_file)
    check("config: root parsed absolute", loaded.roots[0] == tmp / "fixture")
    check("config: relative data dir resolves beside config",
          loaded.data_dir == tmp / "navdata")
    check("config: stub default backend", loaded.llm_backend == "stub")
    shutil.rmtree(tmp / "fixture")

    # --- indexer ---
    cfg = build(tmp)
    conn = db.connect(cfg.db_path)
    stats = indexer.index(conn, cfg)
    check("index: 9 files scanned", stats["scanned"] == 9, stats)
    check("index: all new on first run", stats["updated"] == 9, stats)
    row = conn.execute("SELECT kind FROM files WHERE path LIKE '%binary.bin'").fetchone()
    check("index: binary file metadata-only", row and row["kind"] == "binary")
    row = conn.execute("SELECT kind FROM files WHERE path LIKE '%main.py'").fetchone()
    check("index: py file is text", row and row["kind"] == "text")

    hits = db.search(conn, "widget")
    check("search: FTS finds doc content",
          len(hits) == 1 and hits[0]["path"].endswith("MAINTENANCE_LOG.md"), hits)

    stats2 = indexer.index(conn, cfg)
    check("index: incremental rerun touches nothing",
          stats2["updated"] == 0 and stats2["unchanged"] == 9, stats2)

    (cfg.roots[0] / "ToolB" / "standalone.py").rename(tmp / "parked.py")
    stats3 = indexer.index(conn, cfg)
    check("index: vanished file removed", stats3["removed"] == 1, stats3)
    (tmp / "parked.py").rename(cfg.roots[0] / "ToolB" / "standalone.py")
    indexer.index(conn, cfg)

    # --- depmap ---
    dstats = depmap.map_deps(conn)
    edges = {(r["src"].rsplit("/", 1)[-1], r["dst"].rsplit("/", 1)[-1], r["kind"])
             for r in conn.execute("SELECT * FROM deps")}
    check("depmap: import edge main->helper",
          ("main.py", "helper.py", "import") in edges, edges)
    check("depmap: path edge main->output.json",
          ("main.py", "output.json", "path") in edges, edges)
    check("depmap: run edge main->run_me.py",
          ("main.py", "run_me.py", "run") in edges, edges)

    roles = {k.rsplit("/", 1)[-1]: v for k, v in depmap.roles(conn).items()}
    check("roles: helper is root", roles.get("helper.py") == "root", roles)
    check("roles: main is dependent", roles.get("main.py") == "dependent", roles)
    check("roles: standalone is self-contained",
          roles.get("standalone.py") == "self-contained", roles)
    check("roles: run_me is root", roles.get("run_me.py") == "root", roles)

    # --- analyzers ---
    registry = get_registry()
    check("analyzers: 3 registered", len(registry) == 3, list(registry))
    results = {name: run_analyzer(conn, cfg, a) for name, a in registry.items()}
    check("analyzers: all ran ok",
          all(r["status"] == "ok" for r in results.values()), results)

    f = conn.execute("SELECT path, message FROM findings WHERE analyzer='missing_docs'").fetchall()
    flagged = {r["path"].rsplit("/", 1)[-1] for r in f}
    check("missing_docs: ToolB flagged", "ToolB" in flagged, flagged)
    check("missing_docs: sub flagged", "sub" in flagged, flagged)
    check("missing_docs: ToolA not flagged (has log)", "ToolA" not in flagged, flagged)

    f = conn.execute("SELECT message FROM findings WHERE analyzer='broken_refs'").fetchall()
    msgs = [r["message"] for r in f]
    check("broken_refs: gone.csv flagged",
          any("gone.csv" in m for m in msgs), msgs)
    check("broken_refs: existing refs not flagged",
          not any("output.json" in m or "real.txt" in m for m in msgs), msgs)

    f = conn.execute("SELECT path, message FROM findings WHERE analyzer='doc_drift'").fetchall()
    check("doc_drift: ToolA docs lag flagged",
          len(f) == 1 and f[0]["path"].endswith("ToolA") and "older" in f[0]["message"], f)

    before = conn.execute("SELECT COUNT(*) AS n FROM findings").fetchone()["n"]
    rerun = {name: run_analyzer(conn, cfg, a) for name, a in registry.items()}
    after = conn.execute("SELECT COUNT(*) AS n FROM findings").fetchone()["n"]
    check("findings: rerun dedupes (0 new)",
          before == after and all(r["new"] == 0 for r in rerun.values()))

    runs = conn.execute("SELECT COUNT(*) AS n FROM analyzer_runs").fetchone()["n"]
    check("runs: every run recorded", runs == 6, runs)
    conn.close()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\nprove_core: {PASS}/{PASS + FAIL}")
sys.exit(1 if FAIL else 0)
