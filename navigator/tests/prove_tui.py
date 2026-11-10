# SPDX-License-Identifier: Apache-2.0
"""Headless smoke proof for the dashboard: mounts the real app against a
real (fixture) database via Textual's test pilot — no terminal needed."""

import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixture import build, make_tmp  # noqa: E402
from navigator import db, depmap, indexer, sense  # noqa: E402
from navigator.analyzers import get_registry, run_analyzer  # noqa: E402
from navigator.app import NavigatorApp  # noqa: E402
from textual.widgets import DataTable, ListView, Static  # noqa: E402

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


async def main(cfg, scope):
    app = NavigatorApp(cfg)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        scopes = app.query_one("#scopes", ListView)
        names = {item.name for item in scopes.children}
        check("tui: scope list populated", f"{cfg.roots[0].name}/ToolA" in names, names)

        overview = app.query_one("#overview", Static)
        text = str(overview.render())
        check("tui: overview shows file count", "Files indexed:" in text, text)
        check("tui: overview shows analyzer runs", "missing_docs" in text, text)

        table = app.query_one("#findings_table", DataTable)
        check("tui: findings table populated", table.row_count >= 3, table.row_count)

        app.selected_scope = scope
        app._refresh_summary()
        body = str(app.query_one("#summary_body", Static).render())
        check("tui: summary pane renders stored summary", "[STUB:" in body, body)

        await pilot.press("q")


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
    conn.close()
    asyncio.run(main(cfg, scope))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\nprove_tui: {PASS}/{PASS + FAIL}")
sys.exit(1 if FAIL else 0)
