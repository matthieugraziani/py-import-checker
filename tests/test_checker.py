from pathlib import Path

from py_import_checker.checker import check_directory


def write_py(tmp_path: Path, name: str, content: str) -> None:
    (tmp_path / name).write_text(content)


def test_clean_project(tmp_path: Path):
    write_py(tmp_path, "a.py", "x = 1\n")
    write_py(tmp_path, "b.py", "from a import x\n")

    result = check_directory(tmp_path)

    assert result.success
    assert result.checked == 2
    assert result.errors == []


def test_missing_import(tmp_path: Path):
    write_py(tmp_path, "broken.py", "import missing_package\n")

    result = check_directory(tmp_path)

    assert not result.success
    assert len(result.errors) == 1
    assert result.errors[0].error_type == "ModuleNotFoundError"


def test_runtime_error_is_not_import_error(tmp_path: Path):
    write_py(tmp_path, "bad.py", "1 / 0\n")

    result = check_directory(tmp_path)

    assert result.success