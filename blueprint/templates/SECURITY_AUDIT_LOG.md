# SECURITY_AUDIT_LOG.md — Recurring Security Scan Log + Cadence
## Classification: Tier 4

> Every scan run, what it checked, what was found, what was done.

---

## What gets scanned

Adapt to your stack. Common categories:

| Category | What it checks for |
|---|---|
| Secrets | API keys, passwords, tokens hardcoded in files |
| Credentials in repos | `.env`, `*.pem`, `*.key` accidentally committed |
| Permissions | Files with overly-permissive ACLs |
| Cloud-sync exposure | Tier 4–5 content in OneDrive/iCloud/Dropbox |
| Outdated dependencies | Pinned packages with CVEs |
| Open ports | Local services accepting connections |
| Git history | High-entropy strings in old commits |
| External account audit | Accounts with credentials in your vault |

---

## Cadence

| Scan | Cadence | Notes |
|---|---|---|
| Secrets / credentials | Weekly | Catches accidents fast |
| Full audit | Monthly | First session of the month |
| Pre-deployment review | On demand | Before any tool goes external |
| Quarterly deep audit | Quarterly | Includes vault inventory |

Cadence dates live in `SESSION_ENV.md`. Results live here.

---

## Entry template

```markdown
### YYYY-MM-DD — [Scan type]

**Run by:** [operator or agent]
**Scope:** [what was scanned]
**Tool / method:** [script, command, manual checklist]

**Findings:**

| Severity | Finding | File / Location | Resolution |
|---|---|---|---|
| (Critical / High / Medium / Low) | (description) | (path) | (fix or "won't fix because...") |

**Resolution summary:**
- (1-line summary)
- (open items pushed to TASK_QUEUE)

**Cadence update:**
- Last run: YYYY-MM-DD
- Next due: YYYY-MM-DD
```

---

## Tools (pick based on stack)

- `gitleaks` — git-history secret scanner
- `trufflehog` — high-entropy + regex scanner
- `bandit` — Python static analysis
- Custom scripts — for project-specific checks

Your scan tool should at minimum:
- Find high-entropy strings (regex + entropy threshold).
- Find credential-pattern filenames.
- Check git-tracked paths.
- Classify by location (cloud-synced vs local-only).
- Output structured (markdown / JSON).

---

## Approved security patterns

When operator approves a *pattern* (not just an instance) for resolution:
log the pattern in `Knowledge_Management/approved_security_patterns.md`.

- Audit log records *findings*.
- Pattern file records *decisions* governing future findings.

Cross-reference: "Resolution: per pattern PSP-003 — see approved_security_patterns.md."

---

## What NOT to log here

- Code-vulnerability fixes that aren't security-related → tool's
  `MAINTENANCE_LOG.md`.
- Abstract security discussion without a scan → not the place.
- One-off "I checked X manually" → either run as a repeatable scan or
  put in `TASK_QUEUE.md`.

---

## Maintenance

- **Every scan:** add an entry. Don't batch.
- **Monthly:** review the previous month. Recurring findings? Cadence
  honored?
- **Quarterly:** re-read approved patterns. Obsolete? Should any tighten?

---

_Signed: [your signature line] — [date]_
