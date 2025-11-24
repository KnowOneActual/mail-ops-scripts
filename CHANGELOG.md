# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-11-23

### Added
- CSV Export: Added `--csv` flag to export parsed data to a flat CSV file.
- CLI Arguments: Migrated to `argparse` for robust command-line handling.

## [0.3.0] - 2025-11-23

### Added
- Bulk processing: Can now pass a directory path to process all `.xml`, `.gz`, and `.zip` files inside it.
- Improved filename reporting in the output header.

## [0.2.0] - 2025-11-23

### Added
- Compression support: Now parses `.gz` and `.zip` archives directly.

## [0.1.0] - 2025-11-23

### Added
- Initial project structure.
- `dmarc_parser.py`: Basic XML parsing for DMARC reports.
- `ROADMAP.md`: Future feature planning.
- `README.md`: Usage instructions.

