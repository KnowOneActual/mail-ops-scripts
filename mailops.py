import argparse
import configparser
import sys
import os
import getpass

# Import your tool modules
import dmarc_parser
import spf_check
import blacklist_monitor
import dkim_gen
import imap_fetcher

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def cmd_fetch(args, config):
    """Handles the IMAP fetching workflow."""
    email_addr = args.email or config.get('imap', 'email', fallback=None)
    server = args.server or config.get('imap', 'server', fallback='imap.mail.me.com')
    
    if not email_addr:
        print("[!] Error: Email not configured in config.ini or --email argument.")
        return

    # Check for stored password, otherwise ask safely
    pwd = config.get('imap', 'password', fallback=None)
    if not pwd:
        print(f"Enter App Password for {email_addr} (hidden):")
        try:
            pwd = getpass.getpass("> ")
        except KeyboardInterrupt:
            return

    imap_fetcher.fetch_reports(email_addr, pwd, server)

def cmd_report(args, config):
    """Handles DMARC analysis."""
    target = args.path or config.get('general', 'download_dir', fallback='./dmarc_reports')
    print(f"[*] Analyzing reports in: {target}")

    all_records = []
    files = []
    
    # Locate files
    if os.path.isfile(target):
        files.append(target)
    elif os.path.isdir(target):
        for root, _, filenames in os.walk(target):
            for f in filenames:
                if f.lower().endswith(('.xml', '.gz', '.zip')):
                    files.append(os.path.join(root, f))
    
    if not files:
        print("[-] No DMARC files found.")
        return

    # Process files
    for f in files:
        records = dmarc_parser.parse_dmarc_xml(f)
        if records:
            all_records.extend(records)
            
    # Apply Alerts Filter
    if args.alerts:
        print("[!] Filtering for failures only...")
        all_records = [r for r in all_records if r['spf'] != 'pass' or r['dkim'] != 'pass']

    # Output
    if args.csv:
        dmarc_parser.save_to_csv(all_records, args.csv)
    else:
        dmarc_parser.print_to_console(all_records)

def cmd_check(args, config):
    """Runs a health check (SPF + Blacklist)."""
    domain = args.domain or config.get('monitor', 'domain', fallback=None)
    if not domain:
        print("[!] Error: Domain not set in config.ini or argument.")
        return
        
    print(f"\n=== HEALTH CHECK: {domain} ===")
    
    print("\n[1] Checking SPF Record...")
    record = spf_check.fetch_spf_record(domain)
    if record:
        spf_check.analyze_spf(record)
    
    print("\n[2] Checking Blacklist Status...")
    blacklist_monitor.run_check(domain)

def cmd_dkim(args, config):
    """Generates DKIM keys."""
    domain = args.domain or config.get('monitor', 'domain', fallback="example.com")
    dkim_gen.generate_and_print(args.selector, domain)

def main():
    parser = argparse.ArgumentParser(description="Mail Ops Utility Belt")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # 1. Fetch
    fetch_p = subparsers.add_parser('fetch', help='Download reports from email')
    fetch_p.add_argument('--email', help='Override configured email')

    # 2. Report
    report_p = subparsers.add_parser('report', help='Analyze DMARC data')
    report_p.add_argument('path', nargs='?', help='Path to reports (default: ./dmarc_reports)')
    report_p.add_argument('--csv', help='Export to CSV')
    report_p.add_argument('--alerts', action='store_true', help='Show failures only')

    # 3. Check (Health)
    check_p = subparsers.add_parser('check', help='Run SPF & Blacklist audit')
    check_p.add_argument('domain', nargs='?', help='Domain to audit')

    # 4. DKIM
    dkim_p = subparsers.add_parser('dkim', help='Generate DKIM keys')
    dkim_p.add_argument('selector', help='Selector name (e.g. mail, k1)')
    dkim_p.add_argument('--domain', help='Override domain')

    args = parser.parse_args()
    config = load_config()

    if args.command == 'fetch':
        cmd_fetch(args, config)
    elif args.command == 'report':
        cmd_report(args, config)
    elif args.command == 'check':
        cmd_check(args, config)
    elif args.command == 'dkim':
        cmd_dkim(args, config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()