# SESSION_PROTOCOL.md — Start/End Loops
## Classification: Tier 4

> The routine the agent runs at the start and end of every session.

---

## Start of session — 8 steps

The agent runs these in order, unannounced.

1. **Read the directive.** `DIRECTIVE.md` (or your harness's auto-load
   file). Free if auto-loaded.
2. **Read memory index.** `MEMORY.md`. Note scope; don't load topic
   files yet.
3. **Load relevant topic files.** Based on the operator's first message.
4. **Read TASK_QUEUE.** What's open / in-progress / blocked.
5. **Read SESSION_ENV recurring-maintenance checklist.** Surface anything
   overdue. Don't *do* the maintenance; surface it.
6. **Confirm what's next.** Restate to the operator what's in progress
   and what's overdue. Get redirect or confirmation.
7. **Resolve open conflicts before acting.** If memory says one thing
   and current state says another, flag the conflict before proceeding.
8. **Begin the work.** Only after 1–7.

---

## During session — standing rules

### Plain-language proposal before code
For tasks >5 min: brief the operator first (scope, approach, success,
estimate). Wait for approval. Then execute.

### Fail twice → flag and propose alternatives
Don't iterate on a broken approach indefinitely. Two failures = stop,
explain, propose 2–3 paths, let operator pick.

### Three gates before acting on memory
1. **Ask gate** — verify against current state before answering recall
   questions.
2. **Save gate** — confirm inference matches reality before saving.
3. **Cold-read gate** — scan topic files against current evidence; don't
   blindly cite outdated content.

---

## End of session — 5 steps

Run before sign-off. Don't skip.

1. **Update MEMORY topic files.** Anything new that fits user / feedback
   / project / reference. Update the index pointer. Durable facts only.
2. **Update TASK_QUEUE.** Move tasks: `[ ]` → `[>]` → `[x]` → `[~]`
   (with reason). Add new tasks discovered.
3. **Update SESSION_ENV log.** Add a context-evolution entry. Update
   last-run dates on completed maintenance items. Skimmable in 60 seconds.
4. **Update per-tool MAINTENANCE_LOG.** Errors, reasoning for non-trivial
   choices, dependency changes, handoff notes.
5. **Confirm clean state.** Background tasks running? Unsaved files?
   Surface before signing off.

---

## What "session start hot" looks like

After good end-of-session protocol, tomorrow:

- Agent loads directive (auto).
- Reads `MEMORY.md` — sees yesterday's "in progress" topic file.
- Loads relevant memories.
- Reads `TASK_QUEUE` — sees the `[>]` from yesterday.
- Reads `SESSION_ENV` — sees yesterday's evolution log.
- Says: "Yesterday we were on X, status Y. Z is overdue. Continue X?"

~60 seconds. No re-briefing.

---

## Failure modes

- Skipping end-of-session.
- Index bloat past truncation.
- Vague memory entries.
- Conversation transcripts in memory files.
- Maintenance items slipping past cadence.

---

## Per-harness adaptation

| Harness | Auto-loaded |
|---|---|
| Claude Code | `CLAUDE.md` and `MEMORY.md` index |
| Cursor / Cline | varies — check config |
| Custom agent | whatever your loader does |

If your harness auto-loads, those steps are free. Protocol still applies.

---

_Signed: [your signature line] — [date]_
