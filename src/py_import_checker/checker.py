"""Core import verification engine."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ImportFailure:
    """Represents a single import failure."""

    file: Path
    error_type: str
    message: str


@dataclass
class CheckResult:
    """Aggregated result from a full scan."""

    checked: int = 0
    errors: list[ImportFailure] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


_SKIP_PARTS = {".venv", "venv", "__pycache__", ".git", "node_modules", "dist", "build"}


def _should_skip(path: Path, script_path: Path) -> bool:
    if path.resolve() == script_path.resolve():
        return True
    return any(part in _SKIP_PARTS for part in path.parts)


def check_directory(
    root: Path,
    extra_paths: list[Path] | None = None,
    glob: str = "**/*.py",
) -> CheckResult:
    """
    Scan all Python files under *root* and attempt to import each one.

    Parameters
    ----------
    root:
        Directory to scan recursively.
    extra_paths:
        Additional paths inserted at the front of sys.path before scanning
        (e.g. the project ``src/`` directory).
    glob:
        Glob pattern used to find Python files (default: ``**/*.py``).
    """
    root = root.resolve()
    script_path = Path(__file__).resolve()

    paths_to_add = [root] + (extra_paths or [])
    for p in reversed(paths_to_add):
        p_str = str(p)
        if p_str not in sys.path:
            sys.path.insert(0, p_str)

    result = CheckResult()

    for file_path in sorted(root.glob(glob)):
        if _should_skip(file_path, script_path):
            continue

        result.checked += 1
        relative = file_path.relative_to(root)
        module_name = ".".join(relative.with_suffix("").parts)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
        except (ModuleNotFoundError, ImportError) as exc:
            result.errors.append(
                ImportFailure(
                    file=relative,
                    error_type=type(exc).__name__,
                    message=str(exc),
                )
            )
        except Exception:  # pylint: disable=broad-exception-caught
            # Ignore pure runtime errors — only structural import issues matter.
            pass

    return result