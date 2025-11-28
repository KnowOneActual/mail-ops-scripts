## Version 2.3.0: CLI, Packaging, and Test Foundation

- Add a proper CLI entry point in `pyproject.toml` (e.g. `mailops = mailops.cli:main`) so users can run `mailops ...` directly.
- Move all command logic (check, fetch, report, dkim) into submodules, keeping `mailops.py` as CLI glue.
- List all actual dependencies under `project.dependencies` to ensure reliable installs.
- Build a minimal test suite (`tests/`) for SPF parsing, DMARC XML analysis, and DKIM generation using `pytest`.
- Expand the CI workflow to run lint (black/isort/ruff), type check (mypy), and test on Python 3.8–3.12.

## Version 2.4.0: Dashboard Upgrade and Enhanced Logging

- Add a `mailops serve` subcommand to launch a local web server for quick report browsing.
- Switch from print to the `logging` module. Add `--verbose`/`--quiet` flags.
- Create a single config loader that reads `.ini` and environment variables, with validation and helpful errors.
- Document the security model and supported operations in the README.

## Version 2.5.0: Advanced UX and Extensibility

- Implement dry-run modes for DNS/IMAP/network checks.
- Allow flexible custom RBL lists or DMARC indicators via simple config/extension hooks.
- Expand CI to build and upload releases to TestPyPI on tag (optionally automate real PyPI publish).
- Broaden tests to cover error and edge cases in every subcommand.