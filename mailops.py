import argparse
import configparser
import sys
import os
import getpass

# Import your tool modules
# Ensure these files are in the same directory or properly installed
import dmarc_parser
import spf_check
import blacklist_monitor
import dkim_gen
import imap_fetcher

# --- Styling for Help Menu ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

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
    # Default to current directory if not specified, or config
    target = args.path or config.get('general', 'download_dir', fallback='./dmarc_reports')
    
    if not os.path.exists(target):
         print(f"{Colors.YELLOW}[!] Path not found: {target}{Colors.RESET}")
         return

    print(f"[*] Analyzing reports in: {target}")

    all_records = []
    files = []
    
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

    for f in files:
        # Use the updated dmarc_parser which returns status_msg/color
        records = dmarc_parser.parse_dmarc_xml(f)
        if records:
            all_records.extend(records)
            
    if args.alerts:
        print(f"{Colors.YELLOW}[!] Filtering for failures/investigations only...{Colors.RESET}")
        all_records = [r for r in all_records if r.get('status_msg', 'OK') != 'OK']

    # Output Routing
    if args.html:
        # dmarc_parser.save_to_html(all_records, args.html) 
        pass 
    elif args.csv:
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
    # --- Custom Help Text with Examples ---
    epilog_text = f"""
{Colors.HEADER}COMMON USAGE EXAMPLES:{Colors.RESET}
  {Colors.BOLD}1. Analyze a specific folder of reports:{Colors.RESET}
     python mailops.py report /Users/userx/Desktop/DMARC_Log

  {Colors.BOLD}2. Analyze just one file:{Colors.RESET}
     python mailops.py report /Users/userx/Desktop/report.xml

  {Colors.BOLD}3. Show ONLY failures (Investigate/Blocked):{Colors.RESET}
     python mailops.py report /Users/userx/Desktop/DMARC_Log --alerts

  {Colors.BOLD}4. Check your Domain Health (SPF + Blacklists):{Colors.RESET}
     python mailops.py check beaubremer.com

  {Colors.BOLD}5. Fetch new reports from email:{Colors.RESET}
     python mailops.py fetch

{Colors.HEADER}LEGEND (for Report):{Colors.RESET}
  {Colors.GREEN}OK{Colors.RESET}           : Authenticated and safe.
  {Colors.YELLOW}BLOCKED{Colors.RESET}      : Spoofing attempt blocked by policy.
  {Colors.RED}INVESTIGATE{Colors.RESET}  : Authentication failed, email likely delivered.
"""

    parser = argparse.ArgumentParser(
        description="Mail Ops Utility Belt - All-in-one DMARC & Deliverability Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=epilog_text
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # 1. Fetch
    fetch_p = subparsers.add_parser('fetch', help='Download reports from email')
    fetch_p.add_argument('--email', help='Override configured email')
    fetch_p.add_argument('--server', help='Override IMAP server')

    # 2. Report
    report_p = subparsers.add_parser('report', help='Analyze DMARC data')
    report_p.add_argument('path', nargs='?', help='Path to reports (default: ./dmarc_reports)')
    report_p.add_argument('--csv', help='Export to CSV')
    report_p.add_argument('--html', help='Export to HTML Dashboard')
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
        # Print help if no command is provided
        parser.print_help()

if __name__ == "__main__":
    main()