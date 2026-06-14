# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.1.0] — 2026-06-08

### Added
- Core `check_directory()` engine using `importlib.util`
- Zero dependencies — stdlib only
- CLI (`py-import-checker`) with `--src`, `--glob`, `--verbose` flags
- src-layout support via `--src` (repeatable)
- Auto-skip `.venv`, `venv`, `__pycache__`, `dist`, `build`
- Exit codes: `0` success · `1` broken imports · `2` bad args
- 9 unit tests (checker + CLI)
- GitHub Actions CI: Python 3.9–3.12 matrix + self-scan job
- `pyproject.toml` with Hatchling, ruff, mypy

[Unreleased]: https://github.com/matthieugraziani/py-import-checker/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/matthieugraziani/py-import-checker/releases/tag/v0.1.0