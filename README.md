<p align="center">
  <h1 align="center">py-import-checker</h1>
<p align="center">
  <a href="https://pepy.tech/projects/py-import-checker">
    <img src="https://static.pepy.tech/personalized-badge/py-import-checker?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=GREEN&left_text=downloads" alt="PyPI Downloads">
  </a>
   <a href="https://pypi.org/project/py-import-checker/">
      <img src="https://img.shields.io/pypi/v/py-import-checker.svg" alt="PyPI version">
    </a>
    <a href="https://github.com/matthieugraziani/py-import-checker/actions">
      <img src="https://github.com/matthieugraziani/py-import-checker/actions/workflows/ci.yml/badge.svg" alt="Tests">
    </a>
    <a href="https://opensource.org/licenses/MIT">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
    </a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  </p>
</p>

A zero-dependency Python tool that scans a project and reports broken imports.

It loads Python files using the standard library and reports import failures before they reach runtime.

## Features

- Zero dependencies (Python standard library only)
- Supports `src/` layouts with `--src`
- Reports `ImportError` and `ModuleNotFoundError`
- Ignores runtime errors raised during module execution
- Skips virtual environments and build directories
- Works in CI with meaningful exit codes

## Installation

```bash
pip install py-import-checker
```

## Usage

```bash
py-import-checker
py-import-checker path/to/project
py-import-checker . --src src/
py-import-checker . --src src/ --src lib/
py-import-checker . --glob "app/**/*.py"
py-import-checker . --verbose
```

## Python API

```python
from pathlib import Path

from py_import_checker.checker import check_directory

result = check_directory(
    Path("src"),
    extra_paths=[Path("src")],
)

if not result.success:
    for error in result.errors:
        print(error.file, error.message)
```

## Pre-commit

```yaml
repos:
  - repo: https://github.com/matthieugraziani/py-import-checker
    rev: v0.2.4
    hooks:
      - id: py-import-checker
        args: [--src, src/]
```

## Development

```bash
pip install hatch
hatch env create
hatch run test
hatch run lint
hatch run type-check
```

## License

MIT
