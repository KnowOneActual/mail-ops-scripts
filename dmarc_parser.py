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
    Parses a DMARC aggregate report.
    Returns a list of record dictionaries. 
    If a report is a "Policy Check" (no traffic), it prints a summary immediately but returns empty list.
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
    
    # --- NEW: Handle "Nil Reports" (Policy Checks) ---
    if not records:
        # Check if they at least saw our policy
        policy = root.find('.//policy_published')
        if policy is not None:
            domain = policy.findtext('domain')
            p_mode = policy.findtext('p')
            pct = policy.findtext('pct')
            print(f"\n[i] Policy Check Only: {org_name}")
            print(f"    - They checked: {domain}")
            print(f"    - They saw: p={p_mode} (Applied to {pct}%)")
            print(f"    - Traffic: 0 emails sent.")
            return [] # Still return empty list so it doesn't mess up CSV math
    # -------------------------------------------------

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
        # We don't print "No records" here anymore because the 
        # parse function handles the "Policy Check" notification directly.
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
        print("\nNo traffic data found to save to CSV.")
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

def save_to_html(all_data, output_file):
    """Generates a visual HTML dashboard report."""
    if not all_data:
        print("\nNo traffic data to generate HTML report.")
        return

    # Calculate Summary Stats
    total = len(all_data)
    fails = sum(1 for r in all_data if r['spf'] != 'pass' or r['dkim'] != 'pass')
    pass_count = total - fails
    pass_percent = (pass_count / total) * 100 if total > 0 else 0

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DMARC Analysis Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f4f4f9; color: #333; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ margin-top: 0; color: #2c3e50; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 20px; padding: 15px; background: #eef2f7; border-radius: 6px; border-left: 5px solid #3498db; }}
        .stat {{ font-size: 1.1em; }}
        .stat strong {{ font-weight: 700; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.9em; }}
        th, td {{ padding: 12px 15px; border-bottom: 1px solid #ddd; text-align: left; }}
        th {{ background-color: #34495e; color: white; text-transform: uppercase; font-size: 0.85em; letter-spacing: 0.05em; }}
        tr:hover {{ background-color: #f1f1f1; }}
        
        /* Status Colors */
        tr.fail {{ background-color: #fff0f0; }}
        tr.pass {{ background-color: #ffffff; }}
        
        .badge {{ padding: 4px 8px; border-radius: 4px; color: white; font-weight: bold; font-size: 0.85em; text-transform: uppercase; display: inline-block; width: 60px; text-align: center; }}
        .badge-pass {{ background: #27ae60; }}
        .badge-fail {{ background: #e74c3c; }}
        .badge-softfail, .badge-neutral {{ background: #f39c12; }}
        .badge-none {{ background: #95a5a6; }}
        
        .footer {{ margin-top: 30px; font-size: 0.8em; color: #7f8c8d; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 DMARC Analysis Report</h1>
        <div class="summary">
            <div class="stat">Total Records: <strong>{total}</strong></div>
            <div class="stat">Passing: <strong style="color: #27ae60;">{pass_count}</strong> ({pass_percent:.1f}%)</div>
            <div class="stat">Failing: <strong style="color: #e74c3c;">{fails}</strong></div>
            <div class="stat">Report Date: <strong>{datetime.now().strftime('%Y-%m-%d')}</strong></div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Organization</th>
                    <th>Source IP</th>
                    <th>Date Range</th>
                    <th>SPF Auth</th>
                    <th>DKIM Auth</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
"""

    for row in all_data:
        spf = row['spf'].lower()
        dkim = row['dkim'].lower()
        
        # Determine row styling
        is_fail = spf != 'pass' or dkim != 'pass'
        row_class = "fail" if is_fail else "pass"
        
        # Helper for badge classes
        def get_badge(status):
            if status == 'pass': return 'badge-pass'
            if status in ['fail', 'permerror']: return 'badge-fail'
            if status in ['softfail', 'neutral']: return 'badge-softfail'
            return 'badge-none'
            
        html += f"""
                <tr class="{row_class}">
                    <td><strong>{row['org_name']}</strong><br><span style="color:#7f8c8d; font-size:0.85em">{row['file']}</span></td>
                    <td>{row['source_ip']}</td>
                    <td>{row['begin_date']}<br>to {row['end_date']}</td>
                    <td><span class="badge {get_badge(spf)}">{spf}</span></td>
                    <td><span class="badge {get_badge(dkim)}">{dkim}</span></td>
                    <td>{row['disposition']}</td>
                </tr>
        """

    html += """
            </tbody>
        </table>
        <div class="footer">Generated by Mail Ops Scripts v2.1.0</div>
    </div>
</body>
</html>
"""

    try:
        with open(output_file, 'w') as f:
            f.write(html)
        print(f"\n✅ HTML Report saved to: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"\n[!] Error writing HTML: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse DMARC XML reports.")
    parser.add_argument('path', help="Path to reports")
    parser.add_argument('--csv', help="Output CSV file")
    parser.add_argument('--html', help="Output HTML file")
    parser.add_argument('--alerts-only', action='store_true', help="Only show failures")
    
    args = parser.parse_args()
    
    all_records = []
    
    # Simple file detection for standalone run
    if os.path.isfile(args.path):
        all_records = parse_dmarc_xml(args.path)
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for f in files:
                if f.lower().endswith(('.xml', '.gz', '.zip')):
                    recs = parse_dmarc_xml(os.path.join(root, f))
                    if recs: all_records.extend(recs)

    if args.alerts_only:
        all_records = [r for r in all_records if r['spf'] != 'pass' or r['dkim'] != 'pass']

    if args.html:
        save_to_html(all_records, args.html)
    elif args.csv:
        save_to_csv(all_records, args.csv)
    else:
        print_to_console(all_records)

if __name__ == "__main__":
    main()