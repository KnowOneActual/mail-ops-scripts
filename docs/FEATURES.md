# Mail-Ops Features

## 📊 Report Command

The `mailops report` command analyzes DMARC XML reports and provides comprehensive email authentication analysis.

### Output Format

The report displays:
- **Source IP**: IP address sending the email
- **Envelope To**: DMARC recipient domain (from `<envelope_to>` field)
- **Hostname**: Reverse DNS lookup of source IP
- **Cnt**: Number of messages from this source
- **SPF**: SPF authentication result (pass/fail/none/softfail)
- **DKIM**: DKIM authentication result (pass/fail/none)
- **Analysis**: Status indicator
  - ✅ **OK**: Authentication passed (SPF or DKIM)
  - ⚠️ **BLOCKED (Spoofing)**: Failed with quarantine/reject policy
  - 🔴 **INVESTIGATE**: Failed authentication

### Example Output

```bash
$ mailops report
📊 Analyzing REAL DMARC reports...
Found 11 XML files:

--- Report: Enterprise Outlook (2025-12-23) ---
──────────────────────────────────────────────────────────────────────────────────────────────────────
Source IP            | Envelope To          | Hostname                       | Cnt | SPF  | DKIM | Analysis
──────────────────────────────────────────────────────────────────────────────────────────────────────
57.103.73.211        | outsource.net        | p-west3-cluster1-host8-snip..  | 1   | pass | pass | OK
117.214.28.147       | beaubremer.com       | Unknown                        | 1   | fail | none | INVESTIGATE
```

### Command Options

#### View All Records
```bash
mailops report
```

#### Filter by Security Alerts Only
```bash
mailops report --alerts
```
Shows only records with `BLOCKED (Spoofing)` or `INVESTIGATE` status.

#### Export to CSV
```bash
mailops report --csv results.csv
```

CSV fields:
- org_name
- date
- source_ip
- hostname
- **envelope_to** ← New field!
- count
- spf
- dkim
- disposition
- status_msg
- file

#### Export Alerts to CSV
```bash
mailops report --alerts --csv alerts.csv
```

## 📥 Fetch Command

Automatically download DMARC reports from your email inbox via IMAP.

```bash
mailops fetch --user you@gmail.com --password app-password --days 7
```

Supports:
- Gmail (default: imap.gmail.com)
- Custom IMAP servers via `--server` flag
- Configurable lookback period with `--days`

## 🔐 DKIM Command

Generate DKIM signing keys for your domain.

```bash
mailops dkim yourdomain.com --selector default
```

Generates:
- Private key (for mail server configuration)
- Public key (for DNS TXT record)

## 🔍 SPF Command

Lookup and verify SPF records.

```bash
mailops spf yourdomain.com
```

## 📁 Supported File Formats

The report parser automatically handles:
- `.xml` - Raw DMARC XML files
- `.xml.gz` - Gzip-compressed DMARC files
- `.zip` - ZIP archives containing DMARC XML files

Files can be in the current directory or in a `reports/` subdirectory.
