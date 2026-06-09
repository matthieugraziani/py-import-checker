# <p align=center>py-import-checker<p>

<p align=center>

[![PyPI version](https://img.shields.io/pypi/v/py-import-checker.svg)](https://pypi.org/project/py-import-checker/)
[![Tests](https://github.com/matthieugraziani/py-import-checker/actions/workflows/python-app.yml/badge.svg)](https://github.com/matthieugraziani/py-import-checker/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</p>

**Fast, zero-dependency Python import health scanner.**

Recursively scan any Python project and instantly surface every broken or missing import — before your tests run, before CI fails, before runtime surprises you.

```
py-import-checker src/ --src src/

  py-import-checker  —  Python import health scanner

  Scanning  /home/user/myproject/src

──────────────────────────────────────────────────
  ✗  mypackage/broken_module.py
     ModuleNotFoundError: No module named 'nonexistent_lib'

──────────────────────────────────────────────────
✗ 1 broken import(s) found in 14 file(s) scanned.
```

---

## Architectural Pain Points & Technical Approach
The Problem Analysis
Within complex Python architectures (whether large-scale monoliths or microservices), maintaining the integrity of the internal and external dependency graph presents continuous engineering challenges (such as module refactoring, dependency obsolescence, or configuration drift in project layouts). Traditionally, these anomalies manifest through three critical vectors:

CI/CD Pipeline Infiltration: ModuleNotFoundError or ImportError exceptions are frequently detected only at the very end of the validation pipeline—after time-consuming provisioning and environment setup steps—resulting in wasted computation time (CI runner hours).

Runtime Blindspots: If a broken import path resides within a rarely executed module or one that lacks unit test coverage, the flaw is promoted straight to production, causing critical, unexpected crashes at runtime.

Operational Overhead of Legacy Tooling: Running full-blown linters or executing the entire test suite solely to verify architectural link resolvability introduces unacceptable latency into the developers' local feedback loop.

The Technical Solution
py-import-checker introduces a decoupled, ultra-fast validation layer. By isolating the specification loading of each module without triggering the execution of its underlying business logic, the tool performs a hermetic analysis of the import graph. It actively filters out runtime-state exceptions to surgically and exhaustively isolate structural import health failures alone.

---
## Features

- **Zero dependencies** — uses only the Python standard library (`importlib`, `pathlib`, `sys`)
- **src-layout aware** — pass `--src` to add extra directories to `sys.path`
- **Noise-free** — only reports `ImportError` / `ModuleNotFoundError`; ignores runtime exceptions
- **Auto-skips** virtual environments (`.venv`, `venv`) and build artefacts
- **CI-friendly** — exits with code `1` on any broken import, `0` on success
- **Self-checking** — the CI pipeline scans itself with `py-import-checker`

---

## Installation

```bash
pip install py-import-checker
```

Or install from source (editable):

```bash
git clone https://github.com/matthieugraziani/py-import-checker
cd py-import-checker
pip install -e .
```

---

## Usage

### Command line

```bash
# Scan the current directory
py-import-checker

# Scan a specific directory
py-import-checker path/to/project

# src-layout project (adds src/ to sys.path)
py-import-checker . --src src/

# Multiple extra paths
py-import-checker . --src src/ --src lib/

# Custom file glob
py-import-checker . --glob "app/**/*.py"

# Verbose output (show all files, not just errors)
py-import-checker . -v
```

### Python API

```python
from pathlib import Path
from py_import_checker.checker import check_directory

result = check_directory(
    root=Path("src/"),
    extra_paths=[Path("src/")],
)

if not result.success:
    for err in result.errors:
        print(f"{err.file}: {err.error_type}: {err.message}")
```

### Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/matthieugraziani/py-import-checker
    rev: v0.1.0
    hooks:
      - id: py-import-checker
        args: [--src, src/]
```

### GitHub Actions

```yaml
- name: Check imports
  run: |
    pip install py-import-checker
    py-import-checker . --src src/
```

---

## How it works

For every `.py` file found under the target directory, `py-import-checker` uses
`importlib.util.spec_from_file_location` to load and execute the module in an
isolated namespace. If execution raises `ImportError` or `ModuleNotFoundError`,
the failure is recorded. All other exceptions (runtime errors, missing variables,
etc.) are silently ignored — the tool focuses exclusively on **structural import
health**.

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0`  | All imports resolved successfully |
| `1`  | One or more broken imports found |
| `2`  | Invalid arguments (e.g. path does not exist) |

---

## Development

```bash
# Install with dev extras
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/ tests/

# Type-check
mypy src/
```

---

## License

MIT — see [LICENSE](LICENSE).
