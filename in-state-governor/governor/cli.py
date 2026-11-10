# SPDX-License-Identifier: Apache-2.0
"""Command-line interface for In-State Governor.

Usage::

    governor scan <path> [--config governor.toml] [--format md|json] [--out FILE]

Exit codes:
    0  scan ran; no ``error``-severity findings
    1  scan ran; at least one ``error``-severity finding (drift gate failed)
    2  usage / config / IO error
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .config import load_config
from .report import to_json, to_markdown
from .scan import scan


def _write_stdout(text: str) -> None:
    """Write to stdout as UTF-8, tolerating consoles with a narrow codepage.

    The drift ledger uses Unicode checkbox glyphs; a legacy console codepage
    (e.g. cp1252 on Windows) would otherwise raise UnicodeEncodeError. We write
    bytes to the underlying buffer when available, replacing unencodable
    characters only as a last resort.
    """
    data = text + ("\n" if not text.endswith("\n") else "")
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write(data.encode("utf-8"))
        buffer.flush()
    else:
        sys.stdout.write(data.encode("utf-8", "replace").decode("utf-8", "replace"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="governor",
        description="Deterministic governance-compliance checker (mechanical core).",
    )
    parser.add_argument("--version", action="version", version=f"in-state-governor {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_p = sub.add_parser("scan", help="Scan a tree and report governance drift.")
    scan_p.add_argument("path", help="Directory to scan.")
    scan_p.add_argument(
        "--config",
        default="governor.toml",
        help="Path to the TOML rule config (default: governor.toml).",
    )
    scan_p.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format (default: md).",
    )
    scan_p.add_argument(
        "--out",
        default="-",
        help="Output file, or '-' for stdout (default: stdout).",
    )
    return parser


def _cmd_scan(args: argparse.Namespace) -> int:
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"error: config file not found: {args.config}", file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        findings = scan(args.path, config)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    import os

    root = os.path.abspath(args.path)
    if args.format == "json":
        rendered = to_json(findings, root=root)
    else:
        rendered = to_markdown(findings, root=root)

    if args.out == "-":
        _write_stdout(rendered)
    else:
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(rendered)
                if not rendered.endswith("\n"):
                    fh.write("\n")
        except OSError as exc:
            print(f"error: cannot write {args.out}: {exc}", file=sys.stderr)
            return 2
        print(f"wrote {len(findings)} finding(s) to {args.out}", file=sys.stderr)

    has_error = any(f.severity == "error" for f in findings)
    return 1 if has_error else 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "scan":
        return _cmd_scan(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
