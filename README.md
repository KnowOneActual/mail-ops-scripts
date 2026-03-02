<div align="center">
  <img src="assets/img/mail-ops-scripts.webp" alt="mail ops scripts project logo" width="200">

# Mail Ops Scripts

[![PyPI Version](https://img.shields.io/pypi/v/mail-ops-scripts?color=blue&style=flat-square)](https://pypi.org/project/mail-ops-scripts/)
[![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml)
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A unified operational toolkit for email server administration, security analysis, and reporting.**

### 🚀 Now available on PyPI!
You can now install `mailops` globally with a single command.

</div>

---

## ⚡ Quick Start

Get the CLI installed directly from PyPI and start managing your mail operations in seconds.

```bash
# Install via pipx (recommended for isolated CLI tools)
pipx install mail-ops-scripts

# Or via pip
pip install mail-ops-scripts

# Verify installation
mailops --help
```

> **Note:** If you don't have `pipx` yet, you can install it via Homebrew (`brew install pipx`) on macOS, or follow the [official installation guide](https://pypa.github.io/pipx/).

## 🛠 The Toolkit

`mailops` is a single binary aimed at simplifying the fragmented world of email admin. No more juggling random bash scripts or online DNS checkers.

| Command | Description |
| :--- | :--- |
| **`mailops fetch`** | Connects to Gmail/Exchange via IMAP to download DMARC reports. |
| **`mailops report`** | Parses XML reports (.xml, .gz, .zip) from a folder or file into readable tables or CSVs. |
| **`mailops spf`** | Validates SPF records using Google's DNS-over-HTTPS (secure & cached). |
| **`mailops dkim`** | Generates 2048-bit RSA keys and formats the exact DNS TXT record you need. |

## 🚀 Common Workflows

### 1. The "Monday Morning" Check

Grab the last week's DMARC reports from your dedicated inbox and see if anyone is spoofing you.

```bash
# 1. Download reports from your dmarc@ account
mailops fetch --user admin@example.com --password "app-password" --days 7

# 2. Analyze the data (view alerts only)
mailops report --alerts
```

### 2. Setting Up a New Domain

Spinning up a new sender? Generate your security keys and validate your DNS instantly.

```bash
# 1. Generate DKIM keys (outputs to ./default.private)
mailops dkim example.com --selector=mail

# 2. Verify your SPF record is live and valid
mailops spf example.com
```

### 3. Generate DMARC Analysis Report

Analyze reports in your current directory, a specific folder, or even a single file.

```bash
# Display all records in current directory
mailops report

# Analyze reports in a specific folder
mailops report ./my_logs/

# Analyze a single XML file
mailops report report.xml

# Export all records to CSV
mailops report --csv dmarc_analysis.csv
```

## 📊 Report Command Features

The `mailops report` command analyzes DMARC XML reports and provides:

- **Formatted Tables**: Color-coded analysis of SPF, DKIM, and DMARC policy results
- **Alert Filtering**: `--alerts` flag to show only authentication failures and spoofing attempts
- **CSV Export**: `--csv` flag to save results for further analysis
- **Compressed Format Support**: Automatically handles `.xml`, `.xml.gz`, and `.zip` files
- **Organized Output**: Groups results by organization and date range

### Report Output Example

```bash
$ mailops report
📊 Analyzing REAL DMARC reports...
Found 5 XML files:
  📄 enterprise.protection.outlook.com!example.com!1765324800!1765411200.xml.gz
  ...

Report: enterprise.protection.outlook.com (2025-12-01)
─────────────────────────────────────────────────────────────────────────
Source IP           | Hostname                   | Cnt | SPF  | DKIM | Analysis
─────────────────────────────────────────────────────────────────────────
192.168.1.1         | mail.example.com           | 42  | pass | pass | OK
10.0.0.5            | suspicious.domain          | 3   | fail | fail | INVESTIGATE
```

## 📦 Developer Setup

If you want to contribute or modify the scripts, here is how to get the dev environment running locally.

```bash
# Clone and setup
git clone https://github.com/knowoneactual/mail-ops-scripts
cd mail-ops-scripts

# Create virtual env
python -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e '.[dev]'

# Run the test suite
pytest

# Format and lint code with Ruff (fast & unified)
ruff format .
ruff check --fix .
```

## 🤝 Contributing

We want to keep this lightweight and portable.

* **Standard Libs First**: Trying to avoid external dependencies to ensure the tool runs anywhere.
* **Code Style**: Using**Ruff** for high-performance, unified linting and formatting.
* **See details**: Check [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## 📄 License

MIT © [KnowOneActual](LICENSE)

---

**Made with ❤️ for email operations**

## 🗺️ Roadmap

[![Project Board](https://github.com/users/KnowOneActual/projects/2/views/1)](https://github.com/users/KnowOneActual/projects/2/views/1)
