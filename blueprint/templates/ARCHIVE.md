# ARCHIVE.md — Deletion + Provenance Protocol
## Classification: Tier 4

> When meaningful content is deleted, log it here. Saves future-you from
> "did I delete that on purpose, or was it a mistake?"

---

## When to archive

### Case 1 — Debug / error correction
**No archive needed.** Stub, empty file, typo, never-used scratch — just delete.

### Case 2 — Reorganization, supersession, removal of meaningful content
**Archive entry required.** Examples:
- Document being replaced by canonical version.
- Directory being collapsed into parent.
- Tool being deprecated.
- Multiple files being consolidated.
- Content being moved between classifications.

When in doubt: archive. Cost of an extra entry is low. Cost of a
deletion you can't reconstruct is real.

---

## Entry template

```markdown
## YYYY-MM-DD — [Short title for the deletion]

**Reason:** [1-3 sentences on why these files are being removed,
not just what they were.]

**Authority:** [Operator approved? Standing rule? Pre-approved pattern?]

**Relocated from:** `[path]` (if applicable)

### Deleted [Files / Directories]

**1. `[path/file_1]`** ([size, lines if relevant])
- [What it was]
- [Why being removed]
- [Key knowledge extracted, preserved elsewhere]

**2. `[path/file_2]`** ([size, lines])
- [Same structure]

### Not Deleted (Retained)

- [Path] — [why this superficially-similar file was kept]

_Signed: [operator initials or agent identity] — YYYY-MM-DDTHH:MM:SS-TZ_
```

---

## What goes in vs. doesn't

**In:**
- Reorganization deletions.
- Tool deprecations.
- Document supersession.
- Directory collapses.
- Bulk cleanups.

**Not in:**
- Routine debug edits.
- Renames (→ tool's `MAINTENANCE_LOG.md`).
- File moves within a tool's directory.
- Auto-generated artifacts.
- Sensitive content that can't be safely logged. (Log the *fact* of
  deletion without restating content.)

---

## Cross-reference protocol

When editing a doc whose previous content is now archived, the new doc
should say:

> *Earlier draft of [section]: see ARCHIVE.md, YYYY-MM-DD entry.*

Stops "where did the discussion of X go?" loops.

---

## Maintenance

- **At deletion time:** write the entry. Don't batch.
- **Quarterly:** re-read for the previous quarter. Patterns? Frequent
  reorganizations of the same area suggest a layout problem.
- **Annually:** consider partitioning by year (`ARCHIVE_2025.md`,
  `ARCHIVE_2026.md`) if file gets unwieldy.

---

## What this replaces

Without it, deletions live only in:
- Cloud-sync version history (times out).
- Git history (hard to grep semantically).
- Operator memory (unreliable).

The archive is a third source — durable, greppable, contextual.

---

_Signed: [your signature line] — [date]_
