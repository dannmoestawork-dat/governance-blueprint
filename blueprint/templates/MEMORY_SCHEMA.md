# MEMORY_SCHEMA.md — Persistent Cross-Session Memory
## Classification: Tier 4

> File-based memory that survives across conversations. Reference doc —
> the schema is fixed; adopt as-is.

---

## The schema

```
<memory_root>/
├── MEMORY.md                              ← Index (always loaded — under 200 lines)
├── user_<topic>.md                        ← Operator profile
├── feedback_<topic>.md                    ← Behavioral guidance
├── project_<topic>.md                     ← Active project context
├── reference_<topic>.md                   ← External-resource pointers
└── domain_<topic>.md                      ← (optional) domain-knowledge anchors
```

---

## The four types

### `user`
Operator role, goals, preferences, knowledge level. Helps agent tailor
behavior.

### `feedback`
Guidance on how to approach work — what to avoid AND what to keep doing.
Body structure: **Rule** → **Why** → **How to apply**.

Save when: the operator corrects OR confirms a non-obvious approach.

### `project`
Ongoing work context not derivable from code or git. Convert relative
dates ("Thursday") to absolute (`YYYY-MM-DD`).

Body structure: **Fact / decision** → **Why** → **How to apply**.

### `reference`
Pointers to external systems (Linear, Slack, Grafana, internal wikis).

### `domain` (optional)
Long-lived domain-knowledge anchors. Use sparingly.

---

## Frontmatter (required)

```markdown
---
name: {{memory name}}
description: {{one-line description — used to decide relevance, be specific}}
type: {{user, feedback, project, reference, domain}}
---

{{content — feedback/project structured as: rule/fact, then **Why:** and **How to apply:** lines}}
```

Specific descriptions matter. "Background tasks" rarely matches; "never
sign off with background tasks running — they orphan and don't surface
errors" does.

---

## The index — `MEMORY.md`

Always-loaded entry point. Index, not memory. Each entry one line, under
~150 chars:

```markdown
- [Title](file.md) — one-line hook
```

Hard rules:
- No frontmatter on `MEMORY.md`.
- Never write memory content directly into the index.
- Keep under 200 lines (auto-load truncation).
- Organize by topic, not chronology.
- **Specific hooks save tokens.** Vague hooks make the agent open every
  file unnecessarily. Tight, distinctive descriptions let the agent
  decide relevance from the index alone.

---

## When to read memory

- When relevant to the current task.
- When the operator references prior conversations.
- When the operator explicitly asks.

When NOT: operator says "ignore memory"; memory contradicts observable state.

---

## When to write memory

| Situation | Save? | Type |
|---|---|---|
| Operator corrects approach | Yes | feedback |
| Operator confirms non-obvious choice | Yes | feedback |
| Learn role / preferences | Yes | user |
| Learn external system | Yes | reference |
| Learn project motivation | Yes | project |
| Finished writing code | No | (the code is its own record) |
| Learned a code pattern | No | (derive on demand) |
| Found a bug | No | (commit message is the record) |
| Routine task done | No | |
| Conversation summary | No | |

---

## What NOT to save (even if asked)

- Code patterns / file paths / architecture (derivable from project state)
- Git history (use `git log`)
- Debug solutions (the fix is in the code)
- Anything in `DIRECTIVE.md`
- Ephemeral task details

If the operator asks to save a recent-activity list, redirect: *what was
surprising or non-obvious about it?* That's the part worth keeping.

**Exception — operator testing the schema.** When the operator is
deliberately probing the agent's memory rules (system build, audit,
training a new collaborator), state the redirect rule out loud, then
honor the explicit request. Surface the boundary; don't bypass it
silently.

---

## When to update or forget

- **Wrong:** update the file.
- **Outdated:** *capture history before deletion.* Record what the memory
  said, when it was true, why it's stale, what supersedes it — either
  to `ARCHIVE.md` or in the new memory's body. Then delete file + index
  pointer.
- **Operator says "forget that":** **first, confirm WHAT.** The agent
  restates the entry it's about to delete and waits for explicit
  confirmation. Once confirmed, capture history per the rule above,
  then delete. Wrong deletion is irreversible.

Memory ages. A 6-month-old "we're using Postgres 14" may be wrong now.
Before recommending action based on memory:
- File path? Verify the file exists.
- Function / flag / string? **Search the codebase for it** (editor's
  project-wide search, or `grep` / `rg` from the terminal — find every
  place the named thing appears).
- Operator about to act on the recommendation? Verify first.

"Memory says X exists" ≠ "X exists now."

---

## Memory vs. other persistence

| Mechanism | Lives | Use for |
|---|---|---|
| Conversation context | This session | What we just discussed |
| Plan / approach | This session | Multi-step proposed work |
| Task list | This session | In-progress sub-tasks |
| **Memory** | Across sessions | **Stable facts useful in future conversations** |
| `MAINTENANCE_LOG.md` | Per-tool, durable | Tool-specific decisions |
| `Knowledge_Management/` | Cross-session, validated | Carved-in-stone processes |
| Code | Forever | Behavior |

---

## Curation discipline

1. **Create as many sub-memory files as needed.**
2. **Improve memory processes when context is lost.**
3. **Confirm all chains to root remain intact.** Every memory should
   trace back to a load-bearing principle, doc, or established pattern.
   Step counts may change; context may be refined; **but no gaps to root.**

All three matter. Without (1), files become catch-alls. Without (2),
broken patterns persist. Without (3), references rot quietly until the
chain breaks under load.

---

## Token economics

`MEMORY.md` is auto-loaded — paid every turn. **Topic files** (the
individual `feedback_*.md` / `project_*.md` / `user_*.md` /
`reference_*.md` / `domain_*.md` files in your memory directory) are
loaded *only when relevant* — effectively free until used. Push detail
into topic files. Keep the index lean.

---

## Adoption checklist

1. Create the memory directory (path varies by harness).
2. Initialize empty `MEMORY.md` with section headers.
3. Add Section 9 to `DIRECTIVE.md` pointing the agent at the directory.
4. Save memories one at a time. Don't seed in bulk.
5. Curate every few weeks: prune stale, tighten vague descriptions.

---

_Signed: [your signature line] — [date]_
