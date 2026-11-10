# Navigator

*Observe what your agents and your codebase are actually doing.*

Navigator is a local-first sense-making app. Point it at a tree and it indexes the files, maps dependencies
(root / hub / dependent / self-contained), runs pluggable gap analyzers, and produces reports — keeping
plain-language summaries that a human confirms or corrects (corrections become durable and authoritative).

## Install
```bash
cd navigator
pip install -e .
```
Python 3.11+. Dependencies are listed in `requirements.txt`.

## Core commands
```bash
navigator index /path/to/project     # build the index (files + dependency edges)
navigator sense                      # human-confirmed plain-language summaries per scope
navigator report                     # findings + delta report
```
Run `navigator --help` for the full verb list.

## Configuration
Copy `config.example.toml` to `config.toml` and edit:
- `root` — the tree to index.
- LLM backend — `stub` (deterministic default, no model), `ollama` (local), or any OpenAI-compatible endpoint.
- `exclude_dirs` — directories to skip.

The default backend is `stub` so Navigator runs and proves out with **no model at all**; the LLM is opt-in and
only ever produces `perceived` text for human confirmation.

## Analyzers
Gap analyzers are pluggable (`navigator/analyzers/`): broken references, doc drift, missing docs. Add your own
by following the same interface — each returns structured findings the mechanical core trusts.

## Trust model
Navigator embodies the shared [Trust Model](./Trust-Model.md): the index and analyzers are deterministic and
authoritative; any model-authored summary is labeled `perceived` and is not treated as fact until a human
confirms it. Reports are observations and recommendations — Navigator does not silently edit your tree.

## Tests
```bash
python tests/prove_core.py
python tests/prove_sense.py
python tests/prove_outputs.py
```
The proofs are adversarial (they assert the tool catches bad states, not just that it runs).

*Part of [Governance Blueprint](./Home.md).*
