# EXTERNAL_TOOLS.md — Python Libraries, Obsidian, Agent Internals
## Classification: Tier 0

> Reference for the tooling layer beneath the methodology. Skip on first
> adoption; come back when you need it.

---

## Section 1 — Python libraries

### Provider SDKs (cloud LLMs)

| Library | Role | When to reach for it |
|---|---|---|
| `anthropic` | Anthropic's Claude SDK | Custom agents, batch jobs, scoring harnesses |
| `openai` | OpenAI's GPT SDK | Multi-provider consensus, OpenAI-specific features |
| `mistralai` | Mistral's hosted SDK | Cost arbitrage, third-provider consensus |

### Local model runners

| Library | Role | When |
|---|---|---|
| `ollama` | Local LLM runner serving open-weights models via HTTP | Data sovereignty, offline, latency / cost at volume |
| `llama-cpp-python` | Direct GGUF inference | Sovereign workstations, embedded / edge |

### Memory + retrieval

| Library | Role | When |
|---|---|---|
| `mcp` | Model Context Protocol — standardized tool exposure | Multi-agent compatibility for one tool definition |
| `sentence-transformers` | Embedding models | Semantic memory retrieval beyond keyword match |
| `chromadb` / `qdrant` | Vector stores | Memory store has outgrown keyword-match index |

### Document handling

| Library | Role | When |
|---|---|---|
| `pymupdf` (`fitz`) | PDF parsing + rendering | Domain involves PDFs |
| `python-docx` | Word docs | Office-format deliverables |
| `openpyxl` | Excel docs | Office-format deliverables |
| `obsidian-tools` | Programmatic vault operations | Scripts generating vault files |
| `watchdog` | Filesystem change events | React to file changes vs. polling |

### Cold-start install

```bash
pip install anthropic                # or your provider of choice
pip install pymupdf                  # if you have PDFs
pip install python-docx openpyxl     # if you handle Office formats
```

Add `ollama` for local inference. Add `sentence-transformers` + `chromadb`
when keyword matching stops finding the right memory files.

---

## Section 2 — Obsidian setup

A vault is just a folder of `.md` files. Markdown + YAML frontmatter.
Standard markdown links + Obsidian's `[[wikilinks]]`.

### Recommended core plugins (free, official)

| Plugin | What it does | When to enable |
|---|---|---|
| Templater | Boilerplate / scaffolding for new files | Right away |
| Dataview | Query frontmatter across the vault | When you have ~10+ similarly-shaped notes |
| Excalidraw | Diagram-as-markdown | When diagrams need to live with prose |

### Recommended community plugins

| Plugin | What it does |
|---|---|
| MCP-bridge | Exposes the vault as an MCP server |
| Tasks | Aggregate `[ ]` checkboxes across the vault |
| Calendar | Daily-note pattern for session-end snapshots |

### How `MEMORY.md` becomes browsable

- Each `[Title](file.md)` link → clickable navigation
- Graph view → `MEMORY.md` at center, every topic file linked off it
- Wikilinks resolve cross-file

The agent doesn't *use* Obsidian. The agent reads / writes the same
`.md` files. Obsidian is the *human-facing* view of the same data.

### Cold-start checklist

1. Install Obsidian (free).
2. Open your vault folder.
3. Enable Templater + Dataview.
4. Skip community plugins until you have a need.
5. Don't worry about graph view until you have ~20 files.

---

## Section 3 — Agent tools — under the hood

### What tool-calling actually is

1. Model produces structured JSON-shaped output: *"call `read_file` with
   path = `/foo/bar.md`."*
2. **Harness** (Claude Code, Cline, custom Python loop) **executes** the
   tool call.
3. Harness returns result to model as structured input.
4. Model continues turn with result in context.

The model **decides what tools to call.** The harness **actually calls
them.** The agent's permissions = the harness's permissions.

### The message loop

```
loop:
  user_message → model_input
  model produces: text + tool_calls
  for each tool_call:
    harness.execute(tool_call)
    result → model_input
  model continues until: stop sequence | tool_calls exhausted
end loop
```

Every iteration accumulates state in the context window.

### Why memory must persist outside the context window

- Context window is **finite + per-session**.
- Memory store is **infinite + cross-session**.
- Auto-loaded files (`DIRECTIVE.md`, `MEMORY.md`) are the bridge — they
  re-inject prior session's distilled state at the start of each new
  session.

This is why `MEMORY.md` matters. It's the connective tissue between
sessions.

### How MCP standardizes tool exposure

Without MCP: every tool is harness-specific. Three implementations of
"read a file" for three harnesses.

With MCP: a tool server speaks JSON-RPC; any MCP-compliant client can
use it. One implementation, multiple harnesses.

### How filesystem / bash / web-search tools get sandboxed

The harness defines the sandbox:
- Filesystem scope (paths under vault root).
- Command allow/denylist (`rm -rf` blocked or approved).
- Network policy (allow-listed domains).
- Per-action approval (some destructive actions need explicit OK).

`GOVERNANCE.md` Tier 0–5 + HITL gates are the **operator-side
complement** to the harness sandbox. Harness enforces what *can*
happen; governance defines what *should*.

### Token economics

- Auto-loaded files are paid **every turn**. Keep `MEMORY.md` under 200 lines.
- Topic files are free until loaded. Push detail there.
- Output tokens cost ~3-5× input tokens.
- **Prompt caching** (Anthropic's `cache_control: ephemeral`) gives
  ~90% cost reduction on stable system-context prefix. Worth wiring up
  at >100 queries/day.

---

## Common operator patterns

### Cloud + local hybrid
Cloud for complex reasoning. Local (ollama) for bulk formatting /
classification. Token economics drive this.

### MCP server per concern
Small servers, one per concern (filesystem, vault search, web fetch).
Composable; independently debuggable.

### Prompt cache the auto-load layer
At >100 queries/day, ~90% cost reduction is real money.

---

## One viable infrastructure stack

> **Named not endorsed.** What follows names tools the methodology's
> authoring vault uses. Documenting one working stack so adopters can
> match it, substitute knowingly, or reject on informed grounds.
> Substitute equivalents wherever your context differs.

| Layer | Authoring vault uses | Viable substitutes |
|---|---|---|
| Sovereign workstation | Linux desktop (32-128 GB RAM, modern GPU for ollama / llama-cpp local inference) | any Linux build; Mac Studio for Apple-stack operators |
| Remote-access mesh | **Tailscale** (WireGuard-based, identity-gated) | Nebula, ZeroTier, plain WireGuard, ssh reverse tunnels |
| VPS hosting | **Hetzner** (Linux VPS, systemd, Tailscale-gated) | Linode, Vultr, DigitalOcean, OVH, self-hosted hardware |
| Domain artifact authoring | **FreeCAD** (when domain is spatial; Python scriptable) | Excalidraw, Mermaid, Inkscape, LaTeX, Pandoc — pick by domain |

**Pattern:** pick tools with both interactive and programmatic access.
The agent must be able to edit artifacts; the operator must be able
to refine. Tools that offer only one mode break the partnership.

**Why name them.** Per `DIRECTIVE.md` Section 8 (anti-fragility / build
for portability), tool dependencies should be **made visible** rather
than hidden. Hiding the stack makes the methodology look more general
but actually weakens the worked example — adopters have to guess what
real tooling looks like.

---

## Further reading

- Anthropic: `https://docs.claude.com/`
- OpenAI: `https://platform.openai.com/docs`
- Mistral: `https://docs.mistral.ai/`
- Ollama: `https://ollama.com/`
- llama.cpp: `https://github.com/ggerganov/llama.cpp`
- MCP: `https://modelcontextprotocol.io/`
- Obsidian: `https://obsidian.md/`
- ChromaDB: `https://www.trychroma.com/`
- Qdrant: `https://qdrant.tech/`

---

## Why this doc isn't required reading

You can adopt the methodology without any of this. Foundation docs +
templates + a working harness (Claude Code or equivalent) is enough.

This doc is the next layer for operators who want to: build their own
agents, deploy local models, optimize at volume, or understand failure
modes when the abstraction breaks.

Skip on first pass. Come back when you need it.

---

_Apache 2.0._
