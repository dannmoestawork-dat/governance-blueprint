# DATA_SOURCES.md — External Reference Index
## Classification: Tier 4

> Single canonical index of every data source the operator's tools consume.
> Replace the example sections with your domain's data.

---

## [Section 1 — Internal Reference Data]

| Directory | Source | Contents | Status |
|---|---|---|---|
| `[path]/Reference/[Source_A]/` | [vendor / source name] | [contents] | Active |
| `[path]/Reference/[Source_B]/` | [vendor / source name] | [contents] | Planned |

---

## [Section 2 — Approved External Sources]

Public sources approved for research / cross-referencing. Claims must
be verifiable against at least one of these.

| Source | What it provides | URL / Access |
|---|---|---|
| [Source name] | [type of data] | [URL or "licensed — see note"] |

---

## [Section 3 — Internal Sensitive Data]

| Location | Contents | Classification |
|---|---|---|
| `[path]/[file]` | [type] | Tier 5 |
| `[path]/[file]` | [type] | Tier 4 |

**Sensitive-data rules** (adapt to your domain): the agent never
estimates or recalls sensitive numerical inputs from memory. Always
reads from source files. (See `KNOWN_LIMITATIONS.md` for why.)

---

## [Section 4 — Project Documents]

| Location | Contents | Classification |
|---|---|---|
| `[path]/Production/Active_Projects/` | Active client work | Tier 4 |
| `[path]/Production/Pipeline/Project_Pre_Plan/` | In-progress prep | Tier 4 |

---

## [Section 5 — System / Hardware]

| Source / Location | Contents | Purpose |
|---|---|---|
| `[path]/Architecture/` | System architecture docs | Infra reference |

---

## Handling rules

### For all sources
- Read-only. Never modify originals.
- Extract zips to a temp directory; don't extract in place.
- Cross-reference required. If it can't be cited, don't say it.
- Synthesis is the goal. Raw data is input.

### For vendor / proprietary sources
- May be proprietary but not secret. Reference in deliverables; don't
  republish in a competing product.
- Verify accessibility before depending on it.
- Note credential requirements.

### For sensitive / Tier-5 data
- No external-facing output without explicit approval.
- Live in a designated directory.
- Excluded from cloud-sync if provider doesn't meet your trust threshold.

### For public sources
- Verify accessibility before depending on it.
- Note login requirements.
- URLs change. Log working URLs; expect breakage.

---

## Adding new sources

### New vendor
1. Create directory: `[path]/Reference/[Vendor]_Data/`
2. Add to the appropriate table above.
3. Store raw data — read-only.
4. Update `INVENTORY.md` if a tool processes it.
5. Note licensing/redistribution constraints.

### New external source
1. Add to the appropriate table.
2. Note access method (public, login, licensed).
3. If it feeds a tool, document in that tool's `MAINTENANCE_LOG.md`.

### New project documents
1. Place in the appropriate project directory.
2. Project-specific docs → project's folder.
3. General reference → reference area.

---

## Maintenance

- Update when source onboarded, deprecated, moved, or access changes.
- Don't update for routine content additions within an existing source.

---

_Signed: [your signature line] — [date]_
