"""Command line interface for import checking."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .checker import ScanReport, check_directory
from .fixer import fix_imports, print_fix_report


def print_report(report: ScanReport) -> None:
    for failure in report.failures:
        print(
            f"{failure.file}: "
            f"{failure.error_type}: "
            f"{failure.message}"
        )

    if report.ok:
        print(f"OK: {report.checked} files checked")
    else:
        print(
            f"{len(report.failures)} failures "
            f"in {report.checked} files"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="py-import-checker",
        description="Check Python files for import failures.",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
    )

    parser.add_argument(
        "--src",
        action="append",
        default=[],
        metavar="DIR",
    )

    parser.add_argument(
        "--fix",
        action="store_true",
        default=False,
        help="Attempt to install missing packages with pip.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Show what --fix would install without actually installing.",
    )

    args = parser.parse_args(argv)

    root = Path(args.path).resolve()

    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    report = check_directory(
        root,
        extra_paths=[Path(p) for p in args.src],
    )

    print_report(report)

    if args.fix or args.dry_run:
        if not report.ok:
            print()
            fix_report = fix_imports(report, dry_run=args.dry_run)
            print_fix_report(fix_report, dry_run=args.dry_run)
            if not args.dry_run and fix_report.ok and fix_report.installed:
                # Re-scan after fix to confirm resolution.
                print()
                report = check_directory(
                    root,
                    extra_paths=[Path(p) for p in args.src],
                )
                print_report(report)
                return 0 if report.ok else 1
            return 0 if fix_report.ok else 1

    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())