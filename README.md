<div align="center">
  <img src="assets/img/mail-ops-scripts.webp" alt="mail ops scripts project logo" width="200">
</div>


# Mail Ops Scripts

# **Under Devolment**

[![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml)



A unified operational toolkit for email server administration, security analysis, and reporting.

**Version:** 2.0.0

## Features

* **🛡️ Health Checks:** Instant audit of SPF records and RBL Blacklist status.
* **📊 DMARC Analysis:** Automated parsing of XML reports (with bulk support, CSV export, and alert filtering).
* **📥 Auto-Fetch:** IMAP integration to download DMARC reports from iCloud/Gmail automatically.
* **🔑 DKIM Generator:** Secure local generation of RSA keys and DNS records.

## Setup

1.  **Configure:**
    Edit `config.ini` to set your email, server, and default domain.

2.  **Run:**
    Use the unified CLI for all tasks.

## Usage

### 1. Health Check
Audits your SPF record syntax and checks your IP against major blacklists.
```bash
python mailops.py check
# or override config:
python mailops.py check otherdomain.com
````

### 2\. Fetch Reports

Connects to your email (via `config.ini`), downloads new DMARC attachments, and saves them locally.

```bash
python mailops.py fetch
```

### 3\. Analyze Reports

Parses all downloaded reports and summarizes traffic.

```bash
# View summary in console
python mailops.py report

# Show only failures (Attacks/Errors)
python mailops.py report --alerts

# Export to CSV
python mailops.py report --csv weekly_summary.csv
```

### 4\. Generate DKIM Keys

Creates a 2048-bit private key and prints the DNS TXT record.

```bash
python mailops.py dkim mail --domain example.com
```

-----

## Configuration (`config.ini`)

```ini
[general]
download_dir = ./dmarc_reports

[imap]
email = user@icloud.com
server = imap.mail.me.com
# password = (Optional: Leave blank to be prompted securely)

[monitor]
domain = yourdomain.com
```

## Requirements

  * Python 3.x
  * OpenSSL (for DKIM generation)
  * No `pip install` required (Standard Libs only).

----

## License

MIT License. See [LICENSE](LICENSE) 
