# SPDX-License-Identifier: Apache-2.0
"""Command line interface.

    navigator init                     write a starter config.toml
    navigator index                    index the configured roots
    navigator map                      rebuild the dependency map
    navigator analyze [name]           run one or all gap analyzers
    navigator sense <scope>            (re)generate a plain-language summary
    navigator feedback <scope> <note>  correct/refine a summary (durable)
    navigator confirm <scope>          mark a summary human-confirmed
    navigator recommend                generate next-step recommendations
    navigator search <query>           full-text search the index
    navigator status                   one-screen text status
    navigator dash                     open the dashboard (TUI)
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import db, delegate, depmap, indexer, recommend, report, sense, wiki, work
from .analyzers import get_registry, run_analyzer
from .config import find_config, load_config


def _ctx(args):
    cfg_path = find_config(getattr(args, "config", None))
    if not cfg_path:
        sys.exit("No config.toml found. Run `navigator init` first "
                 "(or pass --config PATH).")
    cfg = load_config(cfg_path)
    conn = db.connect(cfg.db_path)
    return cfg, conn


def cmd_init(args):
    target = Path.cwd() / "config.toml"
    if target.exists():
        sys.exit(f"{target} already exists — edit it instead.")
    example = Path(__file__).resolve().parent.parent / "config.example.toml"
    shutil.copy(example, target)
    print(f"Wrote {target}. Edit [index].roots, then run `navigator index`.")


def cmd_index(args):
    cfg, conn = _ctx(args)
    print(f"Indexing {len(cfg.roots)} root(s)…")
    stats = indexer.index(conn, cfg,
                          progress=lambda s: print(f"  …{s['updated']} files updated"))
    print(f"Done: {stats['scanned']} scanned, {stats['updated']} added/updated, "
          f"{stats['unchanged']} unchanged, {stats['removed']} removed.")
    wiki.log_event(cfg.wiki_dir, "index", str(stats))


def cmd_map(args):
    cfg, conn = _ctx(args)
    stats = depmap.map_deps(conn)
    role_counts: dict[str, int] = {}
    for v in depmap.roles(conn).values():
        role_counts[v] = role_counts.get(v, 0) + 1
    print(f"Dependency map: {stats['edges']} edges. Roles: {role_counts}")
    wiki.log_event(cfg.wiki_dir, "map", f"{stats['edges']} edges, roles {role_counts}")


def cmd_analyze(args):
    cfg, conn = _ctx(args)
    registry = get_registry()
    names = [args.name] if args.name else list(registry)
    for name in names:
        if name not in registry:
            sys.exit(f"Unknown analyzer '{name}'. Available: {', '.join(registry)}")
        result = run_analyzer(conn, cfg, registry[name])
        print(f"{name}: {result['status']}, {result['findings']} findings "
              f"({result['new']} new)")
        wiki.log_event(cfg.wiki_dir, "analyze", str(result))


def cmd_sense(args):
    cfg, conn = _ctx(args)
    try:
        result = sense.summarize(conn, cfg, args.scope)
    except sense.NoEvidenceError as e:
        sys.exit(f"STOPPED — {e}")
    print(f"[{result['status']}] {args.scope}\n\n{result['body']}")
    wiki.log_event(cfg.wiki_dir, "sense", f"summarized {args.scope}")


def cmd_feedback(args):
    cfg, conn = _ctx(args)
    sense.add_feedback(conn, args.scope, args.note)
    print(f"Feedback recorded for {args.scope}. It will shape every future "
          "summary of this scope.")
    wiki.log_event(cfg.wiki_dir, "feedback", f"{args.scope}: {args.note}")


def cmd_confirm(args):
    cfg, conn = _ctx(args)
    sense.confirm(conn, args.scope)
    print(f"Summary for {args.scope} marked confirmed.")
    wiki.log_event(cfg.wiki_dir, "confirm", args.scope)


def cmd_recommend(args):
    cfg, conn = _ctx(args)
    recs = recommend.generate(conn, cfg)
    if not recs:
        sys.exit("No recommendations — there are no open findings yet. "
                 "Run `navigator index`, `navigator map`, `navigator analyze` first.")
    for i, r in enumerate(recs, 1):
        print(f"{i}. {r['body']}\n   why: {r['rationale']}")
    wiki.log_event(cfg.wiki_dir, "recommend", f"{len(recs)} recommendations")


def cmd_search(args):
    cfg, conn = _ctx(args)
    for row in db.search(conn, args.query):
        print(f"{row['path']}\n    {row['snip']}")


def cmd_status(args):
    cfg, conn = _ctx(args)
    n_files = conn.execute("SELECT COUNT(*) AS n FROM files").fetchone()["n"]
    n_edges = conn.execute("SELECT COUNT(*) AS n FROM deps").fetchone()["n"]
    n_open = conn.execute(
        "SELECT COUNT(*) AS n FROM findings WHERE status='open'").fetchone()["n"]
    last = conn.execute(
        "SELECT value FROM meta WHERE key='last_index'").fetchone()
    print(f"files indexed : {n_files}")
    print(f"dep edges     : {n_edges}")
    print(f"open findings : {n_open}")
    print(f"last index    : {last['value'] if last else 'never'}")
    for r in conn.execute(
            "SELECT analyzer, MAX(finished) AS t, findings FROM analyzer_runs "
            "GROUP BY analyzer"):
        print(f"  analyzer {r['analyzer']}: last run {r['t']}, {r['findings']} findings")


def cmd_report(args):
    cfg, conn = _ctx(args)
    path = report.write_report(conn, cfg)
    print(f"Findings report written:\n  {path}")
    wiki.log_event(cfg.wiki_dir, "report", str(path))


def cmd_memory(args):
    cfg, conn = _ctx(args)
    path = report.write_memory_report(conn, cfg)
    print(f"Memory report written:\n  {path}")
    wiki.log_event(cfg.wiki_dir, "memory", str(path))


def cmd_delegate(args):
    cfg, conn = _ctx(args)
    paths = delegate.write_work_orders(conn, cfg)
    if not paths:
        sys.exit("No open findings — nothing to delegate. "
                 "Run `navigator analyze` first.")
    print(f"{len(paths)} work-order file(s) written:")
    for p in paths:
        print(f"  {p}")
    wiki.log_event(cfg.wiki_dir, "delegate", f"{len(paths)} work orders")


def cmd_work(args):
    cfg, conn = _ctx(args)
    asks = work.list_asks(conn)
    if not asks:
        sys.exit("No standing asks found. Record one with:\n"
                 '  navigator feedback <scope> "Standing ask: ..."')
    if args.ask_id:
        asks = [a for a in asks if a["id"] == args.ask_id]
        if not asks:
            sys.exit(f"No standing ask with id {args.ask_id}. "
                     "Run `navigator work --list` to see them.")
    if args.list:
        for a in asks:
            print(f"  #{a['id']}  [{a['scope']}]  {a['note']}")
        return
    for a in asks:
        print(f"Working ask #{a['id']} ({a['scope']})…")
        try:
            result = work.run_ask(conn, cfg, a)
        except sense.NoEvidenceError as e:
            print(f"  SKIPPED — {e}")
            continue
        print(f"  -> {result['path']}  ({result['files_read']} files read"
              + (f", {result['omitted']} omitted" if result['omitted'] else "") + ")")
        wiki.log_event(cfg.wiki_dir, "work",
                       f"ask #{a['id']} -> {result['path'].name}")


def cmd_dash(args):
    cfg, conn = _ctx(args)
    conn.close()  # the app opens its own connection per worker thread
    from .app import NavigatorApp
    NavigatorApp(cfg).run()


def main(argv=None):
    p = argparse.ArgumentParser(prog="navigator",
                                description="Navigator — sense-making dashboard")
    p.add_argument("--config", help="path to config.toml")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    sub.add_parser("map").set_defaults(fn=cmd_map)
    a = sub.add_parser("analyze")
    a.add_argument("name", nargs="?")
    a.set_defaults(fn=cmd_analyze)
    s = sub.add_parser("sense")
    s.add_argument("scope")
    s.set_defaults(fn=cmd_sense)
    f = sub.add_parser("feedback")
    f.add_argument("scope")
    f.add_argument("note")
    f.set_defaults(fn=cmd_feedback)
    c = sub.add_parser("confirm")
    c.add_argument("scope")
    c.set_defaults(fn=cmd_confirm)
    sub.add_parser("recommend").set_defaults(fn=cmd_recommend)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    sub.add_parser("memory").set_defaults(fn=cmd_memory)
    sub.add_parser("delegate").set_defaults(fn=cmd_delegate)
    w = sub.add_parser("work")
    w.add_argument("ask_id", nargs="?", type=int)
    w.add_argument("--list", action="store_true")
    w.set_defaults(fn=cmd_work)
    q = sub.add_parser("search")
    q.add_argument("query")
    q.set_defaults(fn=cmd_search)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("dash").set_defaults(fn=cmd_dash)

    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
