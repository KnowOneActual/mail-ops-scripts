# Changelog

## [2.4.0] - 2025-12-16
**🐛 BUGFIX RELEASE - Report Command Fixed!**

### 🔧 Fixed
- **Report command output missing** - `mailops report` now displays formatted analysis table (was only showing file list)
- **Compressed files not found** - Added support for discovering `.gz` and `.zip` reports (was ignoring compressed files)
- **Alerts filter broken** - `--alerts` flag now properly filters to show only failures and spoofing attempts

### ✨ Improvements
- **Help text documentation** - `mailops report --help` now shows `--csv` flag with examples
- **CSV export** - Clearly documented in help: `mailops report --csv results.csv`
- **Better descriptions** - All report flags now have detailed descriptions in help output
- **Code formatting** - Applied Black formatter for consistent code style

### 📊 Report Command Features
- Parses DMARC XML in `.xml`, `.xml.gz`, and `.zip` formats
- Displays color-coded analysis of SPF/DKIM/DMARC results
- `--alerts` flag filters to show only authentication failures
- `--csv FILE` flag exports results to CSV for further analysis
- Combines `--alerts --csv` to export only failures

### Example Usage
```bash
# Display all records
mailops report

# Show only security failures
mailops report --alerts

# Export all records to CSV
mailops report --csv analysis.csv

# Export only failures to CSV
mailops report --alerts --csv alerts.csv
```

### 👋 Technical
- PR #4: Comprehensive bug fix and documentation update
- Commits:
  - `e66931ab` - Core functionality fixes
  - `30cbc25b` - Help text documentation
  - `b4b4af27` - Black formatter compliance
  - `cbc7319b` - README and CHANGELOG updates

### 📁 Files Changed
- `mailops/cli.py` - Report command fixes and help text
- `README.md` - Added report command features and examples
- `CHANGELOG.md` - This entry

---

## [2.3.0] - 2025-11-28
**🎉 PyPI PRODUCTION SHIPPED!**

### 🚀 Released
- **LIVE on PyPI**: https://pypi.org/project/mail-ops-scripts/2.3.0/
- **Global install**: `pip install mail-ops-scripts`
- **4x LIVE commands**: `mailops dkim`, `spf`, `report`, `fetch`

### 🟢 CI/CD Complete
- **GitHub Actions**: 🟢 GREEN (black/isort/mypy/pytest)
- **Dev workflow**: `pip install -e '.[dev]'`
- **Badges**: ![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)

### 📚 Enterprise Documentation
- **README.md**: Logo + badges + LIVE command table
- **CONTRIBUTING.md**: VS Code Python/HTML/Bash workflow
- **pyproject.toml**: Perfect (license + dev deps)

---

## [2.2.0] - 2025-11-28
**🎉 PRODUCTION CLI COMPLETE!**

### ✨ New Features
- **✅ REAL 4-command CLI:**
  - `mailops dkim example.com` - OpenSSL DKIM key generation
  - `mailops spf google.com` - Google DoH SPF DNS lookups  
  - `mailops report --alerts` - DMARC XML parsing + alerts
  - `mailops fetch --user...` - IMAP report fetching
- **✅ Global install:** `~/.local/bin/mailops` + pip entry points
- **✅ Production workflow:** fetch → report → spf → dkim
- **✅ VS Code ready:** Python/HTML/Bash integration

### 🐛 Fixes
- Fixed `args.pass` → `args.password` syntax error
- Fixed all import errors (`generate_keys`, `fetch_spf_record`)
- Fixed pyproject.toml TOML syntax + duplicates
- Fixed zsh globbing: `pip install -e '.[dev]'`

### 💿 Build
- ✅ `python -m build` ready
- ✅ PyPI deployable: `twine upload dist/*`

---

## [2.1.0] - 2025-11-26
- Initial CLI structure + module imports
- Basic argparse subparsers

## [2.0.0] - 2025-11-26
- Core modules: dkim_gen, spf_check, dmarc_parser, imap_fetcher
