# Worked Example — The Methodology In Action

> **Purpose.** Reading the foundation docs tells you *what* the methodology
> is. This directory shows you *how it played out* on a real tool — what
> the directive shaped, where memory grew, how governance gated each
> release, what the naming convention looked like under load. De-identified
> from a real-world case but structurally faithful.

---

## What's here

```
worked_example/
└── RoofTakeoff/
    ├── README.md                                   ← case study overview
    └── RTKWE001_..._Case-Study.md                  ← the full narrative
```

**One case study.** A spatial-measurement tool that evolved from v1.0 to
v1.6 over ~2 weeks. The case spans:

- The first session — directive, plain-language proposal, first deliverable.
- Memory growth — domain corrections and feedback memories that
  shaped subsequent sessions.
- Tool versioning — color palette expanded; new conventions emerged;
  failures surfaced limits.
- Variance protocol — when the operator needed to make a "ship-quality"
  claim, the methodology produced the standardized re-run protocol.
- Single-source-of-truth declaration — when measurements scattered
  across multiple docs, one doc was declared canonical and the others
  shrunk to pointers.
- Validate-then-update standing rule — the day older docs disagreed
  with newer better-validated data.

---

## Why this case in particular

It's the most recently completed full arc in the source vault — clean
v1.0 → v1.6 progression, real failures and real fixes, a published
variance protocol, and a moment where the methodology *itself* visibly
reshaped under load (Section 6 of the case study).

If you want a shorter introduction, read `RoofTakeoff/README.md`. If
you want the full arc, read the case study.

---

## What this is NOT

- A tutorial on the spatial-measurement domain. The domain is shown only
  as context; the lessons are about the methodology.
- A claim that this tool is the right solution for any specific problem.
  It's the right *example* for showing the patterns.
- An operations manual for the actual tool. The patterns generalize; the
  tool itself is domain-specific.

---

_Apache 2.0. See parent directory `LICENSE`._
