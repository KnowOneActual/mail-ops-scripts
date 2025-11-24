# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.5] - 2025-11-23
### Documentation
- **IMAP Guide:** Added a comprehensive "Provider Setup & Troubleshooting" section to `README.md` covering iCloud, Gmail, and Outlook.
- **Usage Examples:** Updated general usage instructions for clarity across all tools.

## [1.2.4] - 2025-11-23
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