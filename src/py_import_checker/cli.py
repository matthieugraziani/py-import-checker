"""Command-line interface for py-import-checker."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .checker import CheckResult, check_directory

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
DIM = "\033[2m"


def _banner() -> None:
    print(f"\n{BOLD}{CYAN}py-import-checker{RESET}  —  Python import health scanner\n")


def _print_result(result: CheckResult, verbose: bool) -> None:
    if verbose:
        print(f"{DIM}Verbose mode enabled.{RESET}\n")

    if result.errors:
        print(f"{YELLOW}{'─' * 50}{RESET}")
        for err in result.errors:
            print(f"  {RED}✗{RESET}  {BOLD}{err.file}{RESET}")
            print(f"     {DIM}{err.error_type}: {err.message}{RESET}\n")

    print(f"{'─' * 50}")
    total = result.checked
    n_err = len(result.errors)

    if result.success:
        print(
            f"{GREEN}{BOLD}✓ All clear!{RESET}"
            f"  {total} file(s) checked — no broken imports.\n"
        )
    else:
        print(
            f"{RED}{BOLD}✗ {n_err} broken import(s){RESET}"
            f" found in {total} file(s) scanned.\n"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="py-import-checker",
        description="Scan a Python project for broken imports.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory).",
    )
    parser.add_argument(
        "--src",
        metavar="DIR",
        action="append",
        default=[],
        help=(
            "Extra directory to prepend to sys.path (repeatable). "
            "Useful for src-layout projects."
        ),
    )
    parser.add_argument(
        "--glob",
        default="**/*.py",
        help="Glob pattern for file discovery (default: **/*.py).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show all scanned files, not just errors.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args(argv)
    root = Path(args.path).resolve()

    if not root.exists():
        print(f"{RED}Error: path '{root}' does not exist.{RESET}", file=sys.stderr)
        return 2

    extra = [Path(p).resolve() for p in args.src]

    _banner()
    print(f"  {DIM}Scanning  {root}{RESET}")
    if extra:
        print(f"  {DIM}sys.path  {', '.join(str(p) for p in extra)}{RESET}")
    print()

    result = check_directory(root, extra_paths=extra, glob=args.glob)
    _print_result(result, args.verbose)

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
