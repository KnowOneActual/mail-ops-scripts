import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import gzip
import zipfile
import os
import csv
import socket
import sys

# --- Configuration & Helpers ---

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

IP_CACHE = {}

def resolve_ip(ip_address):
    """Resolves IP to Hostname with caching."""
    if ip_address in IP_CACHE:
        return IP_CACHE[ip_address]
    
    try:
        socket.setdefaulttimeout(2)
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        IP_CACHE[ip_address] = hostname
        return hostname
    except Exception:
        result = "Unknown"
        IP_CACHE[ip_address] = result
        return result

def analyze_record(spf, dkim, disposition):
    """
    Determines the status and color based on DMARC results.
    Returns: (Action_String, Color_Code)
    """
    if spf == 'pass' or dkim == 'pass':
        return "OK", Colors.GREEN
    
    if disposition in ['quarantine', 'reject']:
        return "BLOCKED (Spoofing)", Colors.YELLOW
    
    return "INVESTIGATE", Colors.RED

# --- Core Logic ---

def parse_dmarc_xml(file_path):
    tree = None
    filename = os.path.basename(file_path)
    records_data = []
    
    try:
        if file_path.endswith('.gz'):
            with gzip.open(file_path, 'rb') as f:
                tree = ET.parse(f)
        elif file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as z:
                xml_files = [n for n in z.namelist() if n.lower().endswith('.xml')]
                if not xml_files: return []
                with z.open(xml_files[0]) as f:
                    tree = ET.parse(f)
        else:
            tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"{Colors.RED}[!] Error processing '{filename}': {e}{Colors.RESET}")
        return []

    org_name = root.findtext('.//org_name') or "Unknown Org"
    
    date_range = root.find('.//date_range')
    if date_range is not None:
        begin_ts = int(date_range.findtext('begin', 0))
        end_ts = int(date_range.findtext('end', 0))
        begin_date = datetime.fromtimestamp(begin_ts).strftime('%Y-%m-%d')
        end_date = datetime.fromtimestamp(end_ts).strftime('%Y-%m-%d')
    else:
        begin_date = end_date = "Unknown"

    records = root.findall('record')
    if not records:
        return [] 

    for record in records:
        row = record.find('row')
        source_ip = row.findtext('source_ip')
        count = row.findtext('count')
        disposition = row.find('.//policy_evaluated/disposition').text
        
        spf = record.find('.//auth_results/spf/result')
        spf_res = spf.text if spf is not None else "none"
        
        dkim = record.find('.//auth_results/dkim/result')
        dkim_res = dkim.text if dkim is not None else "none"

        hostname = resolve_ip(source_ip)
        status_msg, status_color = analyze_record(spf_res, dkim_res, disposition)

        records_data.append({
            'org_name': org_name,
            'date': begin_date,
            'source_ip': source_ip,
            'hostname': hostname,
            'count': count,
            'spf': spf_res,
            'dkim': dkim_res,
            'disposition': disposition,
            'status_msg': status_msg,
            'status_color': status_color,
            'file': filename
        })
        
    return records_data

def print_to_console(all_data):
    if not all_data:
        print("No records found.")
        return

    current_file = None
    header_fmt = "{:<20} | {:<30} | {:<5} | {:<6} | {:<6} | {:<15}"
    row_fmt    = "{:<20} | {:<30} | {:<5} | {:<6} | {:<6} | {:<15}"

    for row in all_data:
        if row['file'] != current_file:
            current_file = row['file']
            print(f"\n{Colors.BOLD}--- Report: {row['org_name']} ({row['date']}) ---{Colors.RESET}")
            print("-" * 95)
            print(Colors.HEADER + header_fmt.format("Source IP", "Hostname", "Cnt", "SPF", "DKIM", "Analysis") + Colors.RESET)
            print("-" * 95)
        
        host_display = (row['hostname'][:27] + '..') if len(row['hostname']) > 29 else row['hostname']
        
        line = row_fmt.format(
            row['source_ip'], host_display, row['count'], row['spf'], row['dkim'], row['status_msg']
        )
        print(row['status_color'] + line + Colors.RESET)

def save_to_csv(all_data, output_file):
    if not all_data: return
    
    clean_data = [{k: v for k, v in r.items() if k != 'status_color'} for r in all_data]
    headers = ['org_name', 'date', 'source_ip', 'hostname', 'count', 'spf', 'dkim', 'disposition', 'status_msg', 'file']
    
    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(clean_data)
        print(f"\n{Colors.GREEN}✅ Exported to {output_file}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] CSV Error: {e}{Colors.RESET}")

def main():
    # We define the legend text here with the color codes embedded
    epilog_text = f"""
{Colors.BOLD}LEGEND:{Colors.RESET}
  {Colors.GREEN}OK{Colors.RESET}           : Email is authenticated and safe.
  {Colors.YELLOW}BLOCKED{Colors.RESET}      : Spoofing attempt caught by your policy (Quarantine/Reject).
  {Colors.RED}INVESTIGATE{Colors.RESET}  : Authentication failed, but email may have been delivered.
"""

    parser = argparse.ArgumentParser(
        description="Parse DMARC XML reports and analyze sender reputation.",
        formatter_class=argparse.RawTextHelpFormatter, # This keeps the newlines in the epilog
        epilog=epilog_text
    )
    
    parser.add_argument('path', help="Path to reports (file or folder)")
    parser.add_argument('--csv', help="Output CSV file path")
    parser.add_argument('--alerts-only', action='store_true', help="Only show failures/investigations")
    
    args = parser.parse_args()
    
    all_records = []
    
    files_to_process = []
    if os.path.isfile(args.path):
        files_to_process.append(args.path)
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for f in files:
                if f.lower().endswith(('.xml', '.gz', '.zip')):
                    files_to_process.append(os.path.join(root, f))
    
    if not files_to_process:
        print(f"{Colors.RED}[!] No DMARC files found in '{args.path}'{Colors.RESET}")
        return

    print(f"{Colors.BLUE}[*] Analyzing {len(files_to_process)} files...{Colors.RESET}")

    for f in files_to_process:
        recs = parse_dmarc_xml(f)
        if recs: all_records.extend(recs)

    if args.alerts_only:
        all_records = [r for r in all_records if r['status_msg'] != "OK"]

    if args.csv:
        save_to_csv(all_records, args.csv)
    else:
        print_to_console(all_records)

if __name__ == "__main__":
    main()