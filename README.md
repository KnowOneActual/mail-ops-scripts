<div align="center">
  <img src="assets/img/mail-ops-scripts.webp" alt="mail ops scripts project logo" width="200">

# Mail Ops Scripts


[![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>


A unified operational toolkit for email server administration, security analysis, and reporting.

## 🚀 COMMANDS STATUS

| Command | Status | Tech |
|---------|--------|------|
| `mailops dkim example.com` | ✅ **FULLY LIVE** | OpenSSL key generation |
| `mailops spf google.com` | ✅ **FULLY LIVE** | Google DNS-over-HTTPS |
| `mailops report --alerts` | ✅ **FILE READY** | DMARC XML parsing |
| `mailops fetch --user...` | ✅ **CREDS READY** | IMAPlib + Gmail/Outlook |

✅ LIVE = Real code executing (DKIM keys generated, SPF DNS lookups, XML parsing)
⏳ TODO = Structure ready but needs real implementation
❌ BROKEN = Import errors or crashes


## 🎯 PRODUCTION WORKFLOW

```
📥 1. Fetch reports          → mailops fetch --user you@gmail.com --password app-pass --days 7
📊 2. Analyze + alerts       → mailops report --alerts
🔍 3. SPF validation         → mailops spf yourdomain.com
🔑 4. DKIM key generation    → mailops dkim yourdomain.com --selector=mail
```

## 💾 Quick Start

```
# Clone + setup
git clone https://github.com/knowoneactual/mail-ops-scripts
cd mail-ops-scripts

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv/bin/Activate.ps1   # Windows PowerShell

# Install
pip install -e .

# Test
mailops --help
```

## 📦 INSTALL


```bash
# Global CLI

pip install mail-ops-scripts
```

# Dev workflow
```bash
git clone https://github.com/KnowOneActual/mail-ops-scripts
cd mail-ops-scripts
pip install -e '.[dev]'
black . && isort . && mypy .
```

## 📋 Commands Reference

```text
# DKIM Key Generation
mailops dkim example.com                    # default selector
mailops dkim example.com --selector=mail    # custom selector

# SPF Checking  
mailops spf google.com
mailops spf yourdomain.com

# DMARC Reports
mailops report                          # All XML files
mailops report --alerts                 # Failures only
mailops report --csv output.csv         # Export CSV

# IMAP Fetching
mailops fetch --user you@gmail.com --password app-password --days 7
mailops fetch --user user@domain.com --server imap.domain.com --days 30
```

## 🎉 Features

- ✅ **Real OpenSSL DKIM generation** → `selector.private` files
- ✅ **Google DNS-over-HTTPS SPF** → Production DNS lookups
- ✅ **DMARC XML parsing** → Console + CSV output
- ✅ **IMAP report fetching** → Gmail/Outlook/Exchange ready
- ✅ **Global CLI install** → `~/.local/bin/mailops`
- ✅ **VS Code workflow** → Python/HTML/Bash integration
- ✅ **Production ready** → Error handling + help text

## 🛠 Development

```
# Dev dependencies
pip install -e '.[dev]'

# Code quality
black .
isort .
mypy .
pytest
```

## 📦 Build & Publish

```
pip install build twine
python -m build
twine upload dist/*
```

## 📖 Changelog
[CHANGELOG.md](CHANGELOG.md)

## 🤝 Contributing
[CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License
[MIT](LICENSE)

---
**Made with ❤️ for email operations**  
[knowoneactual/mail-ops-scripts](https://github.com/knowoneactual/mail-ops-scripts)



## 🗺️ Roadmap
[![Project Board](https://github.com/users/KnowOneActual/projects/2/views/1)](https://github.com/users/KnowOneActual/projects/2/views/1)
