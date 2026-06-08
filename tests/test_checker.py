"""Tests for py-import-checker."""

from __future__ import annotations

from pathlib import Path
import textwrap

from py_import_checker.checker import check_directory
from py_import_checker.cli import main


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def write_py(tmp_path: Path, name: str, content: str) -> Path:
    """Write a Python file inside *tmp_path* and return its path."""
    p = tmp_path / name
    p.write_text(textwrap.dedent(content))
    return p


# ---------------------------------------------------------------------------
# checker.check_directory
# ---------------------------------------------------------------------------


def test_clean_project(tmp_path: Path) -> None:
    write_py(tmp_path, "mod_a.py", "x = 1\n")
    write_py(tmp_path, "mod_b.py", "from mod_a import x\n")

    result = check_directory(tmp_path)

    assert result.success
    assert result.checked == 2
    assert result.errors == []


def test_broken_import_detected(tmp_path: Path) -> None:
    write_py(tmp_path, "broken.py", "import _nonexistent_pkg_xyz\n")

    result = check_directory(tmp_path)

    assert not result.success
    assert len(result.errors) == 1
    assert result.errors[0].error_type == "ModuleNotFoundError"
    assert "_nonexistent_pkg_xyz" in result.errors[0].message


def test_runtime_error_ignored(tmp_path: Path) -> None:
    """Pure runtime errors (NameError, ZeroDivisionError…) must NOT be reported."""
    write_py(tmp_path, "runtime_err.py", "x = 1 / 0\n")

    result = check_directory(tmp_path)

    assert result.success
    assert result.checked == 1


def test_venv_skipped(tmp_path: Path) -> None:
    venv_dir = tmp_path / ".venv" / "lib"
    venv_dir.mkdir(parents=True)
    (venv_dir / "something.py").write_text("import _nope\n")
    write_py(tmp_path, "good.py", "pass\n")

    result = check_directory(tmp_path)

    assert result.success
    assert result.checked == 1


def test_multiple_errors(tmp_path: Path) -> None:
    write_py(tmp_path, "a.py", "import _nope_a\n")
    write_py(tmp_path, "b.py", "import _nope_b\n")
    write_py(tmp_path, "c.py", "pass\n")

    result = check_directory(tmp_path)

    assert not result.success
    assert len(result.errors) == 2
    assert result.checked == 3


# ---------------------------------------------------------------------------
# cli.main
# ---------------------------------------------------------------------------


def test_cli_success(tmp_path: Path) -> None:
    write_py(tmp_path, "ok.py", "x = 42\n")
    code = main([str(tmp_path)])
    assert code == 0


def test_cli_failure(tmp_path: Path) -> None:
    write_py(tmp_path, "bad.py", "import _nope_cli\n")
    code = main([str(tmp_path)])
    assert code == 1


def test_cli_missing_path(tmp_path: Path) -> None:
    code = main([str(tmp_path / "does_not_exist")])
    assert code == 2


def test_cli_src_flag(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "mylib.py").write_text("VALUE = 99\n")
    write_py(tmp_path, "consumer.py", "from mylib import VALUE\n")

    code = main([str(tmp_path), "--src", str(src)])
    assert code == 0