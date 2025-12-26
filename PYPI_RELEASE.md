# PyPI Release Guide for mail-ops-scripts v2.5.0

## 🎉 Release Status: ✅ COMPLETED

**Released**: December 26, 2025  
**Version**: 2.5.0  
**PyPI**: https://pypi.org/project/mail-ops-scripts/2.5.0/

### What's Live
- ✅ envelope_to field support
- ✅ Console output with new column
- ✅ CSV export enhancement
- ✅ Complete documentation
- ✅ Available via `pip install mail-ops-scripts`

---

## Prerequisites

1. **PyPI Account**: You need a PyPI account at https://pypi.org/
2. **API Token**: Create an API token at https://pypi.org/manage/account/
3. **Build Tools**: Install build and twine

```bash
pip install build twine
```

4. **Configuration** (Optional): Create `~/.pypirc` for automatic authentication:

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your PyPI API token
```

## Step-by-Step Release Process (Reference)

### 1. Verify Version is Updated ✅

Already done:
```toml
[project]
version = "2.5.0"
```

### 2. Verify Changelog is Updated ✅

Already updated in CHANGELOG.md with:
- envelope_to field support
- Console output changes
- CSV export enhancements

### 3. Create Git Tag ✅

```bash
git tag -a v2.5.0 -m "Release v2.5.0 - Add envelope_to field support"
git push origin v2.5.0
```

### 4. Build Distribution Packages ✅

```bash
python -m build
```

This creates:
- `dist/mail-ops-scripts-2.5.0.tar.gz` (source distribution)
- `dist/mail-ops-scripts-2.5.0-py3-none-any.whl` (wheel)

### 5. Verify Build Integrity ✅

```bash
twine check dist/*
```

Output:
```
Checking distribution dist/mail-ops-scripts-2.5.0.tar.gz: Passed
Checking distribution dist/mail-ops-scripts-2.5.0-py3-none-any.whl: Passed
```

### 6. Upload to TestPyPI (Optional)

Test first to catch any issues:

```bash
twine upload --repository testpypi dist/*
```

Then test install:
```bash
pip install --index-url https://test.pypi.org/simple/ mail-ops-scripts==2.5.0
```

### 7. Upload to Production PyPI ✅

```bash
twine upload dist/*
```

Credentials:
```
Enter your username: __token__
Enter your password: pypi-AgEIcHlwaS5vcmc...
```

### 8. Verify Release on PyPI ✅

Visit: https://pypi.org/project/mail-ops-scripts/

Shows:
- Version: **2.5.0**
- Release Date: **2025-12-26**
- Latest Release with envelope_to support

### 9. Create GitHub Release

Manually or via GitHub CLI:

```bash
# Using GitHub CLI (if installed)
gh release create v2.5.0 -t "Release v2.5.0" -n "envelope_to Field Support"
```

Or manually:
1. Go to https://github.com/KnowOneActual/mail-ops-scripts/releases
2. Click "Draft a new release"
3. Tag: `v2.5.0`
4. Title: "v2.5.0 - envelope_to Field Support"
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

## Installation Verification ✅

Users can now install:

```bash
# Install latest version
pip install --upgrade mail-ops-scripts

# Verify version
python -c "import mailops; print(mailops.__version__)" 
```

Or:
```bash
mailops --version
```

## What Gets Released

The distribution includes:

```
mail-ops-scripts-2.5.0/
├── mailops/
│   ├── __init__.py
│   ├── cli.py
│   ├── dmarc_parser.py       ✨ (Updated with envelope_to)
│   ├── imap_fetcher.py
│   ├── spf_check.py
│   ├── dkim_gen.py
│   └── ui.py
├── tests/
├── docs/
│   └── FEATURES.md          ✨ (New)
├── README.md
├── LICENSE
├── pyproject.toml           ✨ (v2.5.0)
├── CHANGELOG.md             ✨ (Updated)
└── debug_xml_structure.py   ✨ (New diagnostic tool)
```

## Post-Release Checklist ✅

- ✅ Version bumped to 2.5.0 in pyproject.toml
- ✅ CHANGELOG.md updated and released
- ✅ Git tagged with v2.5.0
- ✅ Distribution packages built and verified
- ✅ Uploaded to PyPI
- ✅ Documentation updated
- ✅ Fresh installation tested

## Troubleshooting (Reference)

### Issue: "Invalid distribution on server"
- Verify with: `twine check dist/*`
- Check pyproject.toml format
- Ensure version matches regex: `\d+\.\d+\.\d+`

### Issue: "403 Forbidden"
- Verify PyPI token is correct
- Check token hasn't expired
- Use `__token__` as username (not your account name)

### Issue: "Already exists"
- Version already uploaded; increment to v2.5.1 or contact PyPI support

## Questions?

Reference:
- PyPI Project: https://pypi.org/project/mail-ops-scripts/
- GitHub Repo: https://github.com/KnowOneActual/mail-ops-scripts
- PyPI Guide: https://packaging.python.org/tutorials/packaging-python-projects/
- Twine Docs: https://twine.readthedocs.io/
- setuptools: https://setuptools.readthedocs.io/
