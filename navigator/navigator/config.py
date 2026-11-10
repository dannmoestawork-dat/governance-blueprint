# SPDX-License-Identifier: Apache-2.0
"""Configuration loading.

A config is a TOML file (see config.example.toml). Relative data paths
resolve against the config file's directory so a cloned repo is fully
self-contained and portable.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_EXCLUDE_DIRS = [
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    ".obsidian", "dist", "build", ".pytest_cache", "_archive",
]
DEFAULT_TEXT_EXTS = [
    ".py", ".md", ".txt", ".toml", ".json", ".yaml", ".yml", ".csv",
    ".sh", ".ps1", ".bat", ".html", ".css", ".js", ".sql", ".ini", ".cfg",
]


@dataclass
class Config:
    roots: list[Path]
    exclude_dirs: list[str] = field(default_factory=lambda: list(DEFAULT_EXCLUDE_DIRS))
    exclude_globs: list[str] = field(default_factory=list)
    text_exts: list[str] = field(default_factory=lambda: list(DEFAULT_TEXT_EXTS))
    max_text_bytes: int = 400_000
    data_dir: Path = Path("data")
    llm_backend: str = "stub"
    llm_url: str = "http://localhost:11434"
    llm_model: str = "llama3"
    llm_timeout: int = 120
    required_docs: list[str] = field(default_factory=lambda: ["MAINTENANCE_LOG.md"])
    drift_days: int = 30
    searx_url: str = ""
    web_cache_dir: Path = Path("data/webcache")

    @property
    def db_path(self) -> Path:
        return self.data_dir / "navigator.db"

    @property
    def wiki_dir(self) -> Path:
        return self.data_dir / "wiki"


def find_config(explicit: str | None = None) -> Path | None:
    """Locate config.toml: explicit path, cwd, or the package's repo dir."""
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    candidates.append(Path.cwd() / "config.toml")
    candidates.append(Path(__file__).resolve().parent.parent / "config.toml")
    for c in candidates:
        if c.is_file():
            return c
    return None


def load_config(path: Path) -> Config:
    base = path.resolve().parent
    with open(path, "rb") as f:
        raw = tomllib.load(f)

    idx = raw.get("index", {})
    data = raw.get("data", {})
    llm = raw.get("llm", {})
    an = raw.get("analyzers", {})
    web = raw.get("web", {})

    def respath(value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else base / p

    roots = [respath(r) for r in idx.get("roots", [])]
    if not roots:
        raise ValueError(f"{path}: [index].roots must list at least one directory")

    return Config(
        roots=roots,
        exclude_dirs=idx.get("exclude_dirs", list(DEFAULT_EXCLUDE_DIRS)),
        exclude_globs=idx.get("exclude_globs", []),
        text_exts=idx.get("text_exts", list(DEFAULT_TEXT_EXTS)),
        max_text_bytes=idx.get("max_text_bytes", 400_000),
        data_dir=respath(data.get("dir", "data")),
        llm_backend=llm.get("backend", "stub"),
        llm_url=llm.get("url", "http://localhost:11434"),
        llm_model=llm.get("model", "llama3"),
        llm_timeout=llm.get("timeout_seconds", 120),
        required_docs=an.get("required_docs", ["MAINTENANCE_LOG.md"]),
        drift_days=an.get("drift_days", 30),
        searx_url=web.get("searx_url", ""),
        web_cache_dir=respath(web.get("cache_dir", "data/webcache")),
    )
