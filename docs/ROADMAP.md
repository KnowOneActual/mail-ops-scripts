# Project Roadmap

This document outlines the planned features and improvements for `mail-ops-scripts`.

## Phase 1: DMARC Parser Enhancements
* [x] **Compression Support:** Automatically detect and parse `.gz` and `.zip` report files without manual extraction.
* [x] **Bulk Processing:** Ability to point the script at a directory and parse all XML files found within it.
* [x] **Export Options:** Add a flag (`--csv` or `--json`) to save the output for analysis in Excel or other tools.
* [x] **"Alert" Mode:** A flag to only display rows where SPF or DKIM failed (filtering out the noise).

## Phase 2: New Operational Tools
* [x] **SPF Syntax Checker:** A script to validate `v=spf1` records, checking for common errors (too many lookups, syntax typos).
* [x] **DKIM Key Generator:** A utility to generate valid 2048-bit RSA keys and the corresponding DNS TXT record format.
* [x] **Blacklist Monitor:** A script to check the domain IP against common RBLs (Real-time Blackhole Lists).

## Phase 3: Automation & Integration
* [x] **IMAP Fetcher:** A script to log into a dedicated `dmarc@` email account, download attachments, and organize them by date.
* [x] **Visualization:** Generate a simple HTML summary dashboard from parsed logs.

---
*Note: Priorities are subject to change based on operational needs.*