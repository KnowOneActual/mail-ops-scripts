<div align="center">
  <img src="assets/img/mail-ops-scripts.webp" alt="mail ops scripts project logo" width="200">


# Mail Ops Scripts

# **Under Development**
</div>

[![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml)


A collection of lightweight, dependency-free Python utilities for email server administration, security analysis, and reporting.

## Tools Included

### 1. DMARC XML Parser (`dmarc_parser.py`)
A robust analyzer for DMARC aggregate reports. It handles single XML files, compressed archives (`.gz`, `.zip`), or entire directories of mixed reports.

**Key Features:**
* **Bulk Processing:** Scans folders recursively for reports.
* **Auto-Decompression:** Reads `.gz` and `.zip` files on the fly.
* **CSV Export:** Converts complex XML data into flat CSVs for Excel/Sheets.
* **Alert Mode:** Filters output to show *only* authentication failures (SPF/DKIM).

### 2. SPF Syntax Checker (`spf_check.py`)
A security tool to validate DNS records without needing external libraries (uses Google's DNS-over-HTTPS API).

**Checks Performed:**
* **Syntax:** Validates `v=spf1` structure.
* **RFC Limits:** Warns if DNS lookups exceed the limit of 10.
* **Security:** Flags dangerous policies like `+all` or `?all`.

### 3. DKIM Key Generator (`dkim_gen.py`)
Generates secure 2048-bit RSA keys for email signing. Uses your system's `openssl` to avoid Python dependencies.

**Output:**
* Saves `selector.private` (The key you upload to your mail server).
* Prints the exact `TXT` record to add to your DNS.

### 4. Blacklist Monitor (`blacklist_monitor.py`)
Checks if your mail server's IP or Domain is listed on major Real-time Blackhole Lists (RBLs) like Spamhaus and Spamcop.

**Key Features:**
* **Smart Resolution:** Accepts either an IP (`1.2.3.4`) or a Domain (`google.com`).
* **Privacy:** Uses DNS-over-HTTPS to query RBLs securely.

### 5. IMAP Report Fetcher (`imap_fetcher.py`)
Connects to your email server, finds DMARC report emails, and downloads the attachments into a `dmarc_reports/YYYY-MM-DD/` folder structure.

---

## Prerequisites

* Python 3.x
* **No `pip install` required.** All scripts use standard libraries.
* **OpenSSL** (Required only for `dkim_gen.py`).

---

## Usage

### DMARC Parser
```bash
# Basic Summary
python dmarc_parser.py ./downloads

# Export to CSV
python dmarc_parser.py ./downloads --csv report.csv

# Show only failures
python dmarc_parser.py ./downloads --alerts-only
````

### SPF Checker

```bash
python spf_check.py google.com
```

### DKIM Generator

```bash
# Syntax: python dkim_gen.py <selector> --domain <domain>
python dkim_gen.py mail --domain example.com
```

### Blacklist Monitor

```bash
# Check by IP
python blacklist_monitor.py 1.2.3.4

# Check by Domain (Auto-resolves to IP)
python blacklist_monitor.py google.com
```

### IMAP Fetcher

```bash
# Default (iCloud):
python imap_fetcher.py --email dmarc@beaubremer.com

# For Gmail:
python imap_fetcher.py --email you@gmail.com --server imap.gmail.com
```

-----

### 🔧 IMAP Fetcher: Common Providers & Setup

Most modern email providers (iCloud, Gmail) require an **App-Specific Password** to use this script. You cannot use your regular login password if 2FA is enabled.

#### 🍏 Apple iCloud (Default)

  * **Server:** `imap.mail.me.com` (Default in script)
  * **Username:** Must be your primary Apple ID email (e.g., `user@icloud.com`), even if checking a custom domain alias.
  * **Password:** Requires an App-Specific Password.
      * Go to [appleid.apple.com](https://www.google.com/search?q=https://appleid.apple.com) \> Sign-In and Security \> App-Specific Passwords.



```bash
python imap_fetcher.py --email your_primary@icloud.com
```

#### 📮 Gmail / Google Workspace

  * **Server:** `imap.gmail.com`
  * **Username:** Your full Gmail address.
  * **Password:** Requires an App Password.
      * Go to [myaccount.google.com](https://myaccount.google.com) \> Security \> 2-Step Verification \> App passwords.
      * *Note: If you don't see "App passwords," enable 2-Step Verification first.*



```bash
python imap_fetcher.py --email you@gmail.com --server imap.gmail.com
```

#### 🟦 Outlook / Office 365

  * **Server:** `outlook.office365.com`
  * **Note:** Many corporate Office 365 accounts **disable** Basic Auth (IMAP) by default. If this fails, you may need to ask your admin to enable "Authenticated SMTP" or use a different fetch method.



```bash
python imap_fetcher.py --email you@outlook.com --server outlook.office365.com
```

#### ❌ Troubleshooting Login Failures

1.  **`[AUTHENTICATIONFAILED]`**: You are likely using your normal password instead of an App Password, or you have 2FA enabled but didn't generate a token.
2.  **`Connection Refused`**: Check if you are behind a corporate firewall blocking port 993.
3.  **`No DMARC reports found`**: The script searches for subjects containing "Report Domain" or "DMARC Aggregate". Ensure your reports aren't going to Spam.

-----

## Roadmap

  * [x] **Phase 1: Reporting** (DMARC Parser complete)
  * [x] **Phase 2: Validation** (SPF Checker complete)
  * [x] **Phase 3: Operations** (DKIM Key Gen, RBL Monitor complete)
  * [x] **Phase 4: Automation** (IMAP Fetcher complete)


## License

MIT [License](./LICENSE) | Copyright (c) 2025 Beau Bremer
