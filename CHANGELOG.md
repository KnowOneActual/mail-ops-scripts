# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Planned
- Multi-domain filtering in report output
- Enhanced alert severity levels
- Report scheduling/automation features
- Integration with external security tools

## [2.5.2] - 2026-03-01

### Added
- **Custom path support for reports**: The `report` command now accepts an optional path argument.
  - Can point to a specific directory containing reports (e.g., `mailops report ./logs`).
  - Can point to a single XML, GZ, or ZIP file (e.g., `mailops report data.xml`).
  - Defaults to the current directory if no path is provided.
  - Recursively checks `reports/` subdirectory if a directory is specified.

## [2.5.1] - 2026-03-01

### Fixed
- Improved PyPI distribution metadata and installation documentation.

## [2.5.0] - 2025-12-26

### Added
- **envelope_to field support**: DMARC reports now extract and display the `<envelope_to>` value from XML reports
  - Added `envelope_to` column to console report output
  - Added `envelope_to` field to CSV exports
  - Field extracted from `feedback/record/identifiers/envelope_to` in DMARC XML structure
- Comprehensive feature documentation in `docs/FEATURES.md`
- Diagnostic tool: `debug_xml_structure.py` for XML inspection and debugging

### Changed
- Console report table width increased to 130 characters to accommodate new envelope_to column
- Report table format now shows: Source IP | Envelope To | Hostname | Cnt | SPF | DKIM | Analysis
- Updated PyPI package with complete release documentation

### Fixed
- Improved XML parsing with explicit `identifiers` element handling
- Better error handling for missing XML fields

## [2.4.0] - Previous Release

### Added
- DMARC XML parsing and reporting
- CSV export functionality
- Alert filtering for authentication failures
- Support for .xml, .xml.gz, and .zip file formats
- DKIM key generation
- SPF record checking
- IMAP report fetching
