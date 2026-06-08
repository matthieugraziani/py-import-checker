# Contributing to py-import-checker

Thank you for considering contributing! This document explains how to get started.

---

## Development setup

```bash
git clone https://github.com/matthieugraziani/py-import-checker
cd py-import-checker
pip install -e ".[dev]"
```

Add a `[project.optional-dependencies]` section in `pyproject.toml` if you need extra dev deps:

```toml
[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
```

---

## Running tests

```bash
pytest
```

All tests must pass before opening a PR.

---

## Linting & type-checking

```bash
ruff check src/ tests/
mypy src/
```

---

## Commit style

Use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | When to use |
|--------|------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `test:` | Adding or fixing tests |
| `refactor:` | Code change without feature/fix |
| `chore:` | Tooling, CI, dependencies |

Example: `feat: add --exclude flag to skip specific paths`

---

## Opening a Pull Request

1. Fork the repo and create a branch from `main`.
2. Make your changes with tests.
3. Run `ruff`, `mypy`, and `pytest` locally — all must pass.
4. Open a PR and fill in the template.

---

## Reporting bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) issue template.

## Requesting features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) issue template.