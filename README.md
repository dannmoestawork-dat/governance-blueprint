# Governance Blueprint

*Keep your local AI agents honest.*

**Governance Blueprint** is a free, local-first, open-source kit for **governing and overseeing AI agents**:
the method and the scaffolding you need once you stop *chatting* with a model and start letting agents *do
work* across your files. It has three parts: **the blueprint** (how to set up a workstation where the agent's
memory lives in files you own, with the rules that keep it honest), and **two oversight tools** that check
the work, plus the trust model they share. Built by a one-person firm, for its own daily work, and shared as is.

## Download everything

Everything here is meant to be read offline and kept. To take the whole thing with you, click the green
**Code** button at the top of this page and choose **Download ZIP**, or clone it:

```bash
git clone https://github.com/dannmoestawork-dat/governance-blueprint.git
```

No account, no email, no sign-up.

---

## Why we built this

We run real, multi-agent AI workflows on **local hardware** — not toy demos, but agents that index files,
plan work, write artifacts, and merge data into live systems, day after day. Three problems showed up fast,
and none of them are solved by a better prompt or a bigger model:

1. **You lose sight of what the agents are actually doing.** Once work runs on a schedule across several
   agents, "is the system working?" becomes unanswerable without a live forensic dig. Our own records drifted
   from reality for *days* — they said an automated step was disabled when it had been running cleanly the
   whole time. Nobody noticed, because nothing was watching.

2. **Local models are unreliable narrators.** A model will cheerfully report success for work it never did,
   cite files it never read, and write plausible-but-wrong summaries. You cannot let a model police itself.
   The only thing you can trust is a **deterministic check of the actual artifact** — not the model's account
   of it.

3. **Governance drift compounds as you add agents.** Every rule you write to keep the system safe relies on
   someone *remembering* it. Add parallel agents and the rules start contradicting each other, stale facts
   propagate, dead links and orphaned files accumulate, and the gap between "the rules" and "what's really on
   disk" widens silently.

These are the failure modes that make AI-assisted work feel powerful and untrustworthy at the same time. The
fix isn't more instruction — **it's structure that enforces and verifies.**

## What we're trying to accomplish — the fully-local, open-source thesis

- **Sovereignty.** Your code, your data, and your *process* stay on hardware you own. No cloud round-trip for
  routine work, no per-token meter on your own oversight, no vendor who can change the rules under you.
- **Legibility & ownership.** A file-based, gated process is something you can **inspect, audit, and hand to
  someone else.** "Just use a frontier model" is not a process you can own or package — a gated, local one is.
- **Trust through structure, not vibes.** The mechanical core *enforces*; the model only *advises*, and its
  output is labeled `perceived` until a human confirms it. Verify the artifact, never the narration.
- **Share the scaffolding.** Anyone running local agents hits these same walls. The tools that keep our agents
  honest should be free for the community to use, inspect, and improve.

---

## What's inside

| Part | Role | Status |
|------|------|--------|
| **[Blueprint](./blueprint/)** | *Set up.* The method: an auto-loaded directive, governance tiers, a folder and naming pattern, persistent memory, runbooks, and the known limits, as 20 documents plus blank templates and a worked example. Start with [blueprint/README.md](./blueprint/README.md). | v1.2, documents only |
| **[Navigator](./navigator/)** | *Observe.* Indexes a tree, maps dependencies, runs gap analyzers, keeps human-confirmed summaries, and reports on what the agents (and the codebase) are actually doing. | Working app, 73 tests passing |
| **[In-State Governor](./in-state-governor/)** | *Audit.* Repeatedly checks the tree against governance rules, records every deviation (drift), and reports it. The compliance auditor that sits **above** Navigator. | Reference checker (6 deterministic rules), 36 tests passing |

The division mirrors the two questions you actually need answered:
**Navigator** asks *"are the agents doing good work?"* — **In-State Governor** asks *"is everyone following the
rules we set?"*

## Quick start

Each tool installs independently (Python 3.11+):

```bash
# Navigator — observe a tree
cd navigator && pip install -e . && navigator index /path/to/your/project && navigator sense

# In-State Governor — audit a tree against governance rules
cd in-state-governor && pip install -e . && governor scan /path/to/your/project --config governor.example.toml
```

## Documentation

The shared **[WIKI](./WIKI/Home.md)** covers the philosophy and the cross-tool trust model:
- [Home](./WIKI/Home.md) — overview & map
- [Why These Tools](./WIKI/Why-These-Tools.md) — the workflow-need story in depth
- [The Trust Model](./WIKI/Trust-Model.md) — mechanical core enforces, the model only narrates
- [The Fully-Local Mission](./WIKI/Fully-Local-Mission.md) — sovereignty, legibility, ownership
- [Navigator](./WIKI/Navigator.md) · [In-State Governor](./WIKI/In-State-Governor.md) — per-tool guides
- [Roadmap](./WIKI/Roadmap.md) — future pieces of the keep

## Contributing

This project leans toward **freedom of choice and autonomy** — light process, fork-freely, no permission
needed. See **[CONTRIBUTING.md](./CONTRIBUTING.md)** (with the design principles that keep the tools
trustworthy), the **[Roadmap](./ROADMAP.md)**, and **[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)**.

## License

[Apache-2.0](./LICENSE). Use it, fork it, build on it. Contributions welcome.

*Governance Blueprint: local-first tools for keeping AI agents honest. Copyright 2026 Daniel Moesta /
Material Industrial Sales & Consulting.*
