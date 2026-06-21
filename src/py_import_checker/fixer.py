"""Auto-fix broken imports by installing missing packages with pip."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field

from .checker import ScanReport


@dataclass
class FixReport:
    installed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failed


def fix_imports(report: ScanReport, dry_run: bool = False) -> FixReport:
    """Attempt to install every missing top-level package found in *report*.

    Parameters
    ----------
    report:
        The :class:`~py_import_checker.checker.ScanReport` produced by
        :func:`~py_import_checker.checker.check_directory`.
    dry_run:
        When *True*, log what *would* be installed but do not actually call
        pip.  Useful for previewing the fix without side-effects.

    Returns
    -------
    FixReport
        Summary of which packages were installed, which failed, and which were
        skipped (already present or non-installable error types).
    """
    fix_report = FixReport()

    # Collect unique package names, preserving insertion order.
    seen: dict[str, None] = {}
    for failure in report.failures:
        pkg = failure.missing_module
        if pkg is not None:
            seen[pkg] = None

    if not seen:
        return fix_report

    for pkg in seen:
        if dry_run:
            fix_report.skipped.append(pkg)
            continue

        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            fix_report.installed.append(pkg)
        else:
            fix_report.failed.append(pkg)

    return fix_report


def print_fix_report(fix_report: FixReport, dry_run: bool = False) -> None:
    if dry_run:
        if fix_report.skipped:
            print("Dry-run — would install:")
            for pkg in fix_report.skipped:
                print(f"  • {pkg}")
        else:
            print("Dry-run — nothing to install.")
        return

    for pkg in fix_report.installed:
        print(f"Installed: {pkg}")
    for pkg in fix_report.failed:
        print(f"Failed to install: {pkg}")

    if not fix_report.installed and not fix_report.failed:
        print("Nothing to install.")
