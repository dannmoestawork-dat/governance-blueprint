# SPDX-License-Identifier: Apache-2.0
"""Adversarial proof suite for In-State Governor.

A checker that only ever passes proves nothing. For every rule we assert BOTH
sides of the contract:

  * a CLEAN fixture produces ZERO findings, and
  * a DIRTY fixture (one seeded violation) produces a finding the rule must
    catch, at the right path/line where applicable.

Run with plain ``python tests/prove_governor.py``. Prints PASS/FAIL counts and
exits non-zero on any failure.
"""

from __future__ import annotations

import os
import sys
import tempfile

# Make the package importable when run as a bare script.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from governor.config import load_config_str  # noqa: E402
from governor.report import to_json, to_markdown  # noqa: E402
from governor.rules import (  # noqa: E402
    ScanContext,
    ScannedFile,
    parse_frontmatter,
    run_rule,
)
from governor.scan import build_context, scan  # noqa: E402

_PASS = 0
_FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global _PASS, _FAIL
    if condition:
        _PASS += 1
        print(f"PASS  {name}")
    else:
        _FAIL += 1
        print(f"FAIL  {name}  {detail}")


def _ctx_from(files: dict[str, str]) -> ScanContext:
    """Build an in-memory ScanContext from {relpath: text}."""
    scanned = [
        ScannedFile(abspath="/virtual/" + rel, relpath=rel, text=text)
        for rel, text in files.items()
    ]
    return ScanContext(root="/virtual", files=scanned)


# --------------------------------------------------------------------------- #
# Rule 1: dead_wiki_links
# --------------------------------------------------------------------------- #
def test_dead_wiki_links() -> None:
    # CLEAN: link target exists as a file, and via frontmatter 'name'.
    clean = _ctx_from(
        {
            "a.md": "See [[topic]] and [[Alias]].",
            "topic.md": "the topic file",
            "real.md": "---\nname: Alias\n---\nbody",
        }
    )
    f = run_rule("dead_wiki_links", clean, {})
    check("dead_wiki_links clean -> 0", len(f) == 0, f"got {f}")

    # DIRTY: [[ghost]] has no target.
    dirty = _ctx_from({"a.md": "intro\nSee [[ghost]] here.\n", "topic.md": "x"})
    f = run_rule("dead_wiki_links", dirty, {})
    check("dead_wiki_links dirty -> 1", len(f) == 1, f"got {f}")
    if f:
        check("dead_wiki_links line=2", f[0].line == 2, f"line {f[0].line}")
        check("dead_wiki_links names target", "ghost" in f[0].message, f[0].message)


# --------------------------------------------------------------------------- #
# Rule 2: dead_path_refs
# --------------------------------------------------------------------------- #
def test_dead_path_refs() -> None:
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "sub"), exist_ok=True)
        with open(os.path.join(d, "sub", "exists.txt"), "w") as fh:
            fh.write("here")

        # CLEAN: link resolves; URL + anchor ignored.
        with open(os.path.join(d, "clean.md"), "w") as fh:
            fh.write(
                "[ok](sub/exists.txt)\n"
                "[web](https://example.com/x)\n"
                "[anchor](#section)\n"
            )
        # DIRTY: link to a missing file.
        with open(os.path.join(d, "dirty.md"), "w") as fh:
            fh.write("line1\n[broken](sub/missing.txt)\n")

        cfg = load_config_str('[[rule]]\nid = "dead_path_refs"\nglob = "**/*.md"\n')
        findings = scan(d, cfg)
        clean_hits = [x for x in findings if x.path == "clean.md"]
        dirty_hits = [x for x in findings if x.path == "dirty.md"]
        check("dead_path_refs clean -> 0", len(clean_hits) == 0, f"got {clean_hits}")
        check("dead_path_refs dirty -> 1", len(dirty_hits) == 1, f"got {dirty_hits}")
        if dirty_hits:
            check("dead_path_refs line=2", dirty_hits[0].line == 2, f"line {dirty_hits[0].line}")


# --------------------------------------------------------------------------- #
# Rule 3: required_header
# --------------------------------------------------------------------------- #
def test_required_header() -> None:
    params = {"glob": "**/*.md", "pattern": "^## Classification:"}
    clean = _ctx_from({"a.md": "# Title\n## Classification: PUBLIC\nbody"})
    check("required_header clean -> 0", len(run_rule("required_header", clean, params)) == 0)

    dirty = _ctx_from({"a.md": "# Title\nbody without header"})
    f = run_rule("required_header", dirty, params)
    check("required_header dirty -> 1", len(f) == 1, f"got {f}")


# --------------------------------------------------------------------------- #
# Rule 4: required_tag
# --------------------------------------------------------------------------- #
def test_required_tag() -> None:
    params = {"glob": "**/*.md", "tags": [r"\[AI-GENERATED\]", r"\[VERIFIED\]"]}
    clean = _ctx_from({"a.md": "content [VERIFIED] more"})
    check("required_tag clean -> 0", len(run_rule("required_tag", clean, params)) == 0)

    dirty = _ctx_from({"a.md": "content with no provenance tag"})
    f = run_rule("required_tag", dirty, params)
    check("required_tag dirty -> 1", len(f) == 1, f"got {f}")


# --------------------------------------------------------------------------- #
# Rule 5: size_limit
# --------------------------------------------------------------------------- #
def test_size_limit() -> None:
    params = {"glob": "INDEX.md", "max_lines": 3}
    clean = _ctx_from({"INDEX.md": "l1\nl2\nl3"})
    check("size_limit clean -> 0", len(run_rule("size_limit", clean, params)) == 0)

    dirty = _ctx_from({"INDEX.md": "l1\nl2\nl3\nl4\nl5"})
    f = run_rule("size_limit", dirty, params)
    check("size_limit dirty -> 1", len(f) == 1, f"got {f}")
    if f:
        check("size_limit reports count", "5" in f[0].message, f[0].message)


# --------------------------------------------------------------------------- #
# Rule 6: frontmatter_shape
# --------------------------------------------------------------------------- #
def test_frontmatter_shape() -> None:
    params = {"glob": "**/*.md", "required_keys": ["title", "status"]}
    clean = _ctx_from({"a.md": "---\ntitle: X\nstatus: draft\n---\nbody"})
    check("frontmatter_shape clean -> 0", len(run_rule("frontmatter_shape", clean, params)) == 0)

    # DIRTY-A: missing a key.
    dirty1 = _ctx_from({"a.md": "---\ntitle: X\n---\nbody"})
    f1 = run_rule("frontmatter_shape", dirty1, params)
    check("frontmatter_shape missing-key -> 1", len(f1) == 1, f"got {f1}")
    if f1:
        check("frontmatter_shape names key", "status" in f1[0].message, f1[0].message)

    # DIRTY-B: no frontmatter at all.
    dirty2 = _ctx_from({"a.md": "no frontmatter here"})
    f2 = run_rule("frontmatter_shape", dirty2, params)
    check("frontmatter_shape no-block -> 1", len(f2) == 1, f"got {f2}")


# --------------------------------------------------------------------------- #
# Frontmatter parser unit checks
# --------------------------------------------------------------------------- #
def test_frontmatter_parser() -> None:
    check("frontmatter none", parse_frontmatter("no block") is None)
    fm = parse_frontmatter("---\ntitle: Hi\nname: foo\n---\nbody")
    check("frontmatter keys", fm == {"title": "Hi", "name": "foo"}, f"got {fm}")


# --------------------------------------------------------------------------- #
# Glob matching (the load-bearing path matcher)
# --------------------------------------------------------------------------- #
def test_glob() -> None:
    ctx = _ctx_from({"top.md": "x", "docs/deep/inner.md": "y", "notes/n.txt": "z"})
    md = {f.relpath for f in ctx.matching("**/*.md")}
    check("glob **/*.md depth0+N", md == {"top.md", "docs/deep/inner.md"}, f"got {md}")
    docs = {f.relpath for f in ctx.matching("docs/**/*.md")}
    check("glob docs/**/*.md", docs == {"docs/deep/inner.md"}, f"got {docs}")
    idx = {f.relpath for f in ctx.matching("top.md")}
    check("glob exact file", idx == {"top.md"}, f"got {idx}")


# --------------------------------------------------------------------------- #
# Config loader
# --------------------------------------------------------------------------- #
def test_config() -> None:
    cfg = load_config_str(
        '[[rule]]\nid = "size_limit"\nglob = "INDEX.md"\nmax_lines = 10\n'
    )
    check("config parses 1 rule", len(cfg.rules) == 1, f"got {cfg.rules}")
    check("config rule id", cfg.rules[0].rule_id == "size_limit")
    check("config params strip id", "id" not in cfg.rules[0].params)

    # Unknown rule id must raise.
    raised = False
    try:
        load_config_str('[[rule]]\nid = "nope"\n')
    except ValueError:
        raised = True
    check("config rejects unknown id", raised)

    # Empty config must raise.
    raised = False
    try:
        load_config_str("title = 'x'\n")
    except ValueError:
        raised = True
    check("config rejects no rules", raised)


# --------------------------------------------------------------------------- #
# Report rendering
# --------------------------------------------------------------------------- #
def test_report() -> None:
    dirty = _ctx_from({"a.md": "See [[ghost]]."})
    findings = run_rule("dead_wiki_links", dirty, {})
    md = to_markdown(findings, root="/virtual")
    check("report md has ledger title", "# Governance Drift Ledger" in md)
    check("report md has rollup table", "| Severity | Count |" in md)
    check("report md has decision line", "Decision: [ ] Accept [ ] Reject [ ] Defer" in md)
    check("report md groups by rule", "`dead_wiki_links`" in md)

    js = to_json(findings, root="/virtual")
    check("report json has findings", '"findings"' in js and '"dead_wiki_links"' in js)

    empty_md = to_markdown([], root="/virtual")
    check("report md empty -> no drift msg", "No drift detected" in empty_md)


# --------------------------------------------------------------------------- #
# End-to-end disk scan
# --------------------------------------------------------------------------- #
def test_e2e_scan() -> None:
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("## Classification: PUBLIC\n[VERIFIED]\nl1\nl2\n")
        cfg = load_config_str(
            '[[rule]]\nid = "required_header"\nglob = "**/*.md"\n'
            'pattern = "^## Classification:"\n'
        )
        findings = scan(d, cfg)
        check("e2e clean scan -> 0", len(findings) == 0, f"got {findings}")

        with open(os.path.join(d, "bad.md"), "w", encoding="utf-8") as fh:
            fh.write("no header here\n")
        findings = scan(d, cfg)
        check("e2e dirty scan -> 1", len(findings) == 1, f"got {findings}")


def main() -> int:
    tests = [
        test_dead_wiki_links,
        test_dead_path_refs,
        test_required_header,
        test_required_tag,
        test_size_limit,
        test_frontmatter_shape,
        test_frontmatter_parser,
        test_glob,
        test_config,
        test_report,
        test_e2e_scan,
    ]
    for t in tests:
        t()
    total = _PASS + _FAIL
    print()
    print(f"RESULT: {_PASS}/{total} passed, {_FAIL} failed")
    return 1 if _FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
