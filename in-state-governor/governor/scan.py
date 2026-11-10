# SPDX-License-Identifier: Apache-2.0
"""Walk a target tree, run enabled rules, collect findings."""

from __future__ import annotations

import os

from .config import Config
from .rules import Finding, ScanContext, ScannedFile, run_rule

# Directories we never descend into.
DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
}

# Only files with these extensions are read into the scan set. Keeping this
# small avoids trying to decode binaries; rules glob within this set.
TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".toml", ".cfg", ".ini", ".rst"}


def build_context(root: str, *, extensions: set[str] | None = None) -> ScanContext:
    """Read every eligible text file under ``root`` into a :class:`ScanContext`."""
    root = os.path.abspath(root)
    exts = extensions if extensions is not None else TEXT_EXTENSIONS
    files: list[ScannedFile] = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE_DIRS]
        for name in sorted(filenames):
            ext = os.path.splitext(name)[1].lower()
            if exts and ext not in exts:
                continue
            abspath = os.path.join(dirpath, name)
            try:
                with open(abspath, "r", encoding="utf-8") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            rel = os.path.relpath(abspath, root).replace(os.sep, "/")
            files.append(ScannedFile(abspath=abspath, relpath=rel, text=text))

    files.sort(key=lambda f: f.relpath)
    return ScanContext(root=root, files=files)


def scan(root: str, config: Config, *, extensions: set[str] | None = None) -> list[Finding]:
    """Run all enabled rules against ``root`` and return all findings, sorted."""
    ctx = build_context(root, extensions=extensions)
    findings: list[Finding] = []
    for rule_cfg in config.rules:
        findings.extend(run_rule(rule_cfg.rule_id, ctx, rule_cfg.params))

    severity_order = {"error": 0, "warning": 1, "info": 2}
    findings.sort(
        key=lambda f: (
            severity_order.get(f.severity, 99),
            f.rule_id,
            f.path,
            f.line,
        )
    )
    return findings
