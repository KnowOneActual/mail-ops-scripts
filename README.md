# Mail Ops Scripts

A collection of Python utilities for email server administration, security analysis, and reporting.

## Tools Included

### 1. DMARC XML Parser (`dmarc_parser.py`)
A lightweight, dependency-free script to parse DMARC aggregate reports (XML format). It converts the raw XML data into a readable CLI summary, helping you quickly identify:
* Source IPs sending mail on your behalf.
* SPF and DKIM authentication results.
* Policy actions taken (None, Quarantine, Reject).

## Prerequisites

* Python 3.x
* Standard libraries only (no `pip install` required for current scripts).

## Usage

### Parsing a DMARC Report
Download your DMARC XML report (extract it if it is a `.zip` or `.gz` file), then run:

```bash
python dmarc_parser.py /path/to/report.xml
````

**Example Output:**

```text
--- Report for google.com ---
Period: 2025-11-20 00:00 to 2025-11-21 23:59
------------------------------------------------------------
Source IP            | Count | SPF    | DKIM   | Disposition
------------------------------------------------------------
209.85.220.41        | 15    | pass   | pass   | none
192.0.2.1            | 2     | fail   | none   | quarantine
```

## Roadmap

  * [ ] Automated `.gz` / `.zip` extraction.
  * [ ] SPF record syntax checker.
  * [ ] Bulk processing for directory of reports.

## License

MIT

````

### 2. A quick privacy tip (The `.gitignore`)

Since you are dealing with security logs, you definitely don't want to accidentally commit your actual XML reports to GitHub. They contain IP addresses and internal data.

Create a file named `.gitignore` in the same folder and add this:

```text
# Ignore DMARC reports
*.xml
*.gz
*.zip

# Ignore Python cache
__pycache__/
*.pyc

# Ignore Mac system files
.DS_Store
````