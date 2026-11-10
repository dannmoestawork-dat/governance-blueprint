# Contributing to Governance Blueprint

Thanks for being here. This project leans, on purpose, toward **freedom of choice and autonomy**. That stance
has its own problems — so does every stance — and we've chosen to work from it anyway. In practice that means:

- **You don't need our permission.** It's Apache-2.0. Use it, fork it, rip out half of it, ship your own
  version. Forking is a first-class, healthy outcome — not a failure of the project.
- **We favor the lightest process that still works.** No CLA, no mandatory templates, no gatekeeping rituals.
- **We'd rather say "here's why we built it this way" than "you must."** What follows are the load-bearing
  choices that make these tools trustworthy. If your change keeps them, we'd love it on the mainline. If your
  change *removes* them, that's not a rejection of you — it's a different tool, and a fork is the right home
  for it.

## Ways to contribute (all welcome, none required)
- **Use it and tell us what broke.** Bug reports are contributions.
- **Open an issue to think out loud.** Especially before a big change — see the [Roadmap](./ROADMAP.md). This
  is a suggestion, not a toll gate.
- **Send a PR.** Small and focused is easiest to review, but we won't turn away ambition.
- **Fork and diverge.** If your vision pulls a different direction, follow it. Tell us — we'll happily link to
  interesting forks.

## Getting set up
Each tool installs independently (Python 3.11+):
```bash
cd navigator          && pip install -e . && python tests/prove_core.py
cd ../in-state-governor && pip install -e . && python tests/prove_governor.py
```

## The spine — why these tools are trustworthy
These aren't bureaucratic rules; they're the reason the tools are worth trusting at all. For changes you'd like
merged into the mainline, please keep them. (Disagree? Fork freely — genuinely.)

1. **The mechanical core is the trust anchor.** Deterministic checks decide pass/fail. An LLM may *advise*
   (interpretation, summary, root-cause) but never *adjudicate*. Model output is labeled `perceived` until a
   human confirms it.
2. **Verify the artifact, not the narration.** Trust the file on disk / the exit code — never a model's account
   of what it did.
3. **Observe and recommend; don't silently mutate the source of truth.** Findings go to a human-decided ledger
   (Accept / Reject / Defer). Auto-fix, if ever added, is opt-in and never the default.
4. **Local-first.** The core function runs offline. A model backend is optional and the user's choice (local
   like Ollama, or any OpenAI-compatible endpoint) — never a hard cloud dependency in the core.
5. **A check that can only pass proves nothing.** Every deterministic check ships **adversarial tests**: assert
   it *catches* a seeded violation *and* *passes* a clean case.

If a PR keeps the five above, the rest is style and we're flexible.

## Practical asks for a PR (light touch)
- Run the relevant `tests/prove_*.py` and mention the result.
- Add tests for new behavior (especially new checks/analyzers — see spine #5).
- Keep new `*.py` files' first line as `# SPDX-License-Identifier: Apache-2.0`.
- Note what you changed and why. A sentence is fine.
- Don't reformat unrelated code in the same PR — keeps reviews honest.

We don't enforce a specific formatter or line length. Match the surrounding code; use your judgment.

## Licensing of contributions
By submitting a contribution you agree it's provided under the project's [Apache-2.0](./LICENSE) license
(inbound = outbound). No separate CLA. If a file is substantially yours, you're welcome to add your copyright
line alongside the existing notice.

## Conduct
Be straight with people and assume good faith. The full version is in
[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) — also written from the freedom-and-autonomy frame.

---
*The frame, restated: we optimize for your autonomy. Where that creates friction, we'll usually resolve it in
favor of your freedom to choose — including the freedom to walk off with the code and build something better.*
