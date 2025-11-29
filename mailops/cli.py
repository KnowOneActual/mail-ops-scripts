#!/usr/bin/env python3
"""MailOps CLI - Email Operations Toolkit"""

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mailops.dkim_gen import generate_keys
from mailops.dmarc_parser import parse_dmarc_xml
from mailops.imap_fetcher import fetch_reports
from mailops.spf_check import fetch_spf_record


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MailOps - Email Operations Toolkit ✅",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 FULL PRODUCTION WORKFLOW:
  1. mailops fetch --user you@gmail.com --pass app-password --days 7
  2. mailops report --alerts
  3. mailops spf yourdomain.com
  4. mailops dkim yourdomain.com
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # FETCH ⚡ REAL IMAP
    fetch_parser = subparsers.add_parser("fetch", help="Fetch DMARC reports from IMAP")
    fetch_parser.add_argument("--days", type=int, default=7, help="Days back")
    fetch_parser.add_argument("--user", required=True, help="IMAP username")
    fetch_parser.add_argument(
        "--password", required=True, help="IMAP password"
    )  # FIXED!
    fetch_parser.add_argument("--server", default="imap.gmail.com", help="IMAP server")

    # REPORT
    report_parser = subparsers.add_parser("report", help="Analyze DMARC reports")
    report_parser.add_argument(
        "--alerts", action="store_true", help="Show only failures"
    )
    report_parser.add_argument("--csv", help="Export to CSV")

    # DKIM
    dkim_parser = subparsers.add_parser("dkim", help="Generate DKIM keys")
    dkim_parser.add_argument("domain", help="Domain name")
    dkim_parser.add_argument("--selector", default="default", help="DKIM selector")

    # SPF
    spf_parser = subparsers.add_parser("spf", help="Check SPF records")
    spf_parser.add_argument("domain", help="Domain to check")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "fetch":
            print(f"📥 Fetching REAL DMARC reports...")
            print(f"   👤 {args.user} | 📧 {args.server} | 📅 {args.days} days")
            fetch_reports(
                args.user, args.password, args.server, days=args.days
            )  # FIXED!
            print("✅ Reports downloaded! Run 'mailops report'")

        elif args.command == "report":
            print("📊 Analyzing REAL DMARC reports...")
            xml_files = glob.glob("*.xml") + glob.glob("reports/*.xml")
            if xml_files:
                print(f"Found {len(xml_files)} XML files:")
                for xml_file in xml_files:
                    print(f"  📄 {xml_file}")
                    parse_dmarc_xml(xml_file)
            else:
                print("❌ No XML files found. Run 'mailops fetch' first!")

        elif args.command == "dkim":
            print(f"🔑 Generating DKIM keys for {args.domain}...")
            generate_keys(args.selector)
            print("✅ DKIM keys generated!")

        elif args.command == "spf":
            fetch_spf_record(args.domain)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
