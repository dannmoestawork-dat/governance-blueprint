# SPDX-License-Identifier: Apache-2.0
"""The dashboard: a clean, keyboard-driven TUI (works over plain SSH).

Left pane: the project tree's scopes with their dependency-role mix.
Right pane: tabs — Overview, Summary (with a feedback box), Findings,
Recommendations, Search. Long actions run in worker threads with their own
database connections, so the interface stays live while the navigator works.
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import (DataTable, Footer, Header, Input, Label,
                             ListItem, ListView, Static, TabbedContent, TabPane)

from . import db, depmap, indexer, recommend, sense, wiki
from .analyzers import get_registry, run_analyzer


class NavigatorApp(App):
    TITLE = "Navigator"
    CSS = """
    #scopes { width: 38%; border: solid $primary; }
    #main { width: 62%; }
    #summary_body { height: 1fr; border: solid $surface; padding: 0 1; }
    #overview { padding: 1 2; }
    Input { dock: bottom; }
    """
    BINDINGS = [
        Binding("i", "do_index", "Index"),
        Binding("m", "do_map", "Map deps"),
        Binding("a", "do_analyze", "Analyze"),
        Binding("s", "do_sense", "Summarize"),
        Binding("r", "do_recommend", "Recommend"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.selected_scope: str | None = None

    # ---------- layout ----------

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield ListView(id="scopes")
            with Vertical(id="main"):
                with TabbedContent():
                    with TabPane("Overview", id="tab_overview"):
                        yield Static(id="overview")
                    with TabPane("Summary", id="tab_summary"):
                        yield Static(id="summary_body")
                        yield Input(placeholder="Type a correction and press Enter "
                                                "(it becomes durable feedback)…",
                                    id="feedback_input")
                    with TabPane("Findings", id="tab_findings"):
                        yield DataTable(id="findings_table")
                    with TabPane("Recommendations", id="tab_recs"):
                        yield Static(id="recs_body")
                    with TabPane("Search", id="tab_search"):
                        yield DataTable(id="search_table")
                        yield Input(placeholder="Search the index…", id="search_input")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#findings_table", DataTable)
        table.add_columns("sev", "analyzer", "path", "message")
        st = self.query_one("#search_table", DataTable)
        st.add_columns("path", "match")
        self.refresh_all()

    # ---------- data refresh (main thread, quick queries only) ----------

    def _conn(self):
        return db.connect(self.cfg.db_path)

    def refresh_all(self) -> None:
        conn = self._conn()
        try:
            self._refresh_scopes(conn)
            self._refresh_overview(conn)
            self._refresh_findings(conn)
            self._refresh_recs(conn)
        finally:
            conn.close()

    def _refresh_scopes(self, conn) -> None:
        scopes: set[str] = set()
        for r in conn.execute("SELECT DISTINCT path FROM files"):
            parts = r["path"].split("/")
            if len(parts) >= 2:
                scopes.add("/".join(parts[:2]))
        lv = self.query_one("#scopes", ListView)
        lv.clear()
        for s in sorted(scopes):
            lv.append(ListItem(Label(s), name=s))

    def _refresh_overview(self, conn) -> None:
        n_files = conn.execute("SELECT COUNT(*) AS n FROM files").fetchone()["n"]
        n_edges = conn.execute("SELECT COUNT(*) AS n FROM deps").fetchone()["n"]
        n_open = conn.execute(
            "SELECT COUNT(*) AS n FROM findings WHERE status='open'").fetchone()["n"]
        last = conn.execute("SELECT value FROM meta WHERE key='last_index'").fetchone()
        runs = conn.execute(
            "SELECT analyzer, MAX(finished) AS t, findings FROM analyzer_runs "
            "GROUP BY analyzer").fetchall()
        lines = [
            f"[b]Files indexed:[/b] {n_files}",
            f"[b]Dependency edges:[/b] {n_edges}",
            f"[b]Open findings:[/b] {n_open}",
            f"[b]Last index:[/b] {last['value'] if last else 'never'}",
            "",
            "[b]Analyzer runs:[/b]",
        ]
        lines += [f"  {r['analyzer']}: {r['t']} ({r['findings']} findings)"
                  for r in runs] or ["  none yet — press 'a'"]
        lines += ["", "Keys: i=index  m=map  a=analyze  s=summarize  r=recommend  q=quit"]
        self.query_one("#overview", Static).update("\n".join(lines))

    def _refresh_findings(self, conn) -> None:
        table = self.query_one("#findings_table", DataTable)
        table.clear()
        for r in conn.execute(
                "SELECT severity, analyzer, path, message FROM findings "
                "WHERE status='open' ORDER BY "
                "CASE severity WHEN 'error' THEN 0 WHEN 'warn' THEN 1 ELSE 2 END "
                "LIMIT 500"):
            table.add_row(r["severity"], r["analyzer"], r["path"], r["message"])

    def _refresh_recs(self, conn) -> None:
        rows = conn.execute(
            "SELECT body, rationale, created FROM recommendations "
            "ORDER BY id DESC LIMIT 10").fetchall()
        text = "\n\n".join(
            f"[b]•[/b] {r['body']}\n  [dim]why: {r['rationale']}[/dim]" for r in rows
        ) or "No recommendations yet — press 'r'."
        self.query_one("#recs_body", Static).update(text)

    def _refresh_summary(self) -> None:
        if not self.selected_scope:
            return
        conn = self._conn()
        try:
            row = sense.get_summary(conn, self.selected_scope)
            notes = conn.execute(
                "SELECT note, created FROM feedback WHERE scope=? ORDER BY id",
                (self.selected_scope,)).fetchall()
        finally:
            conn.close()
        if row:
            text = (f"[b]{self.selected_scope}[/b]  "
                    f"[dim]status: {row['status']} · model: {row['model']}[/dim]\n\n"
                    f"{row['body']}")
        else:
            text = (f"[b]{self.selected_scope}[/b]\n\nNo summary yet — "
                    "press 's' to generate one.")
        if notes:
            text += "\n\n[b]Your feedback (durable):[/b]\n" + "\n".join(
                f"  • {n['note']}" for n in notes)
        self.query_one("#summary_body", Static).update(text)

    # ---------- events ----------

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.selected_scope = event.item.name
        self._refresh_summary()
        self.query_one(TabbedContent).active = "tab_summary"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        event.input.value = ""
        if not value:
            return
        if event.input.id == "feedback_input" and self.selected_scope:
            conn = self._conn()
            try:
                sense.add_feedback(conn, self.selected_scope, value)
            finally:
                conn.close()
            wiki.log_event(self.cfg.wiki_dir, "feedback",
                           f"{self.selected_scope}: {value}")
            self.notify("Feedback saved — it will shape future summaries.")
            self._refresh_summary()
        elif event.input.id == "search_input":
            conn = self._conn()
            try:
                rows = db.search(conn, value)
            except Exception:
                rows = []
            finally:
                conn.close()
            table = self.query_one("#search_table", DataTable)
            table.clear()
            for r in rows:
                table.add_row(r["path"], r["snip"])

    # ---------- actions (worker threads, own connections) ----------

    def action_do_index(self) -> None:
        self.notify("Indexing…")
        self.run_worker(self._work_index, thread=True, exclusive=True)

    def _work_index(self) -> None:
        conn = self._conn()
        try:
            stats = indexer.index(conn, self.cfg)
        finally:
            conn.close()
        wiki.log_event(self.cfg.wiki_dir, "index", str(stats))
        self.call_from_thread(self.notify, f"Index done: {stats}")
        self.call_from_thread(self.refresh_all)

    def action_do_map(self) -> None:
        self.notify("Mapping dependencies…")
        self.run_worker(self._work_map, thread=True, exclusive=True)

    def _work_map(self) -> None:
        conn = self._conn()
        try:
            stats = depmap.map_deps(conn)
        finally:
            conn.close()
        wiki.log_event(self.cfg.wiki_dir, "map", str(stats))
        self.call_from_thread(self.notify, f"Map done: {stats['edges']} edges")
        self.call_from_thread(self.refresh_all)

    def action_do_analyze(self) -> None:
        self.notify("Running all analyzers…")
        self.run_worker(self._work_analyze, thread=True, exclusive=True)

    def _work_analyze(self) -> None:
        conn = self._conn()
        try:
            for analyzer in get_registry().values():
                result = run_analyzer(conn, self.cfg, analyzer)
                wiki.log_event(self.cfg.wiki_dir, "analyze", str(result))
        finally:
            conn.close()
        self.call_from_thread(self.notify, "Analyzers done.")
        self.call_from_thread(self.refresh_all)

    def action_do_sense(self) -> None:
        if not self.selected_scope:
            self.notify("Select a scope on the left first.", severity="warning")
            return
        self.notify(f"Summarizing {self.selected_scope}…")
        self.run_worker(self._work_sense, thread=True, exclusive=True)

    def _work_sense(self) -> None:
        conn = self._conn()
        try:
            sense.summarize(conn, self.cfg, self.selected_scope)
        except sense.NoEvidenceError as e:
            self.call_from_thread(self.notify, str(e), severity="warning")
            return
        finally:
            conn.close()
        wiki.log_event(self.cfg.wiki_dir, "sense", f"summarized {self.selected_scope}")
        self.call_from_thread(self.notify, "Summary updated.")
        self.call_from_thread(self._refresh_summary)

    def action_do_recommend(self) -> None:
        self.notify("Generating recommendations…")
        self.run_worker(self._work_recommend, thread=True, exclusive=True)

    def _work_recommend(self) -> None:
        conn = self._conn()
        try:
            recs = recommend.generate(conn, self.cfg)
        finally:
            conn.close()
        wiki.log_event(self.cfg.wiki_dir, "recommend", f"{len(recs)} recommendations")
        self.call_from_thread(self.notify, f"{len(recs)} recommendations ready.")
        self.call_from_thread(self.refresh_all)
