# Changelog

## [0.2.5] — 2026-06-21

### Added

- `--fix` flag: automatically installs missing packages detected during the scan via pip, then re-scans to confirm resolution.
- `--dry-run` flag: previews which packages would be installed by `--fix` without any side-effects.
- `FailedImport.missing_module` property: extracts the top-level package name from a `ModuleNotFoundError` message.
- New `fixer` module (`py_import_checker.fixer`) exposing `fix_imports()` and `FixReport` for programmatic use.

## [Unreleased]

## [0.2.3] — 2026-06-14

### Fixed

- Fixed Hatch dynamic version configuration.
- Fixed PyPI publishing workflow.

## [0.2.2] — 2026-06-14

### Fixed

- Fixed Trusted Publishing configuration.

## [0.2.1] — 2026-06-14

### Fixed

- Fixed GitHub Actions packaging workflow.

## [0.2.0] — 2026-06-14

### Added

- Added GitHub Actions Trusted Publishing support.
- Updated project documentation.

## [0.1.0] — 2026-06-08

### Added

- Initial release.
- Import checking engine based on `importlib`.
- CLI with `--src`, `--glob`, and `--verbose`.
- Support for src-layout projects.
- GitHub Actions CI.
- Hatch-based packaging.