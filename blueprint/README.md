# LLM Training Products — A Sovereign Workstation Blueprint
## [AI-GENERATED] — 2026-04-28 — Apache 2.0
## Status: v1.2 — v1.0 core (2026-04-28, frozen) + two additive modules (2026-07-08) + lessons since v1.1 (2026-11-10)

> **Intentional redundancy.** The filled `...SYNC_*.md` set and the blank `templates/` set are BOTH the product (worked example + blank kit). The parallel pair is the point; keep both.

> A blueprint for building a sovereign, persistent-memory workstation for
> self-hosting LLMs and agents — for **any kind of knowledge work**, not
> tied to any single domain.

---

## What this is

A reusable methodology + document set for operators who want to:

1. Run LLMs/agents on hardware they own (or that they trust).
2. Give those agents **persistent memory** that survives across sessions.
3. Govern what the agents can read, write, and act on — with explicit tiers,
   gates, and provenance trails.
4. Maintain a clear, auditable record of *what was generated*, *who reviewed it*,
   and *why decisions were made*.

It is **model-agnostic.** The patterns work for Claude Code, Cline, Aider,
custom agents on any provider's SDK, ollama-based local agents, and any
future LLM harness that respects a filesystem and a contract.

It is **domain-agnostic.** Where examples are needed, they are drawn from a
worked case study (`worked_example/RoofTakeoff/`) but the methodology applies
to legal research, scientific notebooks, freelance consulting, lab journals,
academic writing, contract review, or any domain where structured knowledge
work benefits from a persistent AI collaborator.

---

## The seven primitives

This blueprint teaches one stack — seven components that together form the
**sovereign workstation pattern**:

| Primitive | What it is |
|---|---|
| **Model** | The LLM (cloud or local) you partner with |
| **Obsidian** | A markdown vault — the operator-readable view of your knowledge |
| **File_System** | Plain folders + plain files — the durable layer |
| **Markdown** | The single document format for context, memory, and product |
| **Script** | Python (or your language of choice) for the deterministic work |
| **memory_schema** | Persistent cross-session memory by topic + index |
| **Naming convention** | A bracket-token filename pattern that makes the filesystem itself navigable |

Everything in this product teaches how to wire those seven together so they
reinforce each other.

---

## Reading order

Read these in order. Skim is fine — but skim in order. Skip ahead only
when you've completed the foundation.

### Foundation (read these first, ~90 minutes total)

1. **`...DIRECTIVE.md`** — The auto-loaded contract. What the LLM reads at
   every session start. Who you are, what you're building, what's off-limits.
2. **`...GOVERNANCE.md`** — The 6-tier classification framework (Tier 0–Tier 5)
   and HITL gates. What autonomy the agent has at each level.
3. **`...FOLDER_LAYOUT.md`** — The directory pattern. Production / Pipeline /
   Reference / Tools split with a clear lifecycle ramp.
4. **`...NAMING_CONVENTIONS.md`** — The bracket-token filename pattern.
   `[Project][DATE][VERSION][Folder-SyncTag][Etc].ext`. Includes the
   `LOCAL` / `SYNC` / `SHARE` privacy/security signal.
5. **`...MEMORY_SCHEMA.md`** — Persistent cross-session memory: types,
   index, when to write, how the agent uses it.
6. **`...KNOWN_LIMITATIONS.md`** — **Read this before going further.** What
   doesn't work yet, why it doesn't work, what it costs when it fails, what
   we're doing about it. Memory misses, curation effort, context drops.

### Process docs (read after foundation, ~60 minutes total)

7. **`...SESSION_PROTOCOL.md`** — Start-of-session and end-of-session loops,
   recurring-maintenance check.
8. **`...TASK_QUEUE.md`** — Standing work queue + Tier-1/2/3 model.
9. **`...MAINTENANCE_LOG.md`** — Per-tool error log, reasoning, dependencies,
   handoff notes.
10. **`...KNOWLEDGE_MANAGEMENT.md`** — The "carved-in-stone" layer. Validated
    processes that have been used enough to be canonical. Distinct from memory
    (provisional), MAINTENANCE_LOG (per-tool), and code-review wiki (audit-time).
11. **`...DATA_SOURCES.md`** — External-source indexing pattern.
12. **`...INVENTORY.md`** — Tools registry + state.
13. **`...SESSION_ENV.md`** — Cross-session environment + recurring-maintenance
    checklist.
14. **`...LEARNING_LOG.md`** — Terminology corrections + communication patterns.
15. **`...SECURITY_AUDIT_LOG.md`** — Recurring scan pattern + cadence.
16. **`...ARCHIVE.md`** — Deletion + provenance protocol.

### Optional deeper reading

17. **`...EXTERNAL_TOOLS.md`** — Python libraries, Obsidian setup,
    agent tools under the hood (what tool-calling actually is, the message
    loop, MCP, token economics), plus **one viable infrastructure stack**
    (sovereign workstation hardware, Tailscale mesh, Hetzner VPS, FreeCAD
    for spatial-domain artifacts) — named not endorsed. Not required to
    start; valuable when the abstraction breaks, you want to build your
    own agent, or you're sizing your own deployment.

### v1.1 additions (read after the process docs)

18. **`LLMP001_2026-07-08_v1.1_..._RECURSIVE_IMPROVEMENT.md`** — a gated
    self-improvement loop for local LLM stacks: blind evals, typed failure
    findings, one-lever proposals, human-gated apply, deterministic re-eval,
    regression-test ratchet. Extends `...EXTERNAL_TOOLS.md` §1/§4/§5 and
    `...GOVERNANCE.md` §7–8; answers part of the multi-system limitation in
    `...KNOWN_LIMITATIONS.md`.
19. **`LLMP001_2026-07-08_v1.1_..._RUNBOOK_METHOD.md`** — the live-history
    runbook: one file that is both the instructions and the audit trail of a
    multi-step procedure. **§4 carries the reconciliation rulings** for how
    runbooks compose with `...KNOWLEDGE_MANAGEMENT.md`, the governance HITL
    gates, and `...TASK_QUEUE.md`'s single-writer rule — read §4 before
    adopting.

### v1.2 addition (read after you have run the loop for a few weeks)

20. **`LLMP001_2026-11-10_v1.2_..._LESSONS_SINCE_V1.md`** — eight rules the
    methodology learned the hard way after v1.1, each with the failure that
    earned it. Additive: nothing in v1.0 or v1.1 was rewritten.

(All product files in this directory follow the bracket-token naming
convention as a teaching example. The `templates/` subfolder contains the
same docs with **clean filenames** ready to copy into your own vault.)

---

## Templates — adoption-ready starter files

```
templates/
├── README.md                    ← templates index + adoption checklist
├── DIRECTIVE.md
├── GOVERNANCE.md
├── FOLDER_LAYOUT.md
├── NAMING_CONVENTIONS.md
├── MEMORY_SCHEMA.md
├── KNOWN_LIMITATIONS.md
├── SESSION_PROTOCOL.md
├── TASK_QUEUE.md
├── MAINTENANCE_LOG.md
├── KNOWLEDGE_MANAGEMENT.md
├── DATA_SOURCES.md
├── INVENTORY.md
├── SESSION_ENV.md
├── LEARNING_LOG.md
├── SECURITY_AUDIT_LOG.md
├── ARCHIVE.md
├── EXTERNAL_TOOLS.md
├── RECURSIVE_IMPROVEMENT.md     ← v1.1 — improvement-ledger scaffold
└── RUNBOOK_METHOD.md            ← v1.1 — blank runbook template
```

Each template is a tighter scaffold of the corresponding product doc — section
structure intact, placeholders where operator-specific content goes,
"why this section" commentary stripped (it lives in the product file).

Adopt by:

```bash
cp -r templates/ ~/your-vault/
cd ~/your-vault/
# Replace placeholders, set your project mnemonic, start your work
```

---

## Worked example

`worked_example/RoofTakeoff/` walks through one real tool's evolution —
from v1.0 through v1.6 over ~2 weeks — showing the methodology under
load. De-identified but structurally faithful.

The case is divided into 9 sections, each named for the *methodology
pattern* that drove the work (not the tool feature):

1. Session 1 — From idea to v1.0 (~4 hours)
2. The first memory entries
3. v1.1 → v1.5 — color palette and protocol expansion
4. The variance protocol session
5. Failure modes the methodology caught
6. The single-source-of-truth declaration (a NEW pattern that emerged)
7. The validate-then-update standing rule (another NEW pattern)
8. What's still broken (per `KNOWN_LIMITATIONS.md`)
9. What an operator copying this case would change for their domain

Two methodology patterns visible in this case (#6 and #7) were *not*
in the v1.0 methodology — they emerged from real work. The case study
shows them being captured and promoted, not anticipated.

Read this AFTER the foundation docs to see how the pieces compose.

---

## License

[Apache License 2.0](LICENSE) — Copyright 2026 Daniel Moesta / Material Industrial Sales & Consulting.

You may use, modify, and redistribute this work for any purpose, including
commercial use. The patent grant in Section 3 of the license protects both
authors and adopters. See `LICENSE` for full text.

---

## Provenance

Every document in this product carries one of three tags:

- **[AI-GENERATED]** — drafted entirely by an LLM
- **[AI-ASSISTED]** — human edited the AI's initial output
- **[VERIFIED]** — operator has reviewed for accuracy

This is the same tagging system the methodology teaches. Trust + credit
tracking is a feature of the product, not metadata about it.

---

## What this product is NOT

- **Not a fine-tuning dataset.** It is a methodology blueprint, not training data.
- **Not a commercial software product.** No subscription, no service. The
  methodology is open-source under Apache 2.0; you build from it.
- **Not specific to any single LLM provider.** Works with Claude, GPT,
  Mistral, Llama, Qwen, Phi, Gemma — anything that respects a filesystem
  and a contract.
- **Not a magic shortcut.** As `KNOWN_LIMITATIONS.md` makes explicit, the
  methodology has real limits. The compounding payoff is real, but so is
  the daily discipline.

---

## What's still being tuned

We publish `KNOWN_LIMITATIONS.md` as a first-class artifact for a reason.
The system has real failure modes — memory misses, curation effort,
context drops — and the methodology's response is to acknowledge them,
mitigate them where possible, and update this product when better
mitigations emerge.

Re-read `KNOWN_LIMITATIONS.md` quarterly. AI tooling iterates fast; what's
broken in 2026 may be solved in 2027. Your honest accounting should move
with it.

---

## File index (full set)

```
LLM_Training_Products/
├── LICENSE                                                    ← Apache 2.0
├── README.md                                                  ← THIS FILE
│
├── LLMP001_..._DIRECTIVE.md                                   ← #1 in reading order
├── LLMP001_..._GOVERNANCE.md                                  ← #2
├── LLMP001_..._FOLDER_LAYOUT.md                               ← #3
├── LLMP001_..._NAMING_CONVENTIONS.md                          ← #4
├── LLMP001_..._MEMORY_SCHEMA.md                               ← #5
├── LLMP001_..._KNOWN_LIMITATIONS.md                           ← #6 — read before going further
├── LLMP001_..._SESSION_PROTOCOL.md                            ← #7
├── LLMP001_..._TASK_QUEUE.md                                  ← #8
├── LLMP001_..._MAINTENANCE_LOG.md                             ← #9
├── LLMP001_..._KNOWLEDGE_MANAGEMENT.md                        ← #10
├── LLMP001_..._DATA_SOURCES.md                                ← #11
├── LLMP001_..._INVENTORY.md                                   ← #12
├── LLMP001_..._SESSION_ENV.md                                 ← #13
├── LLMP001_..._LEARNING_LOG.md                                ← #14
├── LLMP001_..._SECURITY_AUDIT_LOG.md                          ← #15
├── LLMP001_..._ARCHIVE.md                                     ← #16
├── LLMP001_..._EXTERNAL_TOOLS.md                              ← #17 (optional)
├── LLMP001_2026-07-08_v1.1_..._RECURSIVE_IMPROVEMENT.md       ← #18 (v1.1)
├── LLMP001_2026-07-08_v1.1_..._RUNBOOK_METHOD.md              ← #19 (v1.1)
├── LLMP001_2026-11-10_v1.2_..._LESSONS_SINCE_V1.md            ← #20 (v1.2)
│
├── templates/                                                 ← adoption-ready starters
│   ├── README.md
│   ├── DIRECTIVE.md
│   ├── GOVERNANCE.md
│   ├── FOLDER_LAYOUT.md
│   ├── NAMING_CONVENTIONS.md
│   ├── MEMORY_SCHEMA.md
│   ├── KNOWN_LIMITATIONS.md
│   ├── SESSION_PROTOCOL.md
│   ├── TASK_QUEUE.md
│   ├── MAINTENANCE_LOG.md
│   ├── KNOWLEDGE_MANAGEMENT.md
│   ├── DATA_SOURCES.md
│   ├── INVENTORY.md
│   ├── SESSION_ENV.md
│   ├── LEARNING_LOG.md
│   ├── SECURITY_AUDIT_LOG.md
│   ├── ARCHIVE.md
│   ├── EXTERNAL_TOOLS.md
│   ├── RECURSIVE_IMPROVEMENT.md
│   └── RUNBOOK_METHOD.md
│
└── worked_example/
    ├── README.md
    └── RoofTakeoff/
        ├── README.md
        └── RTKWE001_..._Case-Study.md
```

---

_Signed: Claude (Opus 4.7, 1M context) — 2026-04-28_

---

## Version history

- **v1.2 — 2026-11-10.** Module #20 `LESSONS_SINCE_V1.md` added (eight rules learned after v1.1); example
  folder names made generic; references to files outside this release removed. Why: pre-publication review
  before the first public upload. Nothing in v1.0 or v1.1 was rewritten. Claude (Opus 5.5), for operator review.
- **v1.1 — 2026-07-08.** Modules #18 `RECURSIVE_IMPROVEMENT.md` and #19 `RUNBOOK_METHOD.md` added, with
  template mirrors. Claude (Fable 5).
- **v1.0 — 2026-04-28.** First complete blueprint: 17 modules, templates, worked example. Claude (Opus 4.7).
