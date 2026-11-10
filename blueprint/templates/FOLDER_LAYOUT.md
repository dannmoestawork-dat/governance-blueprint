# FOLDER_LAYOUT.md — Vault Directory Pattern
## Classification: Tier 4

> The directory shape. Adopt the lifecycle ramp; customize categories to
> your domain.

---

## The shape

```
<vault_root>/
│
├── DIRECTIVE.md                          ← Auto-loaded contract
├── GOVERNANCE.md                         ← Tier 0–5 + HITL gates
├── FOLDER_LAYOUT.md                      ← THIS FILE
├── NAMING_CONVENTIONS.md
├── MEMORY_SCHEMA.md
├── KNOWN_LIMITATIONS.md
├── SESSION_PROTOCOL.md
├── TASK_QUEUE.md
├── INVENTORY.md
├── DATA_SOURCES.md
├── LEARNING_LOG.md
├── SECURITY_AUDIT_LOG.md
├── SESSION_ENV.md
├── ARCHIVE.md
│
├── Production/                           ← THE LIFECYCLE
│   ├── _io/                              ← Inflow / outflow buffers
│   │   ├── OPR_io/                       ← (rename to your initials)
│   │   │   └── Project_Details/
│   │   └── outbox_from_code/
│   │
│   ├── Pipeline/                         ← Work-in-progress
│   │   ├── Project_Pre_Plan/
│   │   ├── Outreach/
│   │   └── Sub_Templates/
│   │
│   ├── Active_Projects/                  ← READY-TO-SHIP
│   │   └── <project_name>/
│   │
│   ├── CRM/                              ← Relationship hub (if relevant)
│   │   ├── Companies/
│   │   ├── Contacts/
│   │   ├── Projects/
│   │   ├── _templates/
│   │   ├── _views/
│   │   └── output/
│   │
│   └── Reference/                        ← Read-only inputs
│       ├── <Reference_Database>/
│       ├── <Tool_Outputs>/
│       └── <External_Source_Data>/
│
├── Tools/                                ← INTERNAL / IN-DEVELOPMENT
│   ├── <Tool_001>/
│   │   ├── .venv/
│   │   ├── requirements.txt
│   │   ├── MAINTENANCE_LOG.md
│   │   ├── <main_script>.py
│   │   └── output/
│   ├── shared_lib/
│   └── _ARCHIVED_<old_tool>/
│
├── Knowledge_Management/                 ← Validated processes
│   ├── KM_INDEX.md
│   ├── session_protocol.md
│   └── approved_security_patterns.md
│
├── Code_Review/                          ← Wiki-style audit trail
│   ├── REVIEW_LOG.md
│   ├── WIKI.md
│   ├── patterns/
│   ├── rubrics/
│   └── spec_gaps/
│
├── Architecture/                         ← System docs
└── Personal_Outside_Work/                ← Out-of-scope
```

---

## The lifecycle ramp

```
_io/  →  Pipeline/Project_Pre_Plan/  →  Active_Projects/  →  (delivered)
```

| Stage | Directory | Meaning |
|---|---|---|
| Inflow | `_io/<Operator>_io/Project_Details/` | Raw inputs, unprocessed |
| Pre-plan | `Pipeline/Project_Pre_Plan/<project>/` | Working draft |
| Active | `Active_Projects/<project>/` | Packaged for external send |
| Out the door | (delivered) | Archive on completion |

A project lives in `Active_Projects/` only when its tools are reliable
enough to send externally. Tool development on the tools themselves
lives in `Tools/`.

---

## Three views

1. **By Folder** — annotated tree (above)
2. **By Workflow** — "I want to do X → go here"
3. **Data Flow** — which tool feeds which

Workflow table template:

| I want to... | Go here |
|---|---|
| See open tasks | `TASK_QUEUE.md` |
| See what tools exist | `INVENTORY.md` |
| Understand the project | `DIRECTIVE.md` + this file |
| Find a finished deliverable | `Production/Active_Projects/<project>/` |
| Look up a reference | `Production/Reference/<system>/` |
| Find a validated process | `Knowledge_Management/KM_INDEX.md` |
| Check governance | `GOVERNANCE.md` |
| Review code quality | `Code_Review/WIKI.md` |

---

## Per-tool directory anatomy

```
Tools/<Tool_Name>/
├── .venv/
├── requirements.txt
├── MAINTENANCE_LOG.md
├── <main_script>.py
├── helpers/
├── tests/
├── output/
└── README.md (optional, for non-trivial tools)
```

---

## Naming on folders

- Underscores between words: `My_Project/`, not `My Project/`.
- No special characters. Stick to `[A-Z][a-z][0-9][_]`.
- Project mnemonic prefix for project subfolders: `RTK014_Example_Project/`.
- Sync state on folders inherits from the most-restrictive child file.

---

## Maintenance

- Update when a top-level directory is added or data flow changes.
- Don't update for routine file additions inside tools.
- Sign and date in `ARCHIVE.md` when deleting/moving substantial sections.

---

_Signed: [your signature line] — [date]_
