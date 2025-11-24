import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import gzip
import zipfile
import os
import csv
import sys

def parse_dmarc_xml(file_path):
    """
    Parses a DMARC aggregate report and returns a list of record dictionaries.
    """
    tree = None
    filename = os.path.basename(file_path)
    records_data = []
    
    # 1. Open the file based on extension
    try:
        if file_path.endswith('.gz'):
            with gzip.open(file_path, 'rb') as f:
                tree = ET.parse(f)
        elif file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as z:
                xml_files = [n for n in z.namelist() if n.lower().endswith('.xml')]
                if not xml_files:
                    return []
                with z.open(xml_files[0]) as f:
                    tree = ET.parse(f)
        else:
            tree = ET.parse(file_path)
            
        root = tree.getroot()
        
    except Exception as e:
        print(f"[!] Error processing '{filename}': {e}")
        return []

    # 2. Extract Metadata
    org_name = root.findtext('.//org_name') or "Unknown Org"
    
    date_range = root.find('.//date_range')
    if date_range is not None:
        begin_ts = int(date_range.findtext('begin', 0))
        end_ts = int(date_range.findtext('end', 0))
        begin_date = datetime.fromtimestamp(begin_ts).strftime('%Y-%m-%d %H:%M')
        end_date = datetime.fromtimestamp(end_ts).strftime('%Y-%m-%d %H:%M')
    else:
        begin_date = end_date = "Unknown"

    # 3. Extract Records
    records = root.findall('record')
    
    for record in records:
        row = record.find('row')
        source_ip = row.findtext('source_ip')
        count = row.findtext('count')
        
        disposition = row.find('.//policy_evaluated/disposition').text
        
        spf = record.find('.//auth_results/spf/result')
        spf_res = spf.text if spf is not None else "none"
        
        dkim = record.find('.//auth_results/dkim/result')
        dkim_res = dkim.text if dkim is not None else "none"

        # Create a flat dictionary for this row
        records_data.append({
            'org_name': org_name,
            'begin_date': begin_date,
            'end_date': end_date,
            'source_ip': source_ip,
            'count': count,
            'spf': spf_res,
            'dkim': dkim_res,
            'disposition': disposition,
            'file': filename
        })
        
    return records_data

def print_to_console(all_data):
    """Prints the data to console grouped by Organization/File."""
    if not all_data:
        print("\nNo records to display.")
        return

    # Group by file for readable output
    current_file = None
    
    for row in all_data:
        if row['file'] != current_file:
            current_file = row['file']
            print(f"\n--- Report for {row['org_name']} [{current_file}] ---")
            print(f"Period: {row['begin_date']} to {row['end_date']}")
            print("-" * 80)
            print(f"{'Source IP':<20} | {'Count':<5} | {'SPF':<6} | {'DKIM':<6} | {'Disposition'}")
            print("-" * 80)
        
        print(f"{row['source_ip']:<20} | {row['count']:<5} | {row['spf']:<6} | {row['dkim']:<6} | {row['disposition']}")

def save_to_csv(all_data, output_file):
    """Saves the data to a flat CSV file."""
    if not all_data:
        print("\nNo data found to save.")
        return

    headers = ['org_name', 'begin_date', 'end_date', 'source_ip', 'count', 'spf', 'dkim', 'disposition', 'file']
    
    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_data)
        print(f"\n✅ Successfully exported {len(all_data)} records to '{output_file}'")
    except Exception as e:
        print(f"\n[!] Error writing CSV: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse DMARC XML reports (XML, .gz, .zip).")
    parser.add_argument('path', help="Path to a single file or directory of reports")
    parser.add_argument('--csv', help="Output CSV file path (e.g., report.csv)", default=None)
    parser.add_argument('--alerts-only', action='store_true', help="Only show records where SPF or DKIM failed")
    
    args = parser.parse_args()
    
    target_path = args.path
    all_records = []

    # Gather files
    files_to_process = []
    if os.path.isfile(target_path):
        files_to_process.append(target_path)
    elif os.path.isdir(target_path):
        print(f"Scanning directory: {target_path} ...")
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.lower().endswith(('.xml', '.gz', '.zip')):
                    files_to_process.append(os.path.join(root, file))
    else:
        print(f"Error: '{target_path}' is not a valid file or directory.")
        return

    # Process files
    if not files_to_process:
        print("No DMARC files found.")
        return

    print(f"Found {len(files_to_process)} valid report files.")
    
    for file_path in files_to_process:
        print(f"Reading {os.path.basename(file_path)}...", end=" ", flush=True)
        new_records = parse_dmarc_xml(file_path)
        
        if new_records:
            print(f"Ok ({len(new_records)} records)")
            all_records.extend(new_records)
        else:
            print("Empty (No traffic data)")

    # Filter for alerts if requested
    if args.alerts_only:
        print("\n[!] Filtering for alerts (SPF != pass OR DKIM != pass)...")
        original_count = len(all_records)
        all_records = [r for r in all_records if r['spf'] != 'pass' or r['dkim'] != 'pass']
        print(f"Found {len(all_records)} alerts out of {original_count} total records.")

    # Output
    if args.csv:
        save_to_csv(all_records, args.csv)
    else:
        print_to_console(all_records)

if __name__ == "__main__":
    main()