# Changelog Workflow

## Problem
You're keeping up with code changes but the changelog often falls behind because it requires manual updates after every commit.

## Solution
Use the **Conventional Commits** format in commit messages + automated changelog generator script.

---

## Commit Message Format

Use this format for all commits:

```
type(scope): brief description

Optional longer description with details.
```

### Commit Types

| Type | Description | Changelog Section |
|------|-------------|-------------------|
| `feat` | New feature | Added |
| `fix` | Bug fix | Fixed |
| `docs` | Documentation changes | Documentation |
| `style` | Code formatting (no logic change) | Changed |
| `refactor` | Code reorganization | Changed |
| `perf` | Performance improvements | Performance |
| `test` | Test additions/changes | Tests |
| `chore` | Maintenance tasks | Maintenance |
| `ci` | CI/CD changes | CI/CD |

### Scope (Optional)

Scope indicates the component being modified:

```
feat(dmarc_parser): add envelope_to field support
fix(cli): handle missing XML gracefully
docs(readme): update installation instructions
```

### Examples

✅ **Good commits:**
```
feat(dmarc_parser): add envelope_to field extraction
feat(csv): export envelope_to to CSV reports
fix(xml): handle missing identifiers element
docs(features): document envelope_to field
```

❌ **Poor commits:**
```
Update code
Fix bug
Small changes
wip: trying stuff
```

---

## Auto-Generate Changelog

### Preview Before Writing

```bash
cd mail-ops-scripts
python scripts/generate_changelog.py --draft --version 2.5.0
```

This shows you what the changelog will look like without modifying files.

### Generate Changelog Entry

```bash
# Create new changelog entry for v2.6.0
python scripts/generate_changelog.py --version 2.6.0 --recent 30
```

This reads the last 30 commits and generates a changelog entry.

### Append to Existing Changelog

```bash
# Prepend new version entry to existing CHANGELOG.md
python scripts/generate_changelog.py --version 2.6.0 --append
```

This adds the new entry at the top while preserving the old changelog.

---

## Command Options

```bash
usage: generate_changelog.py [-h] [--version VERSION] [--recent RECENT]
                             [--draft] [--output OUTPUT] [--append]

optional arguments:
  -h, --help            Show help message
  --version VERSION     Version number (default: Unreleased)
  --recent RECENT       Number of recent commits (default: 20)
  --draft               Preview without writing files
  --output OUTPUT       Output file (default: CHANGELOG.md)
  --append              Prepend to existing changelog
```

---

## Workflow Example

### Step 1: Make commits with proper messages

```bash
git commit -m "feat(dmarc_parser): add envelope_to field extraction"
git commit -m "feat(csv): include envelope_to in exports"
git commit -m "fix(xml): handle missing identifiers gracefully"
git commit -m "docs(features): document new envelope_to field"
```

### Step 2: Preview changelog

```bash
python scripts/generate_changelog.py --draft --version 2.6.0 --recent 10
```

Output:
```
📄 Preview: Changelog for v2.6.0

Found 4 commits

## [2.6.0] - 2025-12-26

### Added
- Add envelope_to field extraction ([abc1234])
- Include envelope_to in exports ([def5678])

### Fixed
- Handle missing identifiers gracefully ([ghi9012])

### Documentation
- Document new envelope_to field ([jkl3456])
```

### Step 3: Write changelog

```bash
# Option A: Create new changelog
python scripts/generate_changelog.py --version 2.6.0 --recent 10

# Option B: Append to existing changelog (prepends entry)
python scripts/generate_changelog.py --version 2.6.0 --recent 10 --append
```

### Step 4: Review and commit

```bash
# Review the generated changelog
cat CHANGELOG.md

# Stage and commit
git add CHANGELOG.md
git commit -m "docs: update changelog for v2.6.0"
git tag -a v2.6.0 -m "Release v2.6.0"
```

---

## Integration Tips

### Use with Git Hooks (Pre-commit)

Create `.git/hooks/prepare-commit-msg` to remind you about commit format:

```bash
#!/bin/bash
echo "Reminder: Use format: type(scope): description"
echo "  feat(scope), fix(scope), docs(scope), etc."
```

### Use with CI/CD

Automate changelog generation on release:

```yaml
# .github/workflows/release.yml
- name: Generate Changelog
  run: |
    python scripts/generate_changelog.py \
      --version ${{ github.ref_name }} \
      --recent 50 \
      --append
```

### Use with Pre-commit Framework

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: check-commit-format
      name: Check commit format
      entry: python scripts/validate_commits.py
      language: python
      stages: [commit-msg]
```

---

## Current Status

Your `mail-ops-scripts` repo now has:
- ✅ Conventional Commits setup in recent commits
- ✅ Automated changelog generator script
- ✅ This documentation

### Next Time You Release

1. Make commits with proper `feat:`, `fix:`, etc. format
2. Run: `python scripts/generate_changelog.py --draft --version X.Y.Z`
3. Review the preview
4. Run: `python scripts/generate_changelog.py --version X.Y.Z --append`
5. Commit and tag

**No more manual changelog updates!** 🎉

---

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
