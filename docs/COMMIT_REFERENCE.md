# Commit Message Quick Reference

## TL;DR

```bash
# Format: type(scope): description
git commit -m "feat(dmarc_parser): add envelope_to field extraction"
```

---

## Commit Types

| Type | Use When | Example |
|------|----------|----------|
| **feat** | Adding new feature | `feat(report): add filtering by domain` |
| **fix** | Fixing bug | `fix(parser): handle missing XML elements` |
| **docs** | Writing/updating docs | `docs(readme): add installation steps` |
| **style** | Code formatting only | `style(cli): format with black` |
| **refactor** | Reorganizing code | `refactor(parser): simplify XML extraction` |
| **perf** | Improving performance | `perf(csv): reduce memory usage` |
| **test** | Adding/fixing tests | `test(parser): add envelope_to tests` |
| **chore** | Maintenance tasks | `chore: bump version to 2.5.0` |
| **ci** | CI/CD changes | `ci: add GitHub Actions workflow` |

---

## Real Examples from Your Repo

### Good ✅

```bash
# Feature with scope
feat(dmarc_parser): add envelope_to field extraction

# Multiple features
feat(csv): export envelope_to to CSV reports
feat(console): display envelope_to in table output

# Fixes with scope
fix(xml): handle missing identifiers element gracefully
fix(cli): prevent crash on missing XML files

# Documentation
docs(features): document envelope_to field
docs(changelog): add workflow documentation

# Maintenance
chore: bump version to 2.5.0
style(cli): format code to comply with black
```

### Poor ❌

```bash
Update code           # ← Too vague
Fix bug               # ← Which bug?
Small changes         # ← Not descriptive
work in progress      # ← Should be WIP branch instead
add stuff             # ← Too vague
```

---

## Multi-line Commits (For Complex Changes)

```bash
git commit
```

Then in your editor:

```
feat(dmarc_parser): add envelope_to field support

Adds extraction and display of envelope_to field from DMARC XML reports.
This field indicates the recipient domain targeted by email sources.

Changes:
- Extract envelope_to from feedback/record/identifiers/envelope_to
- Display in console table output
- Include in CSV exports
- Handle missing fields gracefully

Fixes: #123
Closes: #456
```

---

## Automatic Changelog Generation

Once you use proper commit messages, generate changelog automatically:

```bash
# Preview (don't write)
python scripts/generate_changelog.py --draft --version 2.6.0

# Generate and prepend to CHANGELOG.md
python scripts/generate_changelog.py --version 2.6.0 --append --recent 30
```

The script reads commit messages and organizes them:
- `feat:` → **Added**
- `fix:` → **Fixed**
- `docs:` → **Documentation**
- `perf:` → **Performance**
- etc.

---

## Tips & Tricks

### 1. **Use Imperative Mood**

✅ Good: `add envelope_to field extraction`  
❌ Bad: `added envelope_to field extraction` or `adding envelope_to...`

### 2. **Reference Issues**

```bash
feat(parser): add envelope_to field

Fixes #42
Closes #123
```

### 3. **Scope Matters**

Use scope to clarify which component changed:

```bash
feat(parser): fix XML namespace handling
feat(cli): add --quiet flag
feat(csv): add timestamp column
```

### 4. **Keep First Line Under 50 Characters**

```
# This line is exactly 50 chars────────────────────
feat(scope): brief description of the change
```

### 5. **Separate Subject from Body**

```bash
# Good (blank line between subject and body)
feat(parser): add envelope_to extraction

This adds support for extracting the envelope_to
field from DMARC XML reports.

# Bad (no blank line)
feat(parser): add envelope_to extraction
This adds support for extracting the envelope_to field
```

---

## Workflow Example

```bash
# 1. Make changes
echo "new feature" >> mailops/dmarc_parser.py

# 2. Stage changes
git add mailops/dmarc_parser.py

# 3. Commit with proper format
git commit -m "feat(dmarc_parser): add envelope_to field extraction"

# 4. Later, when ready to release...
python scripts/generate_changelog.py --draft --version 2.6.0

# 5. Review the preview, then generate
python scripts/generate_changelog.py --version 2.6.0 --append

# 6. Commit and tag
git add CHANGELOG.md
git commit -m "docs: update changelog for v2.6.0"
git tag -a v2.6.0 -m "Release v2.6.0"
```

---

## Why This Matters

### For You
- **Automated changelog generation** → Less manual work
- **Clear commit history** → Easier to understand what changed
- **Professional standards** → Matches industry best practices

### For Users
- **Meaningful changelog** → Know what changed between versions
- **Easy to scan** → Organized by type (Added, Fixed, etc.)
- **Traceable** → Each changelog entry links to commit

---

## More Info

- Read full workflow: `docs/CHANGELOG_WORKFLOW.md`
- Conventional Commits spec: https://www.conventionalcommits.org/
- Semantic Versioning: https://semver.org/
