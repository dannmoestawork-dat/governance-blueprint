# RoofTakeoff — Case Study Overview

> **The short version.** A spatial-measurement tool the operator built
> with their agent. v1.0 shipped in ~4 hours. v1.6 stable two weeks
> later. The story is not the tool — it's how the methodology
> (directive, memory, governance, naming, protocols) compounded across
> sessions to produce a reliable artifact.

---

## The setup

The operator's domain involves measuring physical structures from
construction drawings — typically a long, error-prone manual process.
A measurement off by 5% on a 10,000-unit job produces a meaningfully
wrong cost estimate. The operator wanted to compress a day's manual
work into ~30 minutes of structured human-plus-agent work, *without*
sacrificing accuracy.

---

## Why this case is instructive

Five reasons the methodology was visible and load-bearing:

1. **Adversarial inputs.** Every drawing is different. A method that
   worked on Project A might fail on Project B. The methodology had to
   handle that, not just the happy path.
2. **External ground truth.** Some projects had a reference measurement
   from a vendor; some didn't. The methodology had to express the
   difference between *calibration* (repeatability) and *accuracy*
   (vs ground truth).
3. **Fast iteration.** Six minor versions in two weeks. Without the
   methodology, version drift would have left no record of *why* each
   change was made.
4. **A "ship-quality" claim.** At one point the operator wanted to
   publish the tool as something they'd quote externally with. That
   moment forced the methodology to produce a *variance protocol* —
   a standing rule for proving repeatability.
5. **Doc disagreement.** Late in the arc, three different docs gave
   three different measurements for the same project. The methodology
   produced a *validate-then-update standing rule* and a
   *single-source-of-truth declaration*. Both have since been promoted
   to system-wide patterns.

---

## What's in the full case study

The full case study (`RTKWE001_..._Case-Study.md` in this directory)
walks the arc in 9 sections:

1. **Session 1 — From idea to v1.0** (~4 hours).
2. **The first memory entries.**
3. **v1.1–v1.5 — color palette and protocol expansion.**
4. **The variance protocol session.**
5. **Failure modes the methodology caught.**
6. **The single-source-of-truth declaration.**
7. **The validate-then-update standing rule.**
8. **What's still broken** (per `KNOWN_LIMITATIONS.md`).
9. **What an operator copying this case would change for their domain.**

---

## Reading order

Read this README. Read the foundation docs (DIRECTIVE through
KNOWN_LIMITATIONS) if you haven't. Then the full case study.

---

_Apache 2.0. De-identified from real-world artifacts._
