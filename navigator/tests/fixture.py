# SPDX-License-Identifier: Apache-2.0
"""Builds a small known project tree in a temp dir so every proof runs
against ground truth. Layout:

  ToolA/main.py            imports helper, opens data/output.json, runs sub/run_me.py
  ToolA/helper.py          (imported by main -> role 'root')
  ToolA/data/output.json
  ToolA/sub/run_me.py
  ToolA/MAINTENANCE_LOG.md (mtime forced 60 days older than main.py -> doc_drift)
  ToolB/standalone.py      (no edges -> 'self-contained')
  ToolB/notes.md           references data2/gone.csv (dir exists, file doesn't -> broken_refs)
  ToolB/data2/real.txt
  binary.bin               (metadata-only indexing)
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from navigator.config import Config  # noqa: E402

DAY = 86400


def build(tmp: Path) -> Config:
    root = tmp / "fixture"
    (root / "ToolA" / "data").mkdir(parents=True)
    (root / "ToolA" / "sub").mkdir()
    (root / "ToolB" / "data2").mkdir(parents=True)

    (root / "ToolA" / "main.py").write_text(
        'import helper\n'
        'import os\n'
        'def go():\n'
        '    data = open("data/output.json").read()\n'
        '    os.system("python sub/run_me.py")\n'
        '    return helper.help(data)\n')
    (root / "ToolA" / "helper.py").write_text("def help(x):\n    return x\n")
    (root / "ToolA" / "data" / "output.json").write_text('{"ok": true}')
    (root / "ToolA" / "sub" / "run_me.py").write_text("print('ran')\n")
    log = root / "ToolA" / "MAINTENANCE_LOG.md"
    log.write_text("# Maintenance Log\nToolA processes widget data.\n")
    old = log.stat().st_mtime - 60 * DAY
    os.utime(log, (old, old))

    (root / "ToolB" / "standalone.py").write_text("print('alone')\n")
    (root / "ToolB" / "notes.md").write_text(
        'See "data2/gone.csv" for the export and "data2/real.txt" for notes.\n')
    (root / "ToolB" / "data2" / "real.txt").write_text("real\n")
    (root / "binary.bin").write_bytes(b"\x00\x01\x02\x03")

    return Config(roots=[root], data_dir=tmp / "navdata")


def make_tmp() -> Path:
    return Path(tempfile.mkdtemp(prefix="navproof_"))
