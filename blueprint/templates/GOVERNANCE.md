# GOVERNANCE.md — Tier 0–Tier 5 Classification + HITL Gates
## Classification: Tier 4

> Defines what the agent can see, generate, emit; when it must pause for
> operator approval. Customize the tier audiences and HITL gates to your
> domain; the mechanism stays.

---

## 1. OBJECTIVE & INTENT
For each task: **The Win** + **The Anti-Win**.
Standing: substance over speed; primary sources over derived claims;
proactive value with evidence.

## 2. DATA CONTEXT (Inputs)
Source files / Reference data (read-only) / Operator-provided data /
What's missing (flag gaps).

## 3. PROCEDURAL LOGIC (Steps)
1. Read existing state.
2. Question matrix to minimize revisions.
3. Decision point.
4. Build / transform / generate.
5. Verify.

Standing process: plain-language proposal first → incremental build → flag
on second failure → log decisions in `MAINTENANCE_LOG.md`.

## 4. GOVERNANCE & ACCESS CONTROL
- **Write scope:** Vault root and its subdirectories only.
- **Read-only:** Reference-data directories.
- **Forbidden:** Parent directories, unrelated personal files, external
  data transmission without approval.

**Standing authorization:** [Customize. Example: "For approved
in-progress work, the agent may continue without per-task re-approval."]
- Does NOT cover new projects, external-facing output, destructive
  operations, or spending money.

## 5. QUALITY CONTROL & REPORTING
- All scripts run without errors before delivery.
- Calculations / formulas verified manually.
- Provenance tags on every artifact.
- `MAINTENANCE_LOG.md` per directory with scripts.
- `MEMORY.md` updated at session milestones.

## 6. HUMAN-IN-THE-LOOP (HITL) GATES

| Action | Gate Required? |
|---|---|
| Approved in-progress work | No |
| New project / new directory | Yes — plan mode |
| External-facing deliverable | Yes — explicit review |
| Sensitive numerical inputs | Yes — operator validates |
| File deletion / destructive ops | Yes — always |
| Sending data externally | Yes — always |

Approval signals: "go ahead", "approved", "ship it", "gtg" (or your
preferred convention).

### 6a. Classification Downgrade Gate
Trigger: any action moving data from a higher tier to a lower one.
The agent pauses and explains: What / Why this triggers a gate / Risk /
Mitigation. Operator approves instance OR pattern (logged in
`Knowledge_Management/approved_security_patterns.md`).
Pre-deployment: full Tier 0–5 review before any tool goes live.

## 7. SECURITY & PRIVACY — Tier 0–Tier 5

| Tier | Tag | Audience | Description |
|---|---|---|---|
| 0 | `Tier 0` | Public | Marketing, education, anything public |
| 1 | `Tier 1` | Qualified Lead | Gated content; trade for contact info |
| 2 | `Tier 2` | Customer / Client | Active service delivery |
| 3 | `Tier 3` | Partner | Strategic alliance |
| 4 | `Tier 4` | Internal | Your organization only |
| 5 | `Tier 5` | Operator Only | Strategy, margins, IP, financials |

**Customize the audiences** to your domain (researcher, lawyer, consultant
— see parent product file for adaptation examples).

**Classification rules:**
- Every new file gets `## Classification: Tier [N]`.
- Default to the *highest* applicable level.
- Downgrading requires explicit approval.
- When in doubt, mark Tier 4.

**Secrets management:** `.env` files, never in version control,
`.env.example` template safe to share.

## 8. COST & MODEL MANAGEMENT
Right model for the job. Parallelize independent operations. Don't
over-engineer. No additional API costs without operator approval.

## 9. DATA SANITIZATION
Identify sensitive data → sanitize with placeholders → verify before
external use. Names → `[Name]`. Addresses → `[Address]`.

## 10. DATA CURATION & ARCHIVAL
Durable: vault files (cloud-synced if applicable).
Session-temporary: conversation context, recovered via `MEMORY.md`.
Cleanup triggers: project completion → archive or delete.

## 11. TOOL INTEGRATION
Current toolchain: [your harness, language, runtime, sync provider].
Standing rule: tools run locally; no external dependencies without
approval; packages from default upstream.

---

## Quick-Reference Task Template

```markdown
**Task:** [What needs to happen]
**Win:** [What success looks like]
**Inputs:** [Files, data, context]
**Gate:** [Where to review]
**Sensitivity:** [Tier 0–Tier 5]
**Notes:** [Constraints, prior decisions]
```

---

_Signed: [your signature line] — [date]_
