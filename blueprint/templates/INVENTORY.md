# INVENTORY.md — Tool & Asset Registry
## Classification: Tier 4

> Catalog of every tool, script, database, generated output. Update
> whenever a tool is created or changes significantly.

---

## Maintenance rule

A tool not in `INVENTORY.md` is, for navigation purposes, invisible.
Update during the session that creates / modifies / removes the tool.

---

## Template entry

```markdown
### N.M [Tool Name]
| Field | Value |
|---|---|
| **Script** | `path/to/main_script.py` |
| **Purpose** | (1-3 sentences) |
| **Inputs** | (files, data, configuration) |
| **Outputs** | `path/to/output.xlsx` |
| **Venv** | `path/to/.venv/` |
| **Dependencies** | `lib==X.Y.Z, lib2==X.Y` |
| **Run** | `.venv/Scripts/python main_script.py [args]` |
| **Status** | (active / v1 complete / in development / deprecated) |
```

Optional fields when relevant:
- **Key functions** — for libraries the operator imports.
- **Security** — special handling notes.
- **Commands** — for tools with subcommands.
- **External dependencies** — services, APIs, hardware.

---

## Suggested structure

```markdown
## 1. Client/Customer-Facing Tools (Tier 1)
   1.1 [tool]

## 2. Internal Tools (Tier 1)
   2.1 [tool]

## 3. Tier 2 Tools

## 4. Databases
   (one row per durable database file)

## 5. Generated Documents (Outputs)
   (one row per typical generated artifact)

## 6. Reference Data (Read-Only)
   (pointers — full detail in DATA_SOURCES.md)

## 7. Governance & Documentation Files
   (DIRECTIVE, GOVERNANCE, FOLDER_LAYOUT, etc.)

## 8. Research / No Code Yet
   (planned tools — clearly labeled)

## 9. Python (or other language) Environments
   (one row per venv with location, tools served, key pinned versions)

## 10. Infrastructure
   (servers, sync providers, monitoring, CI)

## 11. Tier 3 — Creative Projects
   (separate to keep Tier 1/2 working areas tight)
```

---

## Per-tool README pattern

For non-trivial tools, the inventory entry points at a per-tool README:

```
Tools/[Tool_Name]/
├── .venv/
├── requirements.txt
├── MAINTENANCE_LOG.md         ← decisions / errors / handoff
├── README.md                  ← user guide (one-page max)
├── [main_script].py
└── output/
```

Inventory says *what it is*. README says *how to run it*.
MAINTENANCE_LOG says *why*.

---

## What NOT to put here

- Conversation context → `MEMORY.md`
- Per-tool decision history → that tool's `MAINTENANCE_LOG.md`
- External data sources → `DATA_SOURCES.md`
- Active task status → `TASK_QUEUE.md`

---

## Anti-patterns

- The wishlist (tools that don't exist as if they do) → use Section 8
  and label clearly.
- The marketing description ("This sophisticated tool...") → state what
  it does; one sentence; move on.
- The stale inventory (path renamed but inventory not updated) → worse
  than no inventory; misdirects.

---

## Maintenance

- **End-of-session:** if tool changed, update.
- **Monthly:** spot-check 3 random entries against actual file state.
- **Quarterly:** trim deprecated entries; promote built tools out of
  Section 8.

---

_Signed: [your signature line] — [date]_
