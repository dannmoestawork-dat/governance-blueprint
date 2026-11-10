# SPDX-License-Identifier: Apache-2.0
"""Tool dependency mapper.

Mechanically extracts edges between scripts in the indexed tree:
  - kind 'import'  : Python imports resolved to in-tree modules
  - kind 'path'    : string literals that point at in-tree files
  - kind 'run'     : script names invoked via subprocess-style strings

From the edges, each tool gets a role:
  - 'root'           : other tools depend on it, it depends on nothing in-tree
  - 'dependent'      : it depends on in-tree tools
  - 'hub'            : both (mid-chain)
  - 'self-contained' : no edges either way

All extraction is conservative and deterministic — no model involved.
"""

from __future__ import annotations

import ast
import re
import warnings

SCRIPT_EXTS = {".py", ".sh", ".ps1", ".bat"}

# String literals that look like file paths with a known extension.
_PATH_LIT = re.compile(
    r"""["']([A-Za-z0-9_][A-Za-z0-9_ ./\\-]{2,200}\.(?:py|md|json|csv|xlsx|toml|yaml|yml|txt|db|sh|ps1))["']"""
)
# Script invocations inside strings: "python foo.py", "bash run.sh", etc.
_RUN_LIT = re.compile(r"(?:python3?|bash|sh|pwsh|powershell)[^\"'\n]{0,80}?([A-Za-z0-9_./\\-]+\.(?:py|sh|ps1))")


def _py_imports(source: str) -> set[str]:
    try:
        with warnings.catch_warnings():
            # indexed third-party scripts often carry sloppy escapes; their
            # SyntaxWarnings are not ours to surface
            warnings.simplefilter("ignore")
            tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def _texts(conn):
    """All indexed text files as {path_key: content}."""
    rows = conn.execute(
        "SELECT f.path AS path, files_fts.content AS content "
        "FROM files_fts JOIN files f ON f.id = files_fts.rowid "
        "WHERE f.kind='text'").fetchall()
    return {r["path"]: r["content"] for r in rows}


def _resolve_relative(src_key: str, candidate: str, all_keys: set[str]) -> str | None:
    """Resolve a path-ish literal against the source file's directory, then
    against each root label. Returns the matching DB key or None."""
    cand = candidate.replace("\\", "/").lstrip("./")
    src_dir = src_key.rsplit("/", 1)[0] if "/" in src_key else ""
    for guess in (f"{src_dir}/{cand}" if src_dir else cand, cand):
        if guess in all_keys:
            return guess
    # last resort: unique basename match
    base = cand.rsplit("/", 1)[-1]
    matches = [k for k in all_keys if k.endswith("/" + base)]
    return matches[0] if len(matches) == 1 else None


def map_deps(conn) -> dict:
    texts = _texts(conn)
    all_keys = set(texts)
    all_keys.update(r["path"] for r in conn.execute("SELECT path FROM files"))

    # module name -> candidate .py keys (for import resolution)
    py_by_stem: dict[str, list[str]] = {}
    for key in all_keys:
        if key.endswith(".py"):
            stem = key.rsplit("/", 1)[-1][:-3]
            py_by_stem.setdefault(stem, []).append(key)

    edges: set[tuple[str, str, str]] = set()
    for src, content in texts.items():
        ext = "." + src.rsplit(".", 1)[-1] if "." in src else ""
        if ext == ".py":
            src_dir = src.rsplit("/", 1)[0]
            for mod in _py_imports(content):
                cands = py_by_stem.get(mod, [])
                same_dir = [c for c in cands if c.rsplit("/", 1)[0] == src_dir]
                target = same_dir[0] if same_dir else (cands[0] if len(cands) == 1 else None)
                if target and target != src:
                    edges.add((src, target, "import"))
        if ext in {".py", ".sh", ".ps1", ".bat", ".md"}:
            for m in _PATH_LIT.finditer(content):
                target = _resolve_relative(src, m.group(1), all_keys)
                if target and target != src:
                    edges.add((src, target, "path"))
            for m in _RUN_LIT.finditer(content):
                target = _resolve_relative(src, m.group(1), all_keys)
                if target and target != src:
                    edges.add((src, target, "run"))

    conn.execute("DELETE FROM deps")
    conn.executemany("INSERT OR IGNORE INTO deps(src, dst, kind) VALUES(?,?,?)",
                     sorted(edges))
    conn.commit()
    return {"edges": len(edges)}


def roles(conn) -> dict[str, str]:
    """Role per script file, derived from edges between scripts only."""
    scripts = {r["path"] for r in conn.execute("SELECT path FROM files")
               if "." + r["path"].rsplit(".", 1)[-1] in SCRIPT_EXTS}
    out_deg: dict[str, int] = {}
    in_deg: dict[str, int] = {}
    for r in conn.execute("SELECT src, dst FROM deps"):
        if r["src"] in scripts and r["dst"] in scripts:
            out_deg[r["src"]] = out_deg.get(r["src"], 0) + 1
            in_deg[r["dst"]] = in_deg.get(r["dst"], 0) + 1
    result = {}
    for s in scripts:
        has_out, has_in = s in out_deg, s in in_deg
        if has_out and has_in:
            result[s] = "hub"
        elif has_out:
            result[s] = "dependent"
        elif has_in:
            result[s] = "root"
        else:
            result[s] = "self-contained"
    return result
