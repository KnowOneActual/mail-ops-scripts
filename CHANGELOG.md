# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2025-11-23
### Added
- **SPF Checker:** Added `spf_check.py` to validate SPF records using DNS-over-HTTPS.

## [0.5.0] - 2025-11-23
### Added
- **Alert Mode:** Added `--alerts-only` flag to `dmarc_parser.py` to filter for authentication failures.

## [0.4.1] - 2025-11-23
### Fixed
- **CLI Feedback:** improved progress reporting to show which files are being scanned.
- **Execution Logic:** Fixed a bug where the script wouldn't run when executed directly.

## [0.4.0] - 2025-11-23
### Added
- **CSV Export:** Added `--csv` flag to export data to flat files.
- **CLI Arguments:** Migrated to `argparse` for robust flag handling.

## [0.3.0] - 2025-11-23
### Added
- **Bulk Processing:** Added support for scanning entire directories for reports.

## [0.2.0] - 2025-11-23
### Added
- **Compression Support:** Added native handling for `.gz` and `.zip` archives.

## [0.1.0] - 2025-11-23
### Added
- Initial project structure.
- `dmarc_parser.py`: Basic XML parsing for DMARC reports.
- `ROADMAP.md`: Future feature planning.
- `README.md`: Usage instructions.
