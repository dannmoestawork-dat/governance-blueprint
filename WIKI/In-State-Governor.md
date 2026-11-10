# In-State Governor

*The compliance auditor that keeps the rules — and everyone following them — honest.*

In-State Governor repeatedly checks a documentation/codebase tree against a set of **governance rules**,
records every deviation (drift), and reports it. Where Navigator asks *"are the agents doing good work?"*,
In-State Governor asks *"is everyone following the rules we set?"* — and it sits **above** Navigator (it can
audit Navigator's own compliance too).

This release ships the **deterministic reference core** — the mechanical checks that form the trust anchor. An
LLM-advisory layer (interpretation, root-cause) is an optional future addition; the core never depends on a
model.

## Install
```bash
cd in-state-governor
pip install -e .
```
Python 3.11+. Pure standard library (uses `tomllib` for config) — no third-party dependencies.

## Run a scan
```bash
governor scan /path/to/project --config governor.example.toml --format md --out drift.md
# or without installing:
python -m governor.cli scan /path/to/project --config governor.toml
```
Exit codes: `0` = no error-severity drift, `1` = error-severity drift found (use as a CI gate), `2` =
usage/config error.

## The rules (deterministic reference set)
Each rule is a self-contained check returning findings `{rule_id, path, line, severity, message}`:

1. **dead_wiki_links** — `[[name]]` references whose target file doesn't exist.
2. **dead_path_refs** — markdown links to relative paths that don't resolve on disk.
3. **required_header** — files matching a glob must contain a configured header regex (e.g. a classification line).
4. **required_tag** — files matching a glob must carry at least one of a configured set of provenance tags.
5. **size_limit** — a configured file must be ≤ N lines (e.g. an index that must stay loadable).
6. **frontmatter_shape** — files in a glob must have YAML frontmatter with required keys.

These six map directly to the highest-frequency drift classes found in real audits: **dead pointers from
renames/moves** and **record-vs-reality / structural drift**.

## Configuration
`governor.example.toml` declares which rules are enabled and their parameters (globs, regexes, limits). Copy it
to `governor.toml` and tailor it to your project's rules. It's config-driven on purpose — the tool is generic;
*your* governance schema lives in the config.

## Output
A markdown **drift ledger** (findings grouped by rule, a severity rollup table, each finding with `path:line`
and a blank `Decision: ☐ Accept ☐ Reject ☐ Defer` line) and/or JSON. The ledger is append-friendly and
human-decided — drift is recorded and decided, never auto-fixed.

## Trust model & tests
Pure mechanical core = the trust anchor ([Trust Model](./Trust-Model.md)). The proofs are adversarial:
```bash
python tests/prove_governor.py     # asserts each rule catches a seeded violation AND passes a clean case
```

*Part of [Governance Blueprint](./Home.md).*
