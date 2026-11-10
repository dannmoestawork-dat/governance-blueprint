# DIRECTIVE.md — Auto-Loaded Operator Contract
## Classification: Tier 5

> Auto-loaded by the agent at every session start. Replace placeholders
> with your specifics. Keep under ~200 lines.

---

## 1. Operator Identity
- **Operator:** [your name]
- **Role:** [what you do]
- **Domain:** [your field]
- **Core objective:** [one sentence on what you want the agent to help you accomplish]
- **Philosophy:** [your operating principle]

## 2. Repository Layout
- Project-specific context lives in each project's directory
  (`MAINTENANCE_LOG.md`, `PROJECT_CONTEXT.md`, or equivalent).
- Reference data is indexed in `DATA_SOURCES.md`.
- Agent-spawned work should reference project docs, not this file.

## 3. Provenance & Attribution
Tag all generated content:
- **[AI-GENERATED]** — File or draft created entirely by an LLM.
- **[AI-ASSISTED]** — Human edited the AI's initial output.
- **[VERIFIED]** — Operator has technically reviewed for accuracy.

## 4. Operational Guardrails
- **Data Privacy:** Redact personal identifiers before any external output.
- **Source of Truth:** External claims must cross-reference primary sources.
  Substantive truth over surface polish. Always.
- **Scope:** Read and write within `[your_vault_root]/` and its subdirectories
  only. Do not access parent directories or unrelated personal files.

## 5. Tooling
- **PDFs:** [your PDF reading tool]
- **Spreadsheets:** [Python + openpyxl / pandas / etc.]
- **Archives:** Extract zips to a temp directory before processing.
- **System interpreter:** [your version, e.g., `python3.12`]

## 6. Maintenance Log Protocol
Every directory with scripts must include a `MAINTENANCE_LOG.md` with:
1. **Error Log** — Date-stamped errors, root causes, resolutions.
2. **Script & Approach Reasoning** — Why each script exists, alternatives.
3. **Dependencies** — Libraries, versions, install locations.
4. **Session Handoff Notes** — End-of-session summary and next steps.

Rules: Create when first script is written. Update during development. Tag
entries per Section 3. Keep entries concise.

## 7. Code Environment Protocol
- Always use a virtual environment (`.venv/`) per project directory.
- Pin dependencies in `requirements.txt` with exact versions.
- All packages from default upstream registries. No custom mirrors without
  explicit approval.

## 8. Working Style
- **Take your time.** Correctness over speed.
- **Be curious and ask questions,** even tangential ones.
- **Propose your approach in plain language before writing code.**
- **When something fails twice, flag it and propose alternatives.**
- **Update audit / review docs alongside the tools they cover.** Don't
  let documentation drift behind code.
- **Build for portability.** Confirm code and schemas don't lock in to a
  single provider, format, or environment. Anti-fragility.
- **Prioritize sense-making in all tasks.**

## 9. Session Memory Protocol
- **Start of session:** Read `MEMORY.md` to restore context.
- **End of session (or at milestones):** Update `MEMORY.md`.
- **Missing memory directory:** Create it and initialize. Never silently skip.
- **Size limit:** `MEMORY.md` under 200 lines (auto-load truncation).
  Use separate topic files for detail.
- **Content:** Stable facts only. Not session chatter.

## 10. Edit Protocol
This file is edited by both Operator and LLMs. Sign new entries.
For deletions to reorganize, copy deleted lines to `ARCHIVE.md` with
signature and timestamp before proceeding.

## 11. Naming Convention
This vault uses the bracket-token convention:
`[Project][DATE][VERSION][Folder-SyncTag][Etc].ext`
See `NAMING_CONVENTIONS.md`. `README.md`, `LICENSE`, and tooling-canonical
files keep their canonical names.

## Related Files
- `TASK_QUEUE.md` — Standing work queue (Tier 1/2/3).
- `LEARNING_LOG.md` — Terminology + communication patterns.
- `DATA_SOURCES.md` — Reference data index.
- `GOVERNANCE.md` — Tier 0–5 + HITL gates.
- `FOLDER_LAYOUT.md` — Directory structure.
- `NAMING_CONVENTIONS.md` — Filename pattern.
- `MEMORY_SCHEMA.md` — Cross-session memory architecture.
- `KNOWN_LIMITATIONS.md` — What doesn't work yet, why, mitigations.
- `SESSION_PROTOCOL.md` — Start/end loops.
- `SESSION_ENV.md` — Recurring-maintenance cadence.
- Project context: each project directory has its own `MAINTENANCE_LOG.md`.
- Auto-memory: every project has a `MEMORY.md` in its harness-specific
  memory directory. Create if missing.

---

_Signed: [your signature line] — [date]_
