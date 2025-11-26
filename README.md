<div align="center">
  <img src="assets/img/mail-ops-scripts.webp" alt="mail ops scripts project logo" width="200">



# Mail Ops Scripts

# **Still under development, please excuse the mess**

[![CI](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml/badge.svg)](https://github.com/KnowOneActual/mail-ops-scripts/actions/workflows/ci.yml)
</div>


A unified operational toolkit for email server administration, security analysis, and reporting.

**Version:** 2.2.0

## Features

* **🛡️ Health Checks:** Instant audit of SPF records and RBL Blacklist status.
* **🧠 Smart Analysis:** Automatic Reverse DNS (PTR) lookups to identify the true sender.
* **📊 DMARC Analysis:** Automated parsing of XML reports with color-coded console output.
* **📥 Auto-Fetch:** Secure IMAP integration to download DMARC reports automatically.
* **🔑 DKIM Generator:** Secure local generation of RSA keys and DNS records.
* **🔒 Secure Config:** Support for Environment Variables to keep secrets safe.

## Setup

### 1. Installation
No complex dependencies required. This project runs on standard Python 3.

```bash
git clone https://github.com/KnowOneActual/mail-ops-scripts.git
cd mail-ops-scripts
````

### 2\. Configuration

You can configure the tool using either a file or environment variables.

**Option A: Config File (Local Use)**
Edit `config.ini` to set your preferences:

```ini
[imap]
email = user@icloud.com
server = imap.mail.me.com
# password = (Leave blank to be prompted securely)
```

**Option B: Environment Variables (CI/CD & Secure Use)**
Instead of storing credentials in a file, export them in your shell:

```bash
export MAILOPS_PASSWORD="your-app-specific-password"
```

-----

## Usage

### 1. Health Check

Audits your SPF record syntax and checks your IP against major blacklists.

```bash
python mailops.py check
# or check a specific domain:
python mailops.py check google.com
```

### 2. Fetch Reports

Connects to your email, downloads new DMARC attachments, and saves them locally.

```bash
python mailops.py fetch
```

### 3. Analyze Reports

Parses all downloaded reports and summarizes traffic.

```bash
# View color-coded summary in console
python mailops.py report

# Show only failures (Attacks/Errors)
python mailops.py report --alerts

# Export to CSV
python mailops.py report --csv weekly_summary.csv
```

### 4. Generate DKIM Keys

Creates a 2048-bit private key and prints the DNS TXT record.

```bash
python mailops.py dkim mail --domain example.com
```

## Requirements

  * Python 3.8+
  * OpenSSL (for DKIM generation)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on code style and pull requests.

## License

MIT License. See [LICENSE](LICENSE)