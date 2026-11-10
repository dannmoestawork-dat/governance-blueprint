# Roadmap

**Governance Blueprint** grows by adding *pieces of the blueprint*. Each new tool is a new piece; improvements to an
existing tool are maintenance. This page tracks the shape, not dates.

## Released — Foundations
- **Navigator** — observe agents & codebase (working app).
- **In-State Governor** — governance compliance auditor (deterministic reference core).

## Candidate future pieces
These are directions, not commitments:

- **Governor — model-advisory layer.** Add an opt-in LLM layer for *interpretation* and *root-cause* on top of
  the deterministic core (every finding still `perceived` until human-confirmed). Includes a rule that audits
  the rule set itself for **internal contradiction** (rule-vs-rule), not just artifact-vs-rule.
- **Activity feed / observe verb.** A durable, queryable record of what scheduled agents actually did, so
  oversight doesn't require a live forensic dig. Both Navigator and Governor would consume it.
- **Owed-items tracker.** A structural home for "to-do / owed / next" items so they're closed, not narrated and
  forgotten (one of the most common drift classes in practice).
- **Recommendation ledger format (shared).** A standard, durable Accept/Reject/Defer ledger both tools emit, so
  decisions accumulate without ever erasing a prior call.
- **CI integrations.** Pre-commit / pipeline hooks that run Governor as a gate.

## Design constraints every piece must honor
- Mechanical core is the trust anchor; the model only advises ([Trust Model](./Trust-Model.md)).
- Local-first; no cloud dependency for core function.
- Observe & recommend; don't silently mutate the source of truth.
- File-based and legible; hand-off-able.

Contributions toward any of these are welcome — open an issue to discuss a piece before building it.
