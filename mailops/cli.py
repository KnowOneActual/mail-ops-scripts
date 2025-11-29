#!/usr/bin/env python3
"""MailOps CLI - Email Operations Toolkit"""

import argparse
import sys
import os
import glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mailops.dkim_gen import generate_keys
from mailops.spf_check import fetch_spf_record
from mailops.dmarc_parser import parse_dmarc_xml

def main() -> None:
    parser = argparse.ArgumentParser(
        description="MailOps - Email Operations Toolkit ✅",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mailops dkim example.com        # Generate REAL DKIM keys ⚡
  mailops spf google.com          # Check REAL SPF records ⚡
  mailops report                  # Analyze REAL DMARC reports ⚡
  mailops fetch --days 7          # Fetch from IMAP ⚡
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # DKIM
    dkim_parser = subparsers.add_parser('dkim', help='Generate DKIM keys')
    dkim_parser.add_argument('domain', help='Domain name')
    dkim_parser.add_argument('--selector', default='default', help='DKIM selector')
    
    # SPF
    spf_parser = subparsers.add_parser('spf', help='Check SPF records')
    spf_parser.add_argument('domain', help='Domain to check')
    
    # REPORT ⚡ REAL DMARC
    report_parser = subparsers.add_parser('report', help='Analyze DMARC reports')
    report_parser.add_argument('--alerts', action='store_true', help='Show only failures')
    report_parser.add_argument('--csv', help='Export to CSV')
    
    # FETCH
    fetch_parser = subparsers.add_parser('fetch', help='Fetch DMARC reports')
    fetch_parser.add_argument('--days', type=int, default=7, help='Days back')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'dkim':
            print(f"🔑 Generating DKIM keys for {args.domain}...")
            generate_keys(args.selector)
            print("✅ DKIM keys generated!")
            
        elif args.command == 'spf':
            fetch_spf_record(args.domain)
            
        elif args.command == 'report':
            print("📊 Analyzing DMARC reports...")
            xml_files = glob.glob("*.xml") + glob.glob("reports/*.xml")
            if xml_files:
                for xml_file in xml_files:
                    print(f"Parsing {xml_file}...")
                    parse_dmarc_xml(xml_file)
            else:
                print("No XML files found. Run 'mailops fetch' first.")
                
        elif args.command == 'fetch':
            print("📥 Fetching DMARC reports from IMAP... (TODO)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
