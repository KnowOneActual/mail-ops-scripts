<div align="center">
  <img src="assets/img/mail-ops-scripts.webp" alt="mail ops scripts project logo" width="200">

# Mail Ops Scripts

[![PyPI Version](https://img.shields.io/pypi/v/mail-ops-scripts?color=blue&style=flat-square)](https://pypi.org/project/mail-ops-scripts/)
[![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
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
# Install via pip
pip install mail-ops-scripts

# Verify installation
mailops --help
````

## 🛠 The Toolkit

`mailops` is a single binary aimed at simplifying the fragmented world of email admin. No more juggling random bash scripts or online DNS checkers.

| Command | Description |
| :--- | :--- |
| **`mailops fetch`** | Connects to Gmail/Exchange via IMAP to download DMARC reports. |
| **`mailops report`** | Parses XML reports into readable stats or CSVs. |
| **`mailops spf`** | Validates SPF records using Google's DNS-over-HTTPS (secure & cached). |
| **`mailops dkim`** | Generates 2048-bit RSA keys and formats the exact DNS TXT record you need. |

## 🚀 Common Workflows

### 1\. The "Monday Morning" Check

Grab the last week's DMARC reports from your dedicated inbox and see if anyone is spoofing you.

```bash
# 1. Download reports from your dmarc@ account
mailops fetch --user admin@example.com --password "app-password" --days 7

# 2. Analyze the data (view alerts only)
mailops report --alerts
```

### 2\. Setting Up a New Domain

Spinning up a new sender? Generate your security keys and validate your DNS instantly.

```bash
# 1. Generate DKIM keys (outputs to ./default.private)
mailops dkim example.com --selector=mail

# 2. Verify your SPF record is live and valid
mailops spf example.com
```

## 📦 Developer Setup

If you want to contribute or modify the scripts, here is how to get the dev environment running locally.

```bash
# Clone and setup
git clone [https://github.com/knowoneactual/mail-ops-scripts](https://github.com/knowoneactual/mail-ops-scripts)
cd mail-ops-scripts

# Create virtual env
python -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e '.[dev]'

# Run the test suite
pytest
```

## 🤝 Contributing

We want to keep this lightweight and portable.

  * **Standard Libs First**: We try to avoid external dependencies to ensure the tool runs anywhere.
  * **Code Style**: We use `black` and `isort`.
  * **See details**: Check [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## 📄 License

MIT © [KnowOneActual](LICENSE)

---
**Made with ❤️ for email operations**  

## 🗺️ Roadmap
[![Project Board](https://github.com/users/KnowOneActual/projects/2/views/1)](https://github.com/users/KnowOneActual/projects/2/views/1)
