# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-11-26

### Refactor
- Restructure project into modular 'mailops' package
- Move core worker scripts (dmarc_parser, spf_check, etc.) into `mailops/` directory.
- Add `__init__.py` to initialize the new package structure.
- Update `mailops.py` imports to reference the new location.
- Clean up root directory to improve project maintainability.

### Added
- **Smart Analysis:** Updated `dmarc_parser.py` to perform Reverse DNS (PTR) lookups, converting raw source IPs into human-readable hostnames.
- **Color-Coded Reporting:** Console output now highlights results in **Green** (OK), **Yellow** (Blocked/Protected), and **Red** (Investigate) for instant visual assessment.
- **Actionable Status:** Added logic to interpret DMARC results into clear action items (`OK`, `BLOCKED`, `INVESTIGATE`) rather than just raw pass/fail data.
- **Enhanced CLI Help:** Updated `mailops.py` and `dmarc_parser.py` help menus (`--help`) to include color-coded legends and "Common Usage Examples" for better usability.

### Changed
- **CSV Export:** Updated CSV output to include new `hostname` and `status_msg` columns.


## [2.1.0] - 2025-11-24
### Added
- **HTML Dashboard:** Added `--html` flag to `mailops.py report`. Generates a visual, color-coded HTML file for easier analysis.
### Fixed
- **Policy Checks:** Updated parser to correctly identify "Nil Reports" (Security scans with 0 traffic). Now reports them as "Policy Check Only" instead of silently ignoring them.



## [2.0.0] - 2025-11-24
### Released
- **Architecture Overhaul:** Refactored project from standalone scripts into a unified application.
- **Master CLI:** Added `mailops.py` as the single entry point for all tools (`check`, `fetch`, `report`, `dkim`).
- **Configuration:** Added `config.ini` support to persist settings (email, domain, paths).
- **Refactor:** Updated `blacklist_monitor.py` and `dkim_gen.py` to expose callable functions for the master CLI.

## [1.2.5] - 2025-11-24
### Documentation
- **IMAP Guide:** Added a comprehensive "Provider Setup & Troubleshooting" section to `README.md` covering iCloud, Gmail, and Outlook.
- **Usage Examples:** Updated general usage instructions for clarity across all tools.

## [1.2.4] - 2025-11-24
### Fixed
- **IMAP Protocol:** Switched from `RFC822` to `BODY[]` for more reliable fetching on iCloud.
- **Resilience:** Added a fallback mechanism to identify the email body by size if the server response structure is non-standard.
- **Stability:** Added strict type checking and flexible response parsing to prevent crashes on malformed headers.

## [1.2.3] - 2025-11-23
### Fixed
- **IMAP Parsing:** Replaced rigid index check with a loop to handle variable server response structures (fixes "Unexpected response format" on iCloud).

## [1.2.0] - 2025-11-24
### Added
- **IMAP Fetcher:** Added `imap_fetcher.py` to automatically find, download, and organize DMARC report attachments from an email inbox.

## [1.1.0] - 2025-11-24
### Added
- **Smart Resolution:** `blacklist_monitor.py` now accepts domain names (e.g., `google.com`), automatically resolves them to an IP, and scans the result.

## [1.0.0] - 2025-11-23
### Released
- **Gold Master:** Project is feature complete.
- Includes DMARC Parser, SPF Checker, DKIM Generator, and Blacklist Monitor.

## [0.8.0] - 2025-11-23
### Added
- **Blacklist Monitor:** Added `blacklist_monitor.py` to check IP reputation against common RBLs using DNS-over-HTTPS.

## [0.7.0] - 2025-11-23
### Added
- **DKIM Generator:** Added `dkim_gen.py` to generate RSA keys and formatted DNS records via system OpenSSL.

## [0.6.0] - 2025-11-23
### Added
- **SPF Checker:** Added `spf_check.py` to validate SPF records using DNS-over-HTTPS.

## [0.5.0] - 2025-11-23
### Added
- **Alert Mode:** Added `--alerts-only` flag to `dmarc_parser.py` to filter for authentication failures.

## [0.4.1] - 2025-11-23
### Fixed
- **CLI Feedback:** Improved progress reporting to show which files are being scanned.
- **Execution Logic:** Fixed a bug where the script wouldn't run when executed directly.

## [0.4.0] - 2025-11-23
### Added
- **CSV Export:** Added `--csv` flag to export data to flat files.
- **CLI Arguments:** Migrated `dmarc_parser.py` to `argparse` for robust flag handling.

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