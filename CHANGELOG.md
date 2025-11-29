# Changelog

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

### 📦 Build
- ✅ `python -m build` ready
- ✅ PyPI deployable: `twine upload dist/*`

---

## [2.1.0] - 2025-11-26
- Initial CLI structure + module imports
- Basic argparse subparsers

## [2.0.0] - 2025-11-26
- Core modules: dkim_gen, spf_check, dmarc_parser, imap_fetcher
