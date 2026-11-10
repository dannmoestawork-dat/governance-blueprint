# The Trust Model

One idea underlies every Governance Blueprint tool:

> **Structure enforces. The model only narrates. Verify the artifact, never the narration.**

## The unreliable narrator

A language model is a fluent generator, not a reliable reporter of fact. It can describe work it never did in
prose indistinguishable from a true report. So a model's *account* of an outcome carries no evidentiary
weight. Only the **artifact** — the file on disk, the row in the database, the exit code — is evidence.

This is not a knock on any particular model; it is a structural property of using a probabilistic generator
inside a deterministic system. The correct response is architectural.

## The split

Every tool divides into two layers with strict roles:

| Layer | Role | Trust |
|-------|------|-------|
| **Mechanical core** | Deterministic checks: does the file exist? does the link resolve? does the header match? did the gate pass? | **Authoritative.** This decides pass/fail. |
| **Model layer** | Interpretation, summary, recommendation — the things determinism can't do. | **Advisory only.** Output is labeled `perceived` and is not acted on until a human confirms it. |

The mechanical core is the **trust anchor**. The model can make the system *smarter*; it can never make it
*decide*.

## Consequences for design

- **A gate that can only pass proves nothing.** Every deterministic check ships with adversarial tests that
  assert it *catches* a seeded violation as well as *passes* a clean case. (See each tool's `tests/`.)
- **Findings are recommendations, not actions.** Tools observe and write to a durable, human-decided ledger
  (Accept / Reject / Defer). They don't silently mutate your source of truth.
- **Reconcile to reality, not to the last record.** Because records drift, a belief about system state must be
  re-derived from the live artifact, not copied forward.
- **`perceived` until confirmed.** Any model-authored text is marked as such and earns durability only when a
  human ratifies it.

This is also why the tools are valuable as a *handoff*: a deterministic, file-based, gated process is
something you can give to another person or team and have them trust it — in a way that "we asked a model and
it seemed right" never is.
