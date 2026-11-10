# TASK_QUEUE.md — Standing Work Queue
## Classification: Tier 4

> Read at session start. Updated through the session.

---

## How this works

- **Before session:** Save and close all open `.md` files in your editor.
- **During session:** Tell agent what to change in chat. Don't edit `.md`
  files directly while agent is running.
- **Between sessions:** Edit freely. No conflict.
- **At session start:** Agent reads this file and reports what's next.
- **Tier 1** always priority. **Tier 2** when Tier 1 blocked or clear.
  **Tier 3** when both clear.
- **Operator can redirect anytime.**

---

## Status markers

| Marker | Meaning |
|---|---|
| `[ ]` | Open — not started |
| `[>]` | In progress |
| `[x]` | Done |
| `[~]` | Blocked (note why) |

A `[>]` task that hasn't moved in two weeks is actually `[~]` or `[ ]`.

---

## Three-tier model

### Tier 1 — Priority work
The work that pays the bills, ships product, or has a deadline.

### Tier 2 — Important but not urgent
Compounds in value over time. No hard deadline. Always tempting to skip.

### Tier 3 — Long-term / creative
Intrinsically rewarding but not commercially urgent. Overflow energy.

---

## Template entry

```markdown
- [>] **Task name**. One-line state. *(in progress YYYY-MM-DD — context)*
  - [ ] Sub-task 1
  - [x] Sub-task 2 *(done YYYY-MM-DD — outcome)*
  - [~] Sub-task 3 — blocked: reason
```

For larger tasks, use the full task brief from `GOVERNANCE.md`:

```markdown
- [ ] **Task:** [What needs to happen]
**Win:** [What success looks like]
**Inputs:** [Files, data, context]
**Gate:** [Where to review]
**Sensitivity:** [Tier 0–Tier 5]
**Notes:** [Constraints, prior decisions]
```

---

## Tier 1 — [Your priority work]

### [Project category 1]
- [ ] (your first task)

### [Project category 2]
- [ ] (your first task)

---

## Tier 2 — [Important but not urgent]

### [Category]
- [ ] (your first task)

---

## Tier 3 — [Long-term / creative]

### [Project]
- [ ] (your first task)

---

## Communication & Process Improvement

- [ ] Quarterly: review completed items — one-and-done or recurring?
- [ ] When this file passes ~500 lines, consider splitting by tier.
- [ ] Biweekly: scan for stale `[>]` markers (>2 weeks → demote / close).

---

## Maintenance

- Review at session start.
- Move completed items to `[x]` immediately. Don't batch.
- Biweekly: scan stale `[>]` items.
- Quarterly: meta-review.

---

_Signed: [your signature line] — [date]_
