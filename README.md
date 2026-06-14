<p align="center">
  <h1 align="center">py-import-checker</h1>
  <p align="center">
    <strong>Fast, zero-dependency Python import health scanner.</strong>
  </p>

  <p align="center">
    Recursively scan any Python project and instantly surface every broken or missing import — 
    <strong>before your tests run, before CI fails, before runtime surprises you.</strong>
  </p>

  <p align="center">
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

```text
py-import-checker src/ --src src/

  py-import-checker  —  Python import health scanner

  Scanning  /home/user/myproject/src

──────────────────────────────────────────────────
  ✗  mypackage/broken_module.py
     ModuleNotFoundError: No module named 'nonexistent_lib'

──────────────────────────────────────────────────
✗ 1 broken import(s) found in 14 file(s) scanned.

```

## Features

- **Zero dependencies** — uses only the Python standard library (`importlib`, `pathlib`, `sys`)
- **src-layout aware** — pass `--src` to add extra directories to `sys.path`
- **Noise-free** — only reports `ImportError` / `ModuleNotFoundError`; ignores runtime exceptions
- **Auto-skips** virtual environments (`.venv`, `venv`) and build artefacts
- **CI-friendly** — exits with code `1` on any broken import, `0` on success
- **Self-checking** — the CI pipeline scans itself with `py-import-checker`


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
Add this to your `.pre-commit-config.yaml`:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/matthieugraziani/py-import-checker
    rev: v0.2.2
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



## How it works

py-import-checker uses `importlib.util.spec_from_file_location` to load each `.py` file in an isolated namespace. Only import errors are captured — everything else (runtime exceptions, missing variables, etc.) is ignored.


## Roadmap (suggestions)

- Mode --fix (suggestions d’imports)
- Support des packages namespace (__init__.py moins strict)
- Intégration VS Code / LSP
- Rapport HTML / JSON
- Détection de circular imports (optionnel)

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

## License - MIT

Auteur : Matthieu Graziani
```text
### Améliorations apportées
- En-tête centré + badges propres
- Démo plus visible
- Sections plus aérées
- Roadmap ajoutée (pour montrer l’évolution)
- Meilleure lisibilité

### Actions prioritaires maintenant
1. **Publier sur PyPI** (version 0.2.3) :
   ```bash
   hatch build
   hatch publish
```