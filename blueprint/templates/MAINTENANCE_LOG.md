# MAINTENANCE_LOG.md — [Tool Name]
## Classification: Tier [N]
## Started YYYY-MM-DD

> Per-tool decision log. Copy this template into every directory that
> contains scripts. Update during development, not just at the end.

> **Not a git substitute.** Git records *what changed and when*; the
> MAINTENANCE_LOG records *why things are the way they are*. They
> complement each other. The methodology works whether or not you use
> git — this log is durable on its own.

---

## Error Log

| Date | Issue | Root Cause | Resolution |
|------|-------|-----------|------------|
| YYYY-MM-DD | (one-line description) | (cause) | (fix or workaround) |

What goes here:
- Bugs that took >15 minutes to diagnose.
- Errors that surfaced architectural problems.
- Workarounds and the reason they were needed.

What doesn't:
- Routine syntax errors. Typos.

---

## Script & Approach Reasoning

### YYYY-MM-DD — [Decision name]
[AI-GENERATED] — [signature]

[2-5 sentences. Why this approach. What alternatives. Why this won.]

What goes here:
- "Considered X, Y, Z. Picked Y because [reason]."
- Why a "weird" library / pattern choice.
- Why this file is structured this way and not the obvious other way.

What doesn't:
- Standard well-known patterns.
- Restating what the docstring says.

---

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| (lib)   | (X.Y.Z) | (why needed) |

**Venv location:** `[path]/.venv/`
**System dependencies:** [if any — imagemagick, ffmpeg, etc.]

---

## Session Handoff Notes

### YYYY-MM-DD — [Session summary]
[AI-ASSISTED] — [signature]

- **Completed:** [what's done]
- **In progress:** [what's next]
- **Blocked on:** [if anything]
- **Most important thing for next session:** [one line]

---

## Rules

- **Create when first script is written.** Don't wait.
- **Update during development**, not just at the end.
- **Tag entries** `[AI-GENERATED]` / `[AI-ASSISTED]` / `[VERIFIED]`.
- **Keep concise.** Decision log, not narrative.
- **Date every entry.** ISO format.
- **Sign every entry.**

---

## Anti-patterns

- The narrative log. "Today I worked on..." → useless.
- The omniscient log. "Of course we picked X." → spell it out.
- The TODO list. → use `TASK_QUEUE.md`.
- The marketing doc. → state what was built and why. No fluff.
- The silent log. No entries between releases. → context decays. Update during.
