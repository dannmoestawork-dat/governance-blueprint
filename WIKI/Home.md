# Governance Blueprint · Wiki

Local-first, open-source tools for **governing and overseeing AI agents**.

When you stop chatting with a model and start letting agents *do work* across your codebase, you need a layer
that watches the agents and keeps them honest. Governance Blueprint is that layer. **Foundations** is the first
release.

## The two oversight questions

| Question | Tool |
|----------|------|
| *Are the agents doing good work?* | **[Navigator](./Navigator.md)** — observe |
| *Is everyone following the rules we set?* | **[In-State Governor](./In-State-Governor.md)** — audit |

In-State Governor sits **above** Navigator: it can audit Navigator's own compliance too.

## Read next
- **[Why These Tools](./Why-These-Tools.md)** — the failure modes that forced these into existence.
- **[The Trust Model](./Trust-Model.md)** — the one idea both tools are built on: *structure enforces, the
  model only narrates.*
- **[The Fully-Local Mission](./Fully-Local-Mission.md)** — why local + open-source is the point, not a
  constraint.
- **[Navigator](./Navigator.md)** · **[In-State Governor](./In-State-Governor.md)** — per-tool guides.
- **[Roadmap](./Roadmap.md)** — how the blueprint grows.

## Design principles (shared by every piece)
1. **Mechanical core is the trust anchor.** Deterministic checks decide pass/fail. An LLM may *advise*, never
   *adjudicate*.
2. **Verify the artifact, not the narration.** A model's report of what it did is not evidence; the file on
   disk is.
3. **Observe, then recommend — don't silently act.** Findings go to a durable, human-decided ledger.
4. **Local-first.** Runs on your hardware; no cloud dependency for core function.
5. **Legible & ownable.** File-based, inspectable, hand-off-able.
