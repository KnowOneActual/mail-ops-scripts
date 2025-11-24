<div align="center">
  <img src="assets/img/mail-ops-scripts.webp" alt="mail ops scripts project logo" width="200">


# Mail Ops Scripts

# **Under Development**
</div>

[![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml)

A collection of lightweight, dependency-free Python utilities for email server administration, security analysis, and reporting.

## Tools Included

### 1. DMARC XML Parser (`dmarc_parser.py`)
A robust analyzer for DMARC aggregate reports. It handles single XML files, compressed archives (`.gz`, `.zip`), or entire directories of mixed reports.

**Key Features:**
* **Bulk Processing:** Scans folders recursively for reports.
* **Auto-Decompression:** Reads `.gz` and `.zip` files on the fly.
* **CSV Export:** Converts complex XML data into flat CSVs for Excel/Sheets.
* **Alert Mode:** Filters output to show *only* authentication failures (SPF/DKIM).

### 2. SPF Syntax Checker (`spf_check.py`)
A security tool to validate DNS records without needing external libraries (uses Google's DNS-over-HTTPS API).

**Checks Performed:**
* **Syntax:** Validates `v=spf1` structure.
* **RFC Limits:** Warns if DNS lookups exceed the limit of 10.
* **Security:** Flags dangerous policies like `+all` or `?all`.

### 3. DKIM Key Generator (`dkim_gen.py`)
Generates secure 2048-bit RSA keys for email signing. Uses your system's `openssl` to avoid Python dependencies.


---

## Prerequisites

* Python 3.x
* **No `pip install` required.** All scripts use standard libraries.

---

## Usage

### Using the DMARC Parser

**1. Basic Summary (Console)**
View a human-readable summary of a single file or an entire folder:
```bash
python dmarc_parser.py ./your_folder
````

**2. Export to CSV**
Save the parsed data to a file for analysis in Excel:

```bash
python dmarc_parser.py ./your_folder  --csv report_analysis.csv
```

**3. Security Audit (Alert Mode)**
Only display rows where SPF or DKIM failed:

```bash
python dmarc_parser.py ./your_folder --alerts-only
```

### Using the SPF Checker

**Check a domain's record:**

```bash
python spf_check.py google.com
```

### Using the DKIM Generator
**Usage:**
```bash
# Syntax: python dkim_gen.py <selector> --domain <domain>
python dkim_gen.py mail --domain example.com
```

-----

## License

MIT License. See [LICENSE](LICENSE) 
