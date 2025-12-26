# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **envelope_to field support**: DMARC reports now extract and display the `<envelope_to>` value from XML reports
  - Added `envelope_to` column to console report output
  - Added `envelope_to` field to CSV exports
  - Field extracted from `feedback/record/identifiers/envelope_to` in DMARC XML structure

### Changed
- Console report table width increased to 130 characters to accommodate new envelope_to column
- Report table format now shows: Source IP | Envelope To | Hostname | Cnt | SPF | DKIM | Analysis

## [1.2.0] - Previous Release

### Added
- DMARC XML parsing and reporting
- CSV export functionality
- Alert filtering for authentication failures
- Support for .xml, .xml.gz, and .zip file formats
- DKIM key generation
- SPF record checking
- IMAP report fetching
