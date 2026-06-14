# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.2.3] — 2026-06-14

### Fixed
- Fixed `pyproject.toml` version conflict: `version` was statically set in `[project]` while `[tool.hatch.version]` also pointed to a dynamic source, causing `hatch build` to fail.
- Switched to fully dynamic versioning (`dynamic = ["version"]`), sourced from `src/py_import_checker/__init__.py`.
- First successful publish to PyPI.

## [0.2.2] — 2026-06-14

### Fixed
- Fixed Trusted Publishing configuration in GitHub Actions workflow.
- Resolved `invalid-publisher` error by aligning workflow name with PyPI publisher configuration.

## [0.2.1] — 2026-06-14

### Fixed
- Fixed GitHub Actions workflow error: `Unable to resolve action pypa/hatch-install` by switching to standard Python setup.

## [0.2.0] — 2026-06-14

### Added
- Added full support for Trusted Publishing via GitHub Actions OIDC.
- Comprehensive `README.md` update for PyPI professional presentation.

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

[Unreleased]: https://github.com/matthieugraziani/py-import-checker/compare/v0.2.3...HEAD
[0.2.3]: https://github.com/matthieugraziani/py-import-checker/releases/tag/v0.2.3
[0.2.2]: https://github.com/matthieugraziani/py-import-checker/releases/tag/v0.2.2
[0.2.1]: https://github.com/matthieugraziani/py-import-checker/releases/tag/v0.2.1
[0.2.0]: https://github.com/matthieugraziani/py-import-checker/releases/tag/v0.2.0
[0.1.0]: https://github.com/matthieugraziani/py-import-checker/releases/tag/v0.1.0