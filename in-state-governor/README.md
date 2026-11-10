<!-- SPDX-License-Identifier: Apache-2.0 -->
# In-State Governor

A small, deterministic **governance-compliance checker** for documentation and
codebase trees. It repeatedly scans a project against a set of governance
rules, records every deviation ("drift"), and reports it as a reviewable
ledger.

Part of **Governance Blueprint**.

## Philosophy: enforce, don't instruct

> A deterministic check is the trust anchor. Never rely on an LLM to
> self-police.

In-State Governor is the **mechanical core**: every check is a plain Python
function whose result is fully reproducible from the files on disk and the
config. There is no model in the loop. A model may *advise* a human reviewer,
but it can never be the thing that decides whether a rule passed — because a
checker that can rationalize its way past a violation is not a checker.

Structure enforces. The tool surfaces drift deterministically; a human
adjudicates each finding in the ledger (`Accept` / `Reject` / `Defer`).

## Install

Pure Python standard library, requires **Python 3.11+** (for `tomllib`). No
third-party runtime dependencies.

```sh
pip install .
# or run straight from the source tree without installing:
python -m governor.cli scan <path> --config governor.toml
```

## Usage

```sh
governor scan <path> [--config governor.toml] [--format md|json] [--out FILE]
```

- `<path>` — directory tree to scan.
- `--config` — TOML rule config (default `governor.toml`).
- `--format` — `md` (drift ledger, default) or `json`.
- `--out` — output file, or `-` for stdout.

Exit codes: `0` no error-severity findings, `1` at least one error-severity
finding (use this to gate CI), `2` usage/config/IO error.

## Configuration

Rules are declared in TOML as an array of `[[rule]]` tables. `id` selects the
rule; every other key is passed through as a parameter. See
[`governor.example.toml`](governor.example.toml) for a complete generic
starting point.

```toml
[[rule]]
id = "required_header"
glob = "**/*.md"
pattern = "^## Classification:"
severity = "error"

[[rule]]
id = "size_limit"
glob = "INDEX.md"
max_lines = 200
severity = "warning"
```

### Built-in rules

| Rule id | What it catches | Key params |
| --- | --- | --- |
| `dead_wiki_links` | `[[name]]` with no matching `<name>.md` (by filename or a `name:` frontmatter field) | `glob`, `severity` |
| `dead_path_refs` | Markdown links to relative paths that don't resolve on disk | `glob`, `severity` |
| `required_header` | Files in `glob` missing a line matching `pattern` | `glob`, `pattern`, `severity` |
| `required_tag` | Files in `glob` lacking any of a set of provenance `tags` (regexes) | `glob`, `tags`, `severity` |
| `size_limit` | Files in `glob` exceeding `max_lines` | `glob`, `max_lines`, `severity` |
| `frontmatter_shape` | Files in `glob` whose YAML frontmatter lacks `required_keys` | `glob`, `required_keys`, `severity` |

Severities are `info`, `warning`, `error`. Only `error` findings fail the exit
gate.

## Sample output (markdown ledger)

```markdown
# Governance Drift Ledger

- Generated (UTC): 2026-01-01T00:00:00Z
- Total findings: **2**

## Severity rollup

| Severity | Count |
| --- | --- |
| info | 0 |
| warning | 1 |
| error | 1 |
| **total** | **2** |

## Findings by rule

### `dead_path_refs` (1)

- [error] `docs/guide.md:14` — Path reference 'images/missing.png' does not resolve on disk.
  - Decision: ☐ Accept ☐ Reject ☐ Defer

### `dead_wiki_links` (1)

- [warning] `notes/a.md:2` — Wiki link [[ghost]] has no matching .md file or 'name:' frontmatter.
  - Decision: ☐ Accept ☐ Reject ☐ Defer
```

JSON output (`--format json`) emits the same findings with a summary block,
suitable for machine consumption.

## Tests

The proof suite is **adversarial**: for every rule it asserts both that a clean
fixture produces zero findings *and* that a seeded violation is caught. A
checker that only ever passes proves nothing.

```sh
python tests/prove_governor.py
```

## License

Apache-2.0.
