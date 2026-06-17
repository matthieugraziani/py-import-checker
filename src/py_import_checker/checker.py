"""Import verification helpers."""

from __future__ import annotations

import importlib.util
import sys
from contextlib import contextmanager
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path



@dataclass
class FailedImport:
    file: Path
    error_type: str
    message: str


@dataclass
class ScanReport:
    checked: int = 0
    failures: list[FailedImport] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


_SKIP_PARTS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "dist",
    "build",
}


@contextmanager
def _temporary_sys_path(paths: list[Path]) -> Iterator[None]:
    previous = sys.path[:]

    for path in reversed(paths):
        value = str(path)
        if value not in sys.path:
            sys.path.insert(0, value)

    try:
        yield
    finally:
        sys.path[:] = previous


def _should_skip(path: Path, current_file: Path) -> bool:
    if path.resolve() == current_file:
        return True

    return any(part in _SKIP_PARTS for part in path.parts)


def _module_name(root: Path, file: Path) -> str:
    relative = file.relative_to(root).with_suffix("")
    return ".".join(relative.parts)


def _check_file(root: Path, file: Path) -> FailedImport | None:
    name = _module_name(root, file)

    spec = importlib.util.spec_from_file_location(name, file)

    if spec is None or spec.loader is None:
        return FailedImport(
            file=file.relative_to(root),
            error_type="ImportSpecError",
            message="Unable to create import specification",
        )

    try:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)

    except (ModuleNotFoundError, ImportError) as exc:
        return FailedImport(
            file=file.relative_to(root),
            error_type=type(exc).__name__,
            message=str(exc),
        )

    except Exception:
        # Import reached module code. Runtime failures are not import failures.
        return None

    return None


def check_directory(
    root: Path,
    extra_paths: list[Path] | None = None,
    pattern: str = "**/*.py",
) -> ScanReport:
    """Try importing Python files below root and report missing imports."""

    root = root.resolve()
    current_file = Path(__file__).resolve()

    paths = [root, *(extra_paths or [])]
    report = ScanReport()

    with _temporary_sys_path(paths):
        for file in sorted(root.glob(pattern)):
            if _should_skip(file, current_file):
                continue

            report.checked += 1

            failure = _check_file(root, file)

            if failure:
                report.failures.append(failure)

    return report