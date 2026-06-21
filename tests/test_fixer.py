"""Tests for the auto-fix module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from py_import_checker.checker import FailedImport, ScanReport, check_directory
from py_import_checker.fixer import FixReport, fix_imports, print_fix_report

# ---------------------------------------------------------------------------
# FailedImport.missing_module
# ---------------------------------------------------------------------------


def test_missing_module_extracts_top_level():
    fi = FailedImport(
        file=Path("x.py"),
        error_type="ModuleNotFoundError",
        message="No module named 'requests'",
    )
    assert fi.missing_module == "requests"


def test_missing_module_extracts_top_level_from_submodule():
    fi = FailedImport(
        file=Path("x.py"),
        error_type="ModuleNotFoundError",
        message="No module named 'numpy.core'",
    )
    assert fi.missing_module == "numpy"


def test_missing_module_returns_none_for_runtime_error():
    fi = FailedImport(
        file=Path("x.py"),
        error_type="ImportSpecError",
        message="Unable to create import specification",
    )
    assert fi.missing_module is None


def test_missing_module_returns_none_for_unrecognised_message():
    fi = FailedImport(
        file=Path("x.py"),
        error_type="ModuleNotFoundError",
        message="something unexpected",
    )
    assert fi.missing_module is None


# ---------------------------------------------------------------------------
# fix_imports — dry_run mode (no subprocess, no network)
# ---------------------------------------------------------------------------


def _report_with_missing(*packages: str) -> ScanReport:
    report = ScanReport(checked=len(packages))
    for pkg in packages:
        report.failures.append(
            FailedImport(
                file=Path(f"{pkg}_user.py"),
                error_type="ModuleNotFoundError",
                message=f"No module named '{pkg}'",
            )
        )
    return report


def test_dry_run_returns_skipped_packages():
    report = _report_with_missing("requests", "httpx")
    fix_report = fix_imports(report, dry_run=True)

    assert fix_report.skipped == ["requests", "httpx"]
    assert fix_report.installed == []
    assert fix_report.failed == []


def test_dry_run_deduplicates_packages():
    report = _report_with_missing("requests", "requests")
    fix_report = fix_imports(report, dry_run=True)

    assert fix_report.skipped == ["requests"]


def test_fix_report_ok_when_no_failures():
    report = ScanReport(checked=1)
    fix_report = fix_imports(report, dry_run=True)

    assert fix_report.ok
    assert fix_report.skipped == []


# ---------------------------------------------------------------------------
# fix_imports — real mode (subprocess mocked)
# ---------------------------------------------------------------------------


def _successful_proc() -> MagicMock:
    m = MagicMock()
    m.returncode = 0
    return m


def _failing_proc() -> MagicMock:
    m = MagicMock()
    m.returncode = 1
    return m


def test_fix_calls_pip_for_each_missing_package():
    report = _report_with_missing("requests", "httpx")

    with patch("py_import_checker.fixer.subprocess.run", return_value=_successful_proc()) as mock_run:
        fix_report = fix_imports(report, dry_run=False)

    assert mock_run.call_count == 2
    assert fix_report.installed == ["requests", "httpx"]
    assert fix_report.failed == []
    assert fix_report.ok


def test_fix_records_failed_installs():
    report = _report_with_missing("nonexistent_pkg_xyz")

    with patch("py_import_checker.fixer.subprocess.run", return_value=_failing_proc()):
        fix_report = fix_imports(report, dry_run=False)

    assert fix_report.failed == ["nonexistent_pkg_xyz"]
    assert fix_report.installed == []
    assert not fix_report.ok


def test_fix_skips_non_import_errors():
    report = ScanReport(checked=1)
    report.failures.append(
        FailedImport(
            file=Path("x.py"),
            error_type="ImportSpecError",
            message="Unable to create import specification",
        )
    )

    with patch("py_import_checker.fixer.subprocess.run") as mock_run:
        fix_report = fix_imports(report, dry_run=False)

    mock_run.assert_not_called()
    assert fix_report.installed == []
    assert fix_report.ok


# ---------------------------------------------------------------------------
# print_fix_report (smoke tests — just ensure no crash)
# ---------------------------------------------------------------------------


def test_print_fix_report_dry_run(capsys):
    fr = FixReport(skipped=["requests", "httpx"])
    print_fix_report(fr, dry_run=True)
    out = capsys.readouterr().out
    assert "requests" in out
    assert "httpx" in out


def test_print_fix_report_installed(capsys):
    fr = FixReport(installed=["requests"])
    print_fix_report(fr, dry_run=False)
    out = capsys.readouterr().out
    assert "Installed: requests" in out


def test_print_fix_report_failed(capsys):
    fr = FixReport(failed=["bogus_pkg"])
    print_fix_report(fr, dry_run=False)
    out = capsys.readouterr().out
    assert "Failed to install: bogus_pkg" in out


def test_print_fix_report_nothing(capsys):
    fr = FixReport()
    print_fix_report(fr, dry_run=False)
    out = capsys.readouterr().out
    assert "Nothing to install" in out


# ---------------------------------------------------------------------------
# Integration — check_directory → fix_imports end-to-end (dry_run)
# ---------------------------------------------------------------------------


def write_py(tmp_path: Path, name: str, content: str) -> None:
    (tmp_path / name).write_text(content)


def test_integration_dry_run_end_to_end(tmp_path: Path):
    write_py(tmp_path, "needs_fake.py", "import _py_import_checker_test_pkg_xyz\n")

    report = check_directory(tmp_path)
    assert not report.ok

    fix_report = fix_imports(report, dry_run=True)
    assert "_py_import_checker_test_pkg_xyz" in fix_report.skipped
