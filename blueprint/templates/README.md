# Templates — Adoption-Ready Starter Files

> **Purpose.** Clean-name copies of every doc in the parent product
> directory, ready to copy into your own vault as starting points.
> Each template has the section structure intact and placeholders where
> operator-specific content goes.
>
> The full pedagogical version (with "why this section" commentary) is
> in the parent directory under the corresponding `LLMP001_..._<NAME>.md`
> filename.

---

## Adopt the templates

```bash
# From the LLM_Training_Products directory:
cp -r templates/ ~/your-vault/

# Then in your vault:
cd ~/your-vault/
# Rename per your own project mnemonic + dates per NAMING_CONVENTIONS.md
# Or keep clean names if your tooling expects them — your call.
```

---

## File-by-file

Read order matches the parent README. Read this list as your
adoption checklist:

| # | Template | What you do with it |
|---|---|---|
| 1 | `DIRECTIVE.md` | Fill in your identity, domain, working style. This becomes your auto-loaded contract. |
| 2 | `GOVERNANCE.md` | Adapt the Tier 0–5 audiences to your context. Customize the HITL gates. |
| 3 | `FOLDER_LAYOUT.md` | Adopt the directory pattern. Most operators use it as-is the first time. |
| 4 | `NAMING_CONVENTIONS.md` | Pick your project mnemonic family. Decide your sync-tag policy (LOCAL/SYNC/SHARE). |
| 5 | `MEMORY_SCHEMA.md` | Reference doc — the schema is fixed, you adopt it as-is. |
| 6 | `KNOWN_LIMITATIONS.md` | Re-read quarterly. Add your own observations as failure modes surface. |
| 7 | `SESSION_PROTOCOL.md` | The protocol is fixed; adapt the per-harness section to your tooling. |
| 8 | `TASK_QUEUE.md` | Empty template ready to fill with your Tier 1/2/3 work. |
| 9 | `MAINTENANCE_LOG.md` | Copy into every directory that has scripts. |
| 10 | `KNOWLEDGE_MANAGEMENT.md` | Reference doc — defines the "carved-in-stone" layer. Adopt as-is; populate `Knowledge_Management/` as processes get validated. |
| 11 | `DATA_SOURCES.md` | Replace example categories with your domain's data. |
| 12 | `INVENTORY.md` | Empty registry; populate as tools land. |
| 13 | `SESSION_ENV.md` | Set your initial cadence. Update last-run dates as you scan / review. |
| 14 | `LEARNING_LOG.md` | Empty by default; fills as the operator-agent partnership matures. |
| 15 | `SECURITY_AUDIT_LOG.md` | Empty by default; fills with each scan run. |
| 16 | `ARCHIVE.md` | Empty by default; fills with each meaningful deletion. |

---

## What's NOT a template

- `LICENSE` — Apache 2.0 license file. If you redistribute this
  methodology, retain attribution per the license. If you build your
  own original product on top, replace with your own license.
- The `LLMP001_..._<NAME>.md` files in the parent directory are
  pedagogical (the "why" commentary). Read those once; they're not
  meant to be copied into your vault.
- The `LLMP001_..._LESSONS_SINCE_V1.md` module (v1.2) has no template:
  its rules apply to the docs you already copied.

---

## After adoption

1. Read `KNOWN_LIMITATIONS.md` before investing heavily. The system has
   real limits; planning around them beats discovering them.
2. Set up your memory directory (path varies by harness — for Claude
   Code, it's auto-managed under your project's memory folder).
3. Pin `MEMORY.md` to your editor's quick-open. You'll touch it often.
4. Run your first session protocol within a week — even with empty
   memories, the rhythm establishes faster than you'd think.

---

_Apache 2.0 licensed. See parent directory `LICENSE` for full terms._
