import sys
import json
import urllib.request
import urllib.parse
import argparse
import re

def fetch_spf_record(domain):
    """
    Fetches the SPF record for a domain using Google's DNS-over-HTTPS API.
    This avoids the need for 'pip install dnspython'.
    """
    print(f"[*] Fetching SPF record for '{domain}'...")
    
    # Google Public DNS DoH API
    url = f"https://dns.google/resolve?name={domain}&type=TXT"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if 'Answer' not in data:
            print(f"[!] No TXT records found for {domain}.")
            return None

        # Filter for the SPF record (starts with "v=spf1")
        spf_records = []
        for answer in data['Answer']:
            # TXT data often comes inside quotes, e.g. "v=spf1..."
            txt_data = answer['data'].strip('"')
            # Handle split TXT records (chunks combined by spaces)
            txt_data = txt_data.replace('" "', '')
            
            if txt_data.startswith('v=spf1'):
                spf_records.append(txt_data)

        if not spf_records:
            print(f"[!] No SPF record found for {domain}.")
            return None
            
        if len(spf_records) > 1:
            print(f"[!] WARNING: Multiple SPF records found! This is invalid.")
            for r in spf_records:
                print(f"    - {r}")
            return spf_records[0] # Return the first one for analysis
            
        return spf_records[0]

    except Exception as e:
        print(f"[!] Error fetching DNS: {e}")
        return None

def analyze_spf(spf_string):
    """
    Analyzes the SPF string for syntax errors and security best practices.
    """
    print(f"\n--- Analysis for: {spf_string} ---")
    issues = []
    warnings = []
    
    # 1. Basic Syntax
    if not spf_string.startswith("v=spf1"):
        issues.append("Record does not start with 'v=spf1'")
    
    # 2. Lookup Counting (Approximation)
    # The limit is 10 DNS lookups. Mechanisms that trigger lookups: include, a, mx, ptr, exists, redirect
    lookup_mechanisms = ['include:', 'a:', 'mx:', 'ptr:', 'exists:', 'redirect=']
    # Plain 'a' and 'mx' also count
    tokens = spf_string.split()
    lookup_count = 0
    
    for token in tokens:
        # Check specific modifiers
        for mech in lookup_mechanisms:
            if token.startswith(mech):
                lookup_count += 1
        # Check standalone 'a' and 'mx'
        if token == 'a' or token == 'mx':
            lookup_count += 1
            
    print(f"[*] DNS Lookup Count (Approx): {lookup_count}/10")
    if lookup_count > 10:
        issues.append(f"Too many DNS lookups ({lookup_count}). Limit is 10 (RFC 7208).")

    # 3. Security Checks
    if "+all" in tokens:
        issues.append("Usage of '+all' allows the entire internet to spoof your domain.")
    elif "?all" in tokens:
        warnings.append("Usage of '?all' (Neutral) provides no protection.")
    elif not (tokens[-1].endswith("-all") or tokens[-1].endswith("~all") or "redirect=" in tokens[-1]):
        issues.append("Record does not end with a strict policy ('-all' or '~all').")

    # 4. Deprecated Mechanisms
    if "ptr" in spf_string:
        warnings.append("The 'ptr' mechanism is deprecated and should not be used.")

    # Report
    if not issues and not warnings:
        print("✅ Status: Valid & Secure")
    else:
        if issues:
            print("❌ Critical Issues:")
            for i in issues:
                print(f"   - {i}")
        if warnings:
            print("⚠️  Warnings:")
            for w in warnings:
                print(f"   - {w}")

def main():
    parser = argparse.ArgumentParser(description="Check SPF record syntax and security.")
    parser.add_argument('domain', help="Domain name to check (e.g., google.com)")
    
    args = parser.parse_args()
    
    record = fetch_spf_record(args.domain)
    
    if record:
        analyze_spf(record)

if __name__ == "__main__":
    main()