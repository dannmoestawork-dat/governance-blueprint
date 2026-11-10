# LEARNING_LOG.md — Terminology Corrections + Communication Patterns
## Classification: Tier 4

> Two things: terminology operator is learning, communication patterns
> between operator and agent. Both sides learn here.

---

## Section 1 — Active Corrections

Terminology being learned. Live entries. Mastered entries → Retired.

```markdown
### [Term]
- **What the operator said:** "[verbatim quote]" (YYYY-MM-DD)
- **Correction:** [Why this term is being misapplied. Intent often correct;
  technical word is the issue.]
- **Key terms to know:**
  - **[term 1]** — [definition]
  - **[term 2]** — [definition]
- **Key clarifications:**
  - [Important nuance.]
```

---

## Section 2 — Reference Glossary

Curated definitions. Quick lookup. Only terms that came up in conversation.

Suggested sub-sections (adapt to your domain):
- Files / Code
- Project Organization
- File Types
- API / Cloud
- Hardware / OS
- Architecture
- Monitoring / Automation
- Domain-specific

---

## Section 3 — Retired Corrections

Mastered terminology. Historical record + evidence the system teaches.

```markdown
### [Term]
- **First correction:** YYYY-MM-DD
- **Mastered:** YYYY-MM-DD
- **Distinction:** [The key insight that stuck.]
```

---

## Section 4 — Communication Patterns — What Works

Two-way patterns. Operator notices what agent does well/poorly; agent
notices what operator does well/poorly. Both logged.

### Operator strengths

```markdown
- **[Pattern]:** [What operator does. Why it helps.]
```

### Operator growth areas

Only logged if operator asks for it. Don't unilaterally write a "things
you do wrong" list.

### Agent improvements

Operator feedback on agent. Promoted to feedback memories when durable.

```markdown
- **YYYY-MM-DD — [Issue]:** [What happened. What operator wants instead.
  (If durable, promoted to `feedback_<topic>.md`.)]
```

### File safety patterns

```markdown
- **Save and close .md files before sessions.**
- **Use [diff/preview feature] before accepting large rewrites.**
- **Cloud-sync version history is last-resort recovery, not durability.**
```

---

## Why this isn't memory

- Learning_Log is the *first place* corrections / feedback get written.
- Memory is where *durable* corrections get promoted.

Log is the staging area. Memory is the long-term store. When in doubt:
log first, promote if it recurs.

---

## Maintenance

- **Active Corrections:** review monthly. Move mastered → Retired.
- **Reference Glossary:** add as terms come up. Don't seed in bulk.
- **Communication Patterns:** review quarterly. Stable patterns →
  candidate feedback memories.

---

_Signed: [your signature line] — [date]_
