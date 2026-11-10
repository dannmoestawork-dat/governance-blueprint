# SPDX-License-Identifier: Apache-2.0
"""Deterministic governance rules.

Each rule is a self-contained function that receives a :class:`ScanContext`
(the full set of scanned files plus the rule's own parameters) and returns a
list of :class:`Finding`. No rule calls a network service or a model; every
result is reproducible from the files on disk and the config. That determinism
is the point: a check you can trust is one that cannot rationalize its way
past a violation.

A rule function signature is::

    def rule(ctx: ScanContext, params: dict) -> list[Finding]

Rules are registered in the :data:`RULES` mapping keyed by ``rule_id`` and are
dispatched by :func:`run_rule`.
"""

from __future__ import annotations

import fnmatch
import os
import re
from dataclasses import dataclass, field, asdict
from typing import Callable

# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

SEVERITIES = ("info", "warning", "error")


@dataclass
class Finding:
    """A single governance deviation (drift) detected by a rule."""

    rule_id: str
    path: str
    line: int  # 1-based; 0 means "whole file / no specific line"
    severity: str
    message: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScannedFile:
    """One file in the scanned set, read once and shared across rules."""

    abspath: str
    relpath: str  # path relative to the scan root, using forward slashes
    text: str

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()


@dataclass
class ScanContext:
    """Everything a rule needs: the scan root and every scanned file."""

    root: str
    files: list[ScannedFile] = field(default_factory=list)

    def matching(self, glob: str) -> list[ScannedFile]:
        """Files whose relpath matches a glob (``**`` supported, case-insensitive)."""
        return [f for f in self.files if _glob_match(f.relpath, glob)]


def _glob_match(relpath: str, glob: str) -> bool:
    """Match a forward-slash relpath against a glob.

    ``fnmatch`` does not special-case ``/`` for ``**``, so we normalize a
    leading ``**/`` to mean "any depth, including zero" by also trying the
    basename and the suffix tail.
    """
    relpath = relpath.replace(os.sep, "/")
    glob = glob.replace(os.sep, "/")
    if fnmatch.fnmatch(relpath, glob):
        return True
    if glob.startswith("**/"):
        tail = glob[3:]
        # match at any depth
        if fnmatch.fnmatch(relpath, tail):
            return True
        if fnmatch.fnmatch(os.path.basename(relpath), tail):
            return True
        return fnmatch.fnmatch(relpath, "*/" + tail) or any(
            fnmatch.fnmatch(relpath, ("*/" * n) + tail) for n in range(1, 12)
        )
    return False


# --------------------------------------------------------------------------- #
# Shared parsing helpers
# --------------------------------------------------------------------------- #

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse a leading ``---`` YAML-ish frontmatter block.

    Stdlib-only: this is a deliberately small flat ``key: value`` parser, not a
    full YAML engine. It returns ``None`` when no frontmatter block is present,
    and a (possibly empty) dict of top-level scalar keys otherwise. Nested
    structures are ignored for key-presence purposes (the key is still recorded
    with an empty value).
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None
    body = m.group(1)
    data: dict[str, str] = {}
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # only treat top-level (non-indented) "key: value" lines as keys
        if line[0] in (" ", "\t", "-"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


# Wiki link: [[name]] or [[name|alias]] or [[name#anchor]]
_WIKILINK_RE = re.compile(r"\[\[([^\[\]|#]+?)(?:[#|][^\[\]]*)?\]\]")

# Inline markdown link/image with a relative target: [text](path) or ![alt](path)
_MDLINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+?)\s*(?:\"[^\"]*\")?\)")


def _line_of(text: str, index: int) -> int:
    """1-based line number for a character offset into ``text``."""
    return text.count("\n", 0, index) + 1


# --------------------------------------------------------------------------- #
# Rules
# --------------------------------------------------------------------------- #


def rule_dead_wiki_links(ctx: ScanContext, params: dict) -> list[Finding]:
    """Flag ``[[name]]`` references with no resolvable target.

    A target resolves if some scanned ``*.md`` file has basename ``name.md``
    (case-insensitive) OR carries a ``name:`` frontmatter field equal to the
    reference. Only files matching ``glob`` are scanned for references.
    """
    glob = params.get("glob", "**/*.md")
    severity = params.get("severity", "warning")

    # Build the resolvable-name index from the whole scanned set.
    names: set[str] = set()
    for f in ctx.files:
        if not f.relpath.lower().endswith(".md"):
            continue
        stem = os.path.splitext(os.path.basename(f.relpath))[0]
        names.add(stem.lower())
        fm = parse_frontmatter(f.text)
        if fm and "name" in fm and fm["name"]:
            names.add(fm["name"].lower())

    findings: list[Finding] = []
    for f in ctx.matching(glob):
        for m in _WIKILINK_RE.finditer(f.text):
            target = m.group(1).strip()
            if not target:
                continue
            if target.lower() not in names:
                findings.append(
                    Finding(
                        rule_id="dead_wiki_links",
                        path=f.relpath,
                        line=_line_of(f.text, m.start()),
                        severity=severity,
                        message=f"Wiki link [[{target}]] has no matching .md file or 'name:' frontmatter.",
                    )
                )
    return findings


def rule_dead_path_refs(ctx: ScanContext, params: dict) -> list[Finding]:
    """Flag markdown links to relative file paths that do not exist on disk.

    Absolute paths, URLs (``scheme://``), in-page anchors (``#...``) and
    ``mailto:`` are ignored — only on-disk relative file references are checked.
    """
    glob = params.get("glob", "**/*.md")
    severity = params.get("severity", "error")

    findings: list[Finding] = []
    for f in ctx.matching(glob):
        base_dir = os.path.dirname(f.abspath)
        for m in _MDLINK_RE.finditer(f.text):
            target = m.group(1).strip()
            if _is_external_or_anchor(target):
                continue
            # strip a trailing #anchor on a file ref
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            if os.path.isabs(file_part):
                continue
            resolved = os.path.normpath(os.path.join(base_dir, file_part))
            if not os.path.exists(resolved):
                findings.append(
                    Finding(
                        rule_id="dead_path_refs",
                        path=f.relpath,
                        line=_line_of(f.text, m.start()),
                        severity=severity,
                        message=f"Path reference '{target}' does not resolve on disk.",
                    )
                )
    return findings


def _is_external_or_anchor(target: str) -> bool:
    if not target:
        return True
    if target.startswith("#"):
        return True
    if target.startswith("mailto:"):
        return True
    # scheme://  or  proto:  (e.g. http://, https://, ftp://)
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", target):
        return True
    return False


def rule_required_header(ctx: ScanContext, params: dict) -> list[Finding]:
    """Files matching ``glob`` must contain a line matching ``pattern``.

    Useful for enforcing a classification banner or required header line.
    """
    glob = params.get("glob", "**/*.md")
    pattern = params.get("pattern")
    severity = params.get("severity", "error")
    if not pattern:
        raise ValueError("required_header rule needs a 'pattern' param")
    rx = re.compile(pattern, re.MULTILINE)

    findings: list[Finding] = []
    for f in ctx.matching(glob):
        if not rx.search(f.text):
            findings.append(
                Finding(
                    rule_id="required_header",
                    path=f.relpath,
                    line=0,
                    severity=severity,
                    message=f"Missing required header matching /{pattern}/.",
                )
            )
    return findings


def rule_required_tag(ctx: ScanContext, params: dict) -> list[Finding]:
    """Files matching ``glob`` must contain at least one of ``tags`` (regexes)."""
    glob = params.get("glob", "**/*.md")
    tags = params.get("tags", [])
    severity = params.get("severity", "warning")
    if not tags:
        raise ValueError("required_tag rule needs a non-empty 'tags' list")
    compiled = [re.compile(t) for t in tags]

    findings: list[Finding] = []
    for f in ctx.matching(glob):
        if not any(rx.search(f.text) for rx in compiled):
            findings.append(
                Finding(
                    rule_id="required_tag",
                    path=f.relpath,
                    line=0,
                    severity=severity,
                    message=f"None of the required provenance tags present: {tags}.",
                )
            )
    return findings


def rule_size_limit(ctx: ScanContext, params: dict) -> list[Finding]:
    """Files matching ``glob`` must be <= ``max_lines`` lines."""
    glob = params.get("glob")
    max_lines = params.get("max_lines")
    severity = params.get("severity", "warning")
    if not glob:
        raise ValueError("size_limit rule needs a 'glob' param")
    if max_lines is None:
        raise ValueError("size_limit rule needs a 'max_lines' param")

    findings: list[Finding] = []
    for f in ctx.matching(glob):
        n = len(f.lines)
        if n > max_lines:
            findings.append(
                Finding(
                    rule_id="size_limit",
                    path=f.relpath,
                    line=0,
                    severity=severity,
                    message=f"File has {n} lines, exceeds limit of {max_lines}.",
                )
            )
    return findings


def rule_frontmatter_shape(ctx: ScanContext, params: dict) -> list[Finding]:
    """Files matching ``glob`` must have frontmatter containing ``required_keys``."""
    glob = params.get("glob", "**/*.md")
    required_keys = params.get("required_keys", [])
    severity = params.get("severity", "error")
    if not required_keys:
        raise ValueError("frontmatter_shape rule needs a non-empty 'required_keys' list")

    findings: list[Finding] = []
    for f in ctx.matching(glob):
        fm = parse_frontmatter(f.text)
        if fm is None:
            findings.append(
                Finding(
                    rule_id="frontmatter_shape",
                    path=f.relpath,
                    line=1,
                    severity=severity,
                    message="Missing YAML frontmatter block (expected leading '---').",
                )
            )
            continue
        missing = [k for k in required_keys if k not in fm]
        if missing:
            findings.append(
                Finding(
                    rule_id="frontmatter_shape",
                    path=f.relpath,
                    line=1,
                    severity=severity,
                    message=f"Frontmatter missing required keys: {missing}.",
                )
            )
    return findings


# --------------------------------------------------------------------------- #
# Registry / dispatch
# --------------------------------------------------------------------------- #

RuleFn = Callable[[ScanContext, dict], list[Finding]]

RULES: dict[str, RuleFn] = {
    "dead_wiki_links": rule_dead_wiki_links,
    "dead_path_refs": rule_dead_path_refs,
    "required_header": rule_required_header,
    "required_tag": rule_required_tag,
    "size_limit": rule_size_limit,
    "frontmatter_shape": rule_frontmatter_shape,
}


def run_rule(rule_id: str, ctx: ScanContext, params: dict) -> list[Finding]:
    """Dispatch a single rule by id."""
    try:
        fn = RULES[rule_id]
    except KeyError:
        raise KeyError(f"Unknown rule_id '{rule_id}'. Known: {sorted(RULES)}")
    return fn(ctx, params)
