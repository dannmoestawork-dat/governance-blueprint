# KNOWN_LIMITATIONS.md — What Doesn't Work Yet, And Why
## Classification: Tier 0

> Be honest about what's still broken. Re-read quarterly.

---

## Why publish this

1. You will hit these failure modes. Naming them lets you work around
   them, not blame yourself.
2. The mitigations are part of the methodology.
3. AI tooling iterates fast. Date each limit; note what's being watched
   as a fix.

---

## The three big ones

### 1. Memory misses

**Looks like:** Agent forgets what it should recall. You correct the
same thing twice.

**Why:** Memory loads via keyword match against index descriptions. If
the description doesn't match the current task's vocabulary, the file
stays unloaded — even when relevant. Worse with bigger memory stores.

**Cost:** Same correction repeats. Trust degrades. You stop saving.

**Mitigations:**
- Specific descriptions. Vague descriptions rarely match.
- Critical feedback memories cross-referenced in `DIRECTIVE.md` so they
  auto-load.
- Watching: semantic-search retrieval (RAG). Adds vector store
  complexity; tradeoff not yet worth it for single-operator vaults.

### 2. Curation effort

**Looks like:** Memory is write-cheap, curate-expensive. After a month,
30 topic files. Some stale, some duplicate. Index at 180+ lines and
growing. You skip curation. Index hits 240, auto-load truncates. Bottom
40 entries silently stop loading.

**Why:** No automatic enforcement. Curation produces no visible output.
Discipline slips.

**Cost:** Index bloat → silent memory loss. Stale memories →
wrong recommendations. Duplicates → conflicting answers. System decays.

**Mitigations:**
- Recurring maintenance cadence in `SESSION_ENV.md`. Drift becomes visible.
- Two-part discipline (`MEMORY_SCHEMA.md`): create as needed; improve
  process when context is lost.
- Honest acknowledgment: if you can't sustain curation, the methodology
  is fragile. Plan accordingly.
- Watching: duplicate-detection scripts, age-based staleness flags.

### 3. Context drops

**Looks like:** 90 minutes into a session, agent applies an old version
of a pattern it should have updated. Or vocabulary drifts after a topic
switch. Or compaction loses detail.

**Why:** Context windows (measured in **tokens** — ~0.75 words per
token; modern windows are 200,000 tokens) are large but not infinitely
coherent. Information at position 50,000 tokens of a 200,000-token window
is loaded but attention varies. Long sessions may trigger lossy compaction.

**Cost:** Late-session work drifts from early-session decisions.
Inconsistency surfaces in review.

**Mitigations:**
- Three gates: ask gate (verify before answering recall questions); save
  gate (confirm inference before writing memory); cold-read gate (scan
  topic files against current evidence).
- Plain-language proposals before code (catches drift early).
- Session protocols (start/end loops) prevent between-session drift.
- **Stop-and-curate during the session — primary discipline.** When you
  notice drift, pause, re-read the relevant memory or doc, restate, resume.
  Works for most cases.
- **Shorter sessions only when stop-and-curate isn't enough.** When
  even mid-session resets don't bring the agent back to first
  principles, end the session for high-stakes work. Escalation, not first move.
- Watching: native memory-management features in agent harnesses.

---

## Smaller open problems

- **Source-cite correctness vs. fluency.** Agent can be confidently
  wrong — *including on tasks where it has been reliably right multiple
  times before*. Track record doesn't predict next-turn correctness.
  Workaround: "if you can't cite it, don't say it" — applied to every
  output, not just early ones.
- **Multi-system integration.** Combining open-source + frontier
  models is real work; doesn't generalize across stacks.
- **Can the agent see what the operator sees?** For visual-precision
  work (drawings, takeoffs, diagrams), no current way to confirm the
  agent's interpretation matches the artifact's actual data. Operator
  remains the only ground truth.
- **Cost portability.** Frontier models getting more expensive faster
  than cheaper. Defense: plain text on a filesystem; any model can read
  markdown. Switching providers becomes a decision, not a migration.
- **Verification gap.** Generated artifacts can pass tests and still be
  subtly wrong. Verification tooling lags generation tooling.

---

## In practice

For the operator considering this methodology:

1. **Plan curation time.** Build into your cadence or it doesn't happen.
2. **Verify before relying on recall.** When agent says "we decided X,"
   check current state for high-stakes calls.
3. **Keep critical rules in the directive.** Don't gate them behind
   index lookup.
4. **End long sessions.** Coherence degrades. Reset is cheap.
5. **You will feel the work.** Not magical efficiency. Real discipline.

---

## Not a known limitation

- Sycophancy or shallow output → directive problem, not a limit.
- Hallucinations → source-cite or don't say it.
- Skipping review → operator is ground truth.
- Reasons not to start → methodology delivers value with these limits.

---

## Updating

- Limit resolved → move to "Resolved."
- New limit emerges → add it.
- Mitigation validated → note it.

Living document. Re-read quarterly.

---

_Signed: [your signature line] — [date]_
