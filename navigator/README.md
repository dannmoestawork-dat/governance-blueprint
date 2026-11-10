# Navigator

A sense-making companion for your project tree. Navigator indexes a
directory, maps which tools depend on which, runs gap analyzers, keeps a
plain-language living summary of what everything appears to be *for* — which
you can correct, and your corrections stick — and recommends next steps. It
keeps a wiki of everything it does, and searches its own history to get
better over time.

It runs entirely offline in a terminal (a clean keyboard-driven dashboard
that works over plain SSH), and can optionally use a local LLM and a
self-hosted search engine — no cloud account required for anything.

*Part of the Governance Blueprint toolkit.*

## The trust model

Navigator is built around one rule: **the mechanical core enforces; the
model only narrates.** The index, the dependency map, and every gap analyzer
are deterministic code — no model involved. A model (if you configure one)
only turns that real evidence into plain language, and everything it writes
is labeled `perceived` until you confirm or correct it. Your corrections are
durable: they're fed back into every future summary and always displayed.

A few structural guarantees follow from that rule:

- Navigator refuses to summarize a scope with no indexed evidence — it will
  not let a model speculate from a directory name alone.
- Navigator never writes into your tree. `report`, `memory`, `work`, and
  `delegate` produce files in `data/outbox/` only.
- Every generated work product carries a full evidence manifest, including a
  count of what was *not* read, so coverage is never silently overstated.

## Install

```bash
git clone <this repo> && cd navigator
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
```

## Quick start

```bash
navigator init                # writes config.toml — edit [index].roots
navigator index <path>        # catalog + full-text index a tree
                              # (or just `navigator index` after editing config)
navigator map                 # build the dependency map
navigator analyze             # run all gap analyzers
navigator sense <scope>       # plain-language summary of one scope
navigator report              # write a findings report to data/outbox/
navigator dash                # open the dashboard (TUI)
```

A *scope* is a path key like `myproject/tools` — top-level entries appear in
the dashboard's left pane. Run `navigator status` to see indexed counts and
available scopes.

## The dashboard

```
┌ Navigator ──────────────────────────────────────────────────┐
│ scopes            │ Overview │ Summary │ Findings │ Recs │ Search │
│  myproject/docs   │                                        │
│  myproject/tools  │  Files indexed: 31,204                 │
│  …                │  Open findings: 117                    │
│                   │  …                                     │
└ i Index  m Map  a Analyze  s Summarize  r Recommend  q Quit ┘
```

Select a scope on the left, press `s` for a plain-language summary, and type
corrections into the feedback box — they become permanent context.

## CLI reference

| Command | What it does |
|---|---|
| `navigator index` | Catalog every file; full-text index text files |
| `navigator map` | Extract dependency edges; classify tools root / dependent / hub / self-contained |
| `navigator analyze [name]` | Run one or all gap analyzers (runs and findings are recorded) |
| `navigator sense <scope>` | Generate/refresh the plain-language summary for a scope |
| `navigator feedback <scope> "note"` | Correct a summary — durable, authoritative |
| `navigator confirm <scope>` | Mark a summary human-verified |
| `navigator recommend` | Ranked plain-language next steps |
| `navigator search <query>` | Full-text search (FTS5) |
| `navigator status` | One-screen text status |
| `navigator report` | Write a findings report (with delta since last) to `data/outbox/` |
| `navigator memory` | Write the knowledge dump: everything it believes + everything you taught it |
| `navigator work [--list] [id]` | Execute `Standing ask:` feedback notes into finished deliverables |
| `navigator delegate` | Turn open findings into agent-ready work orders (md + JSON manifest) |
| `navigator dash` | The TUI dashboard |

`report`/`memory`/`work`/`delegate` all produce files in `data/outbox/`,
never edits to your tree. Work orders are briefs any agent can execute; work
products are labeled `[perceived]` with a full evidence manifest.

## Configuration

Everything lives in one `config.toml` (see `config.example.toml`). Notable:

- `[index] roots` — the directories to index (the only required setting).
- `[llm] backend` — `stub` (default; deterministic, offline, no model),
  `ollama` (any local Ollama server), or `openai` (any OpenAI-compatible URL;
  key via the `NAVIGATOR_LLM_API_KEY` environment variable).
- `[web] searx_url` — optional self-hosted SearXNG for `search`; all
  fetches are cached on disk so offline mode never breaks.
- `[analyzers] required_docs` — which doc files a directory of scripts is
  expected to carry.

## Built-in gap analyzers

- **missing_docs** — script directories missing their required docs
- **broken_refs** — file references whose target no longer exists
  (conservative: only when the parent directory still exists)
- **doc_drift** — docs that lag their scripts by more than N days

Add your own by subclassing `Analyzer` in `navigator/analyzers/` — roughly
20 lines.

## Proofs

```bash
python tests/prove_core.py     # mechanical core   (27 checks)
python tests/prove_sense.py    # narration layer   (24 checks)
python tests/prove_outputs.py  # manager layer     (17 checks)
python tests/prove_tui.py      # dashboard smoke test
```

## License

Apache-2.0. See the `LICENSE` file at the repository root.
