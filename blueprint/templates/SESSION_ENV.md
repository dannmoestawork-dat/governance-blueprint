# SESSION_ENV.md — Recurring Maintenance Cadence + Context Evolution Log
## Classification: Tier 4

> Track recurring maintenance + system evolution. The evolution log
> captures memory additions, KM entries (see `KNOWLEDGE_MANAGEMENT.md`),
> governance updates, protocol changes, tool integrations.

---

## Recurring Maintenance Checklist

Standing tasks with cadence + last-run dates. Agent checks at session start.

| Item | Cadence | Last Run | Next Due |
|---|---|---|---|
| Secrets / credentials scan | Weekly | YYYY-MM-DD | YYYY-MM-DD |
| Full security scan | Monthly | YYYY-MM-DD | YYYY-MM-DD |
| MEMORY.md line count check (<200) | Every session | YYYY-MM-DD | next session |
| Memory index review (descriptions, staleness) | Monthly | YYYY-MM-DD | YYYY-MM-DD |
| LEARNING_LOG active corrections review | Monthly | YYYY-MM-DD | YYYY-MM-DD |
| INVENTORY.md accuracy spot-check | Monthly | YYYY-MM-DD | YYYY-MM-DD |
| TASK_QUEUE.md stale `[>]` items | Biweekly | YYYY-MM-DD | YYYY-MM-DD |
| KNOWN_LIMITATIONS.md re-read | Quarterly | YYYY-MM-DD | YYYY-MM-DD |
| Per-tool MAINTENANCE_LOG sync | Quarterly | YYYY-MM-DD | YYYY-MM-DD |
| Folder layout drift check | Quarterly | YYYY-MM-DD | YYYY-MM-DD |

**Adapt to your domain.** Some items may not apply; others may need adding.

**Cadence rule of thumb:**
- *Weekly:* high-frequency, low-effort.
- *Monthly:* periodic hygiene that keeps the system from rotting.
- *Quarterly:* strategic re-reads that catch slow drift.

---

## Context Evolution Log

Add entries chronologically (newest first). Skip routine work — reserve
for new infrastructure, new patterns, load-bearing decisions.

### Template

```markdown
### YYYY-MM-DD — [Short title]

[2-4 sentence summary.]

- **What changed (1):** [thing 1, with paths]
- **What changed (2):** [thing 2]
- **Why:** [trigger / motivation]
- **New memories saved:** [topic files]
- **Files affected (new):** [paths]
- **Files affected (updated):** [paths]
- **Lessons:** [1-3 numbered]
```

---

## Why one file

The maintenance checklist and the evolution log could be separate; they
aren't. Both surface routine hygiene that compounds. One file = one thing
to read at session start. Cross-references stay tight.

If file gets unwieldy (~1000+ lines): extract older log entries to a
dated archive (`SESSION_ENV_2025.md`). Keep checklist + recent 3-6 months here.

---

## Maintenance

- **Every session:** check the checklist; update last-run dates on
  completed items.
- **At significant milestones:** write an evolution log entry.
- **Quarterly:** review the cadence list itself — still right? Add /
  remove items.

---

## What NOT to put here

- Conversation summaries → not durable enough.
- Per-tool decision logs → that tool's `MAINTENANCE_LOG.md`.
- Open questions → `TASK_QUEUE.md`.
- Operator profile → `MEMORY.md` user-type topic files.

---

_Signed: [your signature line] — [date]_
