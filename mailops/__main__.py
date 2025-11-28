import argparse
import configparser
import getpass
import os
import sys

# Import your tool modules
import blacklist_monitor
import dkim_gen
import dmarc_parser
import imap_fetcher
import spf_check
import ui

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def cmd_fetch(args, config):
    """Handles the IMAP fetching workflow."""
    email_addr = args.email or config.get("imap", "email", fallback=None)
    server = args.server or config.get("imap", "server", fallback="imap.mail.me.com")

    if not email_addr:
        ui.print_error("Email not configured in config.ini or --email argument.")
        return

    # PRIORITY 1: Environment Variable (Secure & Automation friendly)
    pwd = os.environ.get("MAILOPS_PASSWORD")

    # PRIORITY 2: Config File (Convenient but risky if committed)
    if not pwd:
        pwd = config.get("imap", "password", fallback=None)

    # PRIORITY 3: Interactive Prompt (Safest for local manual use)
    if not pwd:
        print(f"Enter App Password for {email_addr} (hidden):")
        try:
            pwd = getpass.getpass("> ")
        except KeyboardInterrupt:
            return

    imap_fetcher.fetch_reports(email_addr, pwd, server)


def cmd_report(args, config):
    """Handles DMARC analysis."""
    target = args.path or config.get("general", "download_dir", fallback="./dmarc_reports")

    if not os.path.exists(target):
        ui.print_warning(f"Path not found: {target}")
        return

    ui.print_info(f"Analyzing reports in: {target}")

    all_records = []
    files = []

    if os.path.isfile(target):
        files.append(target)
    elif os.path.isdir(target):
        for root, _, filenames in os.walk(target):
            for f in filenames:
                if f.lower().endswith((".xml", ".gz", ".zip")):
                    files.append(os.path.join(root, f))

    if not files:
        ui.print_warning("No DMARC files found.")
        return

    for f in files:
        records = dmarc_parser.parse_dmarc_xml(f)
        if records:
            all_records.extend(records)

    if args.alerts:
        ui.print_warning("Filtering for failures/investigations only...")
        all_records = [r for r in all_records if r.get("status_msg", "OK") != "OK"]

    # Output Routing
    if args.html:
        pass
    elif args.csv:
        dmarc_parser.save_to_csv(all_records, args.csv)
    else:
        dmarc_parser.print_to_console(all_records)


def cmd_check(args, config):
    """Runs a health check (SPF + Blacklist)."""
    domain = args.domain or config.get("monitor", "domain", fallback=None)
    if not domain:
        ui.print_error("Domain not set in config.ini or argument.")
        return

    ui.print_header(f"HEALTH CHECK: {domain}")

    ui.print_info("Checking SPF Record...")
    record = spf_check.fetch_spf_record(domain)
    if record:
        spf_check.analyze_spf(record)

    print("")  # Spacer
    ui.print_info("Checking Blacklist Status...")
    blacklist_monitor.run_check(domain)


def cmd_dkim(args, config):
    """Generates DKIM keys."""
    domain = args.domain or config.get("monitor", "domain", fallback="example.com")
    dkim_gen.generate_and_print(args.selector, domain)


def main():
    # --- Custom Help Text with Examples ---
    epilog_text = f"""
{ui.Colors.HEADER}COMMON USAGE EXAMPLES:{ui.Colors.RESET}
  {ui.Colors.BOLD}1. Analyze a specific folder of reports:{ui.Colors.RESET}
     python mailops.py report /Users/userx/Desktop/DMARC_Log

  {ui.Colors.BOLD}2. Analyze just one file:{ui.Colors.RESET}
     python mailops.py report /Users/userx/Desktop/report.xml

  {ui.Colors.BOLD}3. Show ONLY failures (Investigate/Blocked):{ui.Colors.RESET}
     python mailops.py report --alerts

  {ui.Colors.BOLD}4. Check your Domain Health (SPF + Blacklists):{ui.Colors.RESET}
     python mailops.py check beaubremer.com

  {ui.Colors.BOLD}5. Fetch new reports from email:{ui.Colors.RESET}
     python mailops.py fetch

{ui.Colors.HEADER}LEGEND (for Report):{ui.Colors.RESET}
  {ui.Colors.GREEN}OK{ui.Colors.RESET}           : Authenticated and safe.
  {ui.Colors.YELLOW}BLOCKED{ui.Colors.RESET}      : Spoofing attempt blocked by policy.
  {ui.Colors.RED}INVESTIGATE{ui.Colors.RESET}  : Authentication failed, email likely delivered.
"""

    parser = argparse.ArgumentParser(
        description="Mail Ops Utility Belt - All-in-one DMARC & Deliverability Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=epilog_text,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # 1. Fetch
    fetch_p = subparsers.add_parser("fetch", help="Download reports from email")
    fetch_p.add_argument("--email", help="Override configured email")
    fetch_p.add_argument("--server", help="Override IMAP server")

    # 2. Report
    report_p = subparsers.add_parser("report", help="Analyze DMARC data")
    report_p.add_argument("path", nargs="?", help="Path to reports (default: ./dmarc_reports)")
    report_p.add_argument("--csv", help="Export to CSV")
    report_p.add_argument("--html", help="Export to HTML Dashboard")
    report_p.add_argument("--alerts", action="store_true", help="Show failures only")

    # 3. Check (Health)
    check_p = subparsers.add_parser("check", help="Run SPF & Blacklist audit")
    check_p.add_argument("domain", nargs="?", help="Domain to audit")

    # 4. DKIM
    dkim_p = subparsers.add_parser("dkim", help="Generate DKIM keys")
    dkim_p.add_argument("selector", help="Selector name (e.g. mail, k1)")
    dkim_p.add_argument("--domain", help="Override domain")

    args = parser.parse_args()
    config = load_config()

    if args.command == "fetch":
        cmd_fetch(args, config)
    elif args.command == "report":
        cmd_report(args, config)
    elif args.command == "check":
        cmd_check(args, config)
    elif args.command == "dkim":
        cmd_dkim(args, config)
    else:
        # Print help if no command is provided
        parser.print_help()


if __name__ == "__main__":
    main()
