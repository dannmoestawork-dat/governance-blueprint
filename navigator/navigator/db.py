# SPDX-License-Identifier: Apache-2.0
"""SQLite storage. One portable file holds the index, the dependency graph,
analyzer runs and findings, summaries + user feedback, and recommendations.

Paths are stored POSIX-style relative to their index root, as "root_label/rel"
(root_label = the root directory's name), so the database stays valid when the
tree is mirrored between machines.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS files(
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    ext TEXT,
    size INTEGER,
    mtime REAL,
    kind TEXT,
    indexed_at TEXT
);
CREATE VIRTUAL TABLE IF NOT EXISTS files_fts USING fts5(path, content);
CREATE TABLE IF NOT EXISTS deps(
    src TEXT NOT NULL,
    dst TEXT NOT NULL,
    kind TEXT NOT NULL,
    UNIQUE(src, dst, kind)
);
CREATE TABLE IF NOT EXISTS analyzer_runs(
    id INTEGER PRIMARY KEY,
    analyzer TEXT NOT NULL,
    started TEXT,
    finished TEXT,
    status TEXT,
    findings INTEGER
);
CREATE TABLE IF NOT EXISTS findings(
    id INTEGER PRIMARY KEY,
    run_id INTEGER,
    analyzer TEXT NOT NULL,
    severity TEXT NOT NULL,
    path TEXT,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    UNIQUE(analyzer, path, message)
);
CREATE TABLE IF NOT EXISTS summaries(
    id INTEGER PRIMARY KEY,
    scope TEXT UNIQUE NOT NULL,
    body TEXT,
    status TEXT NOT NULL DEFAULT 'perceived',
    model TEXT,
    created TEXT,
    updated TEXT
);
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY,
    scope TEXT NOT NULL,
    note TEXT NOT NULL,
    created TEXT
);
CREATE TABLE IF NOT EXISTS recommendations(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    rationale TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    created TEXT
);
CREATE TABLE IF NOT EXISTS meta(
    key TEXT PRIMARY KEY,
    value TEXT
);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    return conn


def upsert_file(conn, path: str, ext: str, size: int, mtime: float,
                kind: str, content: str) -> None:
    row = conn.execute("SELECT id FROM files WHERE path=?", (path,)).fetchone()
    if row:
        fid = row["id"]
        conn.execute(
            "UPDATE files SET ext=?, size=?, mtime=?, kind=?, indexed_at=? WHERE id=?",
            (ext, size, mtime, kind, utcnow(), fid))
        conn.execute("DELETE FROM files_fts WHERE rowid=?", (fid,))
    else:
        cur = conn.execute(
            "INSERT INTO files(path, ext, size, mtime, kind, indexed_at) VALUES(?,?,?,?,?,?)",
            (path, ext, size, mtime, kind, utcnow()))
        fid = cur.lastrowid
    conn.execute("INSERT INTO files_fts(rowid, path, content) VALUES(?,?,?)",
                 (fid, path, content))


def remove_files(conn, paths: list[str]) -> None:
    for p in paths:
        row = conn.execute("SELECT id FROM files WHERE path=?", (p,)).fetchone()
        if row:
            conn.execute("DELETE FROM files_fts WHERE rowid=?", (row["id"],))
            conn.execute("DELETE FROM files WHERE id=?", (row["id"],))


def search(conn, query: str, limit: int = 25) -> list[sqlite3.Row]:
    return conn.execute(
        """SELECT f.path, f.ext, f.size,
                  snippet(files_fts, 1, '[', ']', ' … ', 12) AS snip
           FROM files_fts JOIN files f ON f.id = files_fts.rowid
           WHERE files_fts MATCH ? ORDER BY rank LIMIT ?""",
        (query, limit)).fetchall()
