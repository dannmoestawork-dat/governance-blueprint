# RECURSIVE_IMPROVEMENT.md — self-improvement ledger scaffold
<!-- Copy this file's tree into your vault as improvement/ and fill the placeholders.
     Method: the RECURSIVE_IMPROVEMENT product doc. Loop: MEASURE → CAPTURE → DISTILL →
     GATE(human) → APPLY → RE-EVAL. One lever per change. Deterministic grader is the only judge. -->

## Directory to create
```
improvement/
├── CONFIG_MANIFEST.md
├── RUNS.md
├── evals/
├── findings/
├── proposals/
└── evidence/
```

## CONFIG_MANIFEST.md (append-only)
```yaml
config_id: C-001
date: YYYY-MM-DD
model: <ollama tag / model id>
num_ctx: <context length>
soul_version: <prompt/principles version or hash>
gate_versions: <grader/validator versions>
scaffold: <how context is assembled>
notes: BASELINE
```

## RUNS.md header
```
| date | eval_id | config_id | variant | run# | verdict | evidence | finding |
|---|---|---|---|---|---|---|---|
```

## evals/EVAL-###.md
```yaml
eval_id: EVAL-001
title: <one line>
variants: [A, B, C]        # blind framings, functionally identical
grader: <path + invocation of the deterministic grader>
ground_truth: <source + date last verified>
type: capability | regression
locks: <P-### for regression evals>
```
Body: Task · Done checklist · Guardrails · Grade rubric (PASS/PARTIAL/FAIL).

## findings/F-###.md
```yaml
finding_id: F-###
date: YYYY-MM-DD
source: eval-run | gate-bounce | operator-observation
eval_runs: <RUNS.md refs>
config_id: C-###
taxonomy: spec-ambiguity | grader-defect | scaffold-gap | model-error | gate-blind-spot | config-limit
lever_hypothesis: L1-L6 | none — accepted boundary
status: open | distilled(P-###) | accepted-boundary | withdrawn
```
Body: What was observed · What caught it · What it teaches.
<!-- Classify spec-ambiguity and grader-defect BEFORE model-error. -->

## proposals/P-###.md
```yaml
proposal_id: P-###
date: YYYY-MM-DD
findings: [F-###]
lever: L1|L2|L3|L4|L5|L6    # exactly one
change: <precise edit>
proof_eval: EVAL-###         # named before apply
expected_delta: <what moves>
status: proposed | approved | applied(C-###) | proven | regressed | reverted | retired
approved_by: ____            # the human gate — never automated
```
Body: Rationale · Risk · Rollback.

## Standing rules
- [ ] Append-only ledgers; evidence kept verbatim
- [ ] Model never grades itself; model may read, never write, this tree
- [ ] Blind re-eval (rotate variants; never announce a test)
- [ ] Re-verify ground truth before any run that justifies a change
- [ ] Every proven proposal adds a regression eval (the ratchet)
