# Contributing

Thanks for contributing to py-import-checker.

## Development setup

Clone the repository:

```bash
git clone https://github.com/matthieugraziani/py-import-checker
cd py-import-checker
```
## Install development dependencies:
```bash
pip install hatch
hatch env create
```
## Running tests

Run the test suite:
```
hatch run test
```

## Linting and type checking

Run checks locally:
```
hatch run lint
hatch run type-check
```
To run all checks:
```
hatch run all
```
## Commit style

Conventional Commits are preferred:

| Prefix | Use for |
|--------|---------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `docs:` | Documentation changes |
| `test:` | Test changes |
| `refactor:` | Code changes without behavior changes |
| `chore:` | Tooling and maintenance |

Example:
```
feat: add exclude option
```

## Pull requests

Before opening a PR:
- Keep changes focused.
- Add tests for behavior changes.
- Run the local checks:
```
hatch run all
```
Describe what changed and why in the pull request.

## Reporting issues

For bugs, use the bug report template:
```
.github/ISSUE_TEMPLATE/bug_report.md
```
For feature requests, use:
```
.github/ISSUE_TEMPLATE/feature_request.md
```