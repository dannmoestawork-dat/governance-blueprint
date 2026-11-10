# KNOWLEDGE_MANAGEMENT.md — Validated Processes, Carved In Stone
## Classification: Tier 4

> The "carved in stone" layer. Validated processes that have been used
> enough times to be canonical. Distinct from memory (provisional),
> MAINTENANCE_LOG (per-tool), and code-review wiki (audit-time).

> **KM vs. `GOVERNANCE.md`.** Both are operator-signed and durable, but
> they govern different things. **`GOVERNANCE.md` = the rulebook**
> (classification tiers, HITL gates, what's allowed). **KM = the
> validated processes the rulebook authorizes** (how you actually do
> session protocols, runbooks, pricing, variance validation). Peers,
> not overlaps — constitution vs. operations manual.

---

## What belongs in KM

A KM entry meets all five:

1. **Validated through use.** N successful applications, not "we should."
2. **Generalizable.** Applies beyond a single tool / project.
3. **Stable.** Shape isn't changing every session.
4. **Operator-signed.** Explicit promotion.
5. **Portability resolved.** Either harness-agnostic (preferred), or
   harness-bound *with explicit dependencies named at the top of the
   file*. The criterion guards against hidden lock-in, not against
   tooling-specific work.

Examples: session protocol, pricing model, variance protocol, approved
security patterns, deployment runbook, gitignore standard.

## What does NOT belong

- Anything still being figured out → memory or MAINTENANCE_LOG.
- Tool-specific decisions → that tool's MAINTENANCE_LOG.
- Code idioms → `Code_Review/patterns/`.
- Session ephemera → conversation / task list.

If unsure: don't promote. Friction is the feature.

---

## Promotion gate

1. **Use validation.** N successful applications (you pick N — typically 3–5).
2. **Generality check.** Applies beyond original context?
3. **Stability check.** Stopped changing session-to-session?
4. **Operator sign-off.** Status moves `[DRAFT]` → `[CONFIRMED-BY-OPERATOR]`.
5. **Index entry.** One-line pointer in `KM_INDEX.md`.

Demotion is legitimate. `[CONFIRMED]` → `[DRAFT]` if it fails under load.

---

## Directory shape

```
Knowledge_Management/                 ← or shorter: KM/
├── KM_INDEX.md                       ← always-loaded index
├── session_protocol.md
├── variance_protocol.md
├── pricing_model.md
├── approved_security_patterns.md
└── ...
```

---

## File format

```markdown
# [Process name]
## Classification: Tier [N]
## Status: [DRAFT | CONFIRMED-BY-OPERATOR]
## Confidence: [DRAFT | VALIDATED | EXTERNALLY-REVIEWED]

### What This Is
[1-3 sentences.]

### Why This Exists
[Trigger / motivation.]

### Source / How We Know
[Validation trail.]

### The Process
[Step-by-step. Numbered. Reproducible.]

### When To Apply
[Triggering conditions.]

### Opposing Steel Man
[Strongest case AGAINST. The cost. Honest acknowledgment.]

### Maintenance
[When to revisit.]

---

_Signed: [operator] — [date promoted]_
```

The **opposing steel man** is load-bearing. Validated processes that
don't acknowledge their cost ossify and rot.

---

## `KM_INDEX.md` format

```markdown
# KM_INDEX.md — Validated Processes

- [Session Protocol](session_protocol.md) — start/end-of-session loops
- [Variance Protocol](variance_protocol.md) — N-run repeatability
- [Pricing Model](pricing_model.md) — pricing formula
- [Approved Security Patterns](approved_security_patterns.md) — standing exceptions
```

Same hygiene as `MEMORY.md`: under ~150 chars per line, organize by topic.

---

## How KM relates to other layers

| Vs. | Difference |
|---|---|
| **Memory** | Memory = *consider when relevant*. KM = *the way you work*. |
| **MAINTENANCE_LOG** | Log = *why this tool*. KM = *how all tools of this class get built*. |
| **Code-review wiki** | Wiki = *patterns recognized in audit*. KM = *processes followed deliberately*. |
| **DIRECTIVE.md** | Directive = *contract*. KM = *processes the contract authorizes*. |

---

## Anti-patterns

- **Premature promotion.** Marking `CONFIRMED` after one use.
- **The kitchen sink.** >30 entries in the index = over-promotion.
- **Carved-and-forgotten.** Quarterly relevance scan in `SESSION_ENV.md`.
- **Contract substitute.** Governance rules belong in `GOVERNANCE.md`.

---

## Maintenance

- **At promotion:** add to `KM_INDEX.md`, write file, sign, date.
- **Quarterly:** scan for unreferenced entries. Demote candidates.
- **On load failure:** demote to `[DRAFT]`, fix, re-validate.
- **Cross-reference both ways** with related memory and wiki entries.

---

_Signed: [your signature line] — [date]_
