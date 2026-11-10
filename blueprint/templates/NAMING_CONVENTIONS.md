# NAMING_CONVENTIONS.md — Bracket-Token Filename Pattern
## Classification: Tier 4

> Filename pattern that makes the filesystem itself navigable.

---

## The format

**Notation:** `[Project][DATE][VERSION][Folder-SyncTag][Etc].ext`

**Filename:** Five fields, **underscore between fields**, **hyphen within
fields**. No literal brackets.

**Example:**
```
RTK014_2026-04-28_v1.6_RoofTakeoff-SYNC_Variance-Tracker.md
```

---

## Field-by-field

### 1. Project — alphanumeric mnemonic
- 3–6 letters + 3-digit ID. Letters allude to the project.
- Examples: `RTK014`, `LLMP001`, `OBT003`.
- Stable across the project's life.

### 2. Date — ISO-8601
- `YYYY-MM-DD`. Sorts chronologically.
- Use last semantic update date for revised files.

### 3. Version — semver-lite
- `vN.N` or `vN.N.N`. Major / minor / patch.
- Documents (not code): `vN.N` is enough.

### 4. Folder-SyncTag — privacy/security signal
- Format: `<FolderMnemonic>-<SyncTag>`
- Folder mnemonic: short version of the parent directory name.
- **Sync tag — three states:**

| Tag | Meaning |
|---|---|
| `LOCAL` | Airgapped — never leaves this machine |
| `SYNC` | Cloud-replicated — backed up but not externally distributed |
| `SHARE` | Externally distributed — sent to clients/partners or published |

The sync tag is the grep-able privacy signal. `find . -name "*_LOCAL_*"`
finds everything that must never leave this machine.

**Promotion rule:** Sync tag can only become *more permissive* with explicit
operator approval. Mirrors the Tier classification downgrade gate.

### 5. Etc — free-form discriminator
- Hyphens for multi-word.
- Examples: `Variance-Tracker`, `Roof27A-Takeoff`, `Q3-Pricing-Update`.

---

## Special-case files (canonical names)

| File | Why retained |
|---|---|
| `README.md` | GitHub auto-renders |
| `LICENSE` | Tooling convention |
| `.gitignore`, `.env.example` | Tool convention |
| `requirements.txt`, `package.json`, etc. | Build-tool convention |
| `CHANGELOG.md`, `CONTRIBUTING.md` | Open-source convention |

Everything else follows the bracket-token convention.

---

## Folders

- Underscores OR hyphens (pick one and stick with it).
- Project mnemonic prefix on subfolders: `RTK014_Example_Project/`.
- Sync state inherits from most-restrictive child file.

---

## Worked rename examples

| Old name | New name |
|---|---|
| `notes.md` | `RTK014_2026-04-28_v1.0_RoofTakeoff-SYNC_Notes.md` |
| `meeting_2026-04-28.md` | `OPS001_2026-04-28_v1.0_Operations-SYNC_Meeting-Notes.md` |
| `Q3 budget v2.xlsx` | `BGT003_2026-04-28_v2.0_Finance-LOCAL_Q3-Budget.xlsx` |
| `final_proposal.docx` | `RTK014_2026-04-28_v3.0_RoofTakeoff-SHARE_Proposal.docx` |

---

## Programmatic parsing

```python
from pathlib import Path

def parse_filename(filename: str) -> dict | None:
    stem = Path(filename).stem
    parts = stem.split("_")
    if len(parts) != 5:
        return None  # not in convention (e.g., README, LICENSE)
    project, date, version, folder_sync, etc = parts
    if "-" not in folder_sync:
        return None
    folder, sync_tag = folder_sync.rsplit("-", 1)
    if sync_tag not in ("LOCAL", "SYNC", "SHARE"):
        return None
    return {
        "project": project, "date": date, "version": version,
        "folder": folder, "sync_tag": sync_tag, "etc": etc,
    }
```

---

## Adoption tips

1. Apply to new files. Migrate existing on touch.
2. Use shell aliases / snippets to generate the prefix.
3. Tab completion handles the verbose part.
4. The agent can rename files conformantly when asked (with `DIRECTIVE.md`
   §11 in place).
5. The convention is yours to bend. Document deviations in this file.

---

_Signed: [your signature line] — [date]_
