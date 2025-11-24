import sys
import json
import urllib.request
import argparse
import ipaddress

# Common RBLs (Real-time Blackhole Lists)
RBL_PROVIDERS = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "b.barracudacentral.org",
    "dnsbl.sorbs.net",
    "ips.backscatterer.org"
]

def resolve_domain(domain):
    """
    Resolves a domain name to an IP address using Google DoH.
    """
    print(f"[*] Resolving IP for: {domain}...", end=" ", flush=True)
    url = f"https://dns.google/resolve?name={domain}&type=A"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        if 'Answer' in data:
            # Filter for A records (type 1)
            for answer in data['Answer']:
                if answer['type'] == 1:
                    ip = answer['data']
                    print(f"Found {ip}")
                    return ip
        
        print("\n[!] Error: No A record found for this domain.")
        return None

    except Exception as e:
        print(f"\n[!] DNS Lookup Error: {e}")
        return None

def check_rbl(ip_address, rbl_domain):
    """
    Checks if an IP is listed on a specific RBL using Google DoH.
    """
    try:
        reversed_ip = ".".join(reversed(ip_address.split(".")))
    except Exception:
        return "Invalid IP format"

    query_domain = f"{reversed_ip}.{rbl_domain}"
    url = f"https://dns.google/resolve?name={query_domain}&type=A"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        if 'Answer' in data:
            return data['Answer'][0]['data']
        else:
            return None

    except Exception as e:
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description="Check if an IP or Domain is on email blacklists.")
    parser.add_argument('target', help="IP address (1.2.3.4) OR Domain name (google.com)")
    
    args = parser.parse_args()
    target_input = args.target
    target_ip = None

    # 1. Determine if input is IP or Domain
    try:
        # Try to validate as IP
        ipaddress.ip_address(target_input)
        target_ip = target_input
    except ValueError:
        # If not an IP, assume it's a domain and resolve it
        target_ip = resolve_domain(target_input)
        if not target_ip:
            sys.exit(1)

    print(f"[*] Checking Blacklist Status for: {target_ip}")
    print("-" * 60)
    print(f"{'RBL Provider':<30} | {'Status':<10}")
    print("-" * 60)
    
    issues_found = 0
    
    for rbl in RBL_PROVIDERS:
        result = check_rbl(target_ip, rbl)
        
        if result is None:
            print(f"{rbl:<30} | ✅ Clean")
        elif result.startswith("Error") or result == "Invalid IP format":
            print(f"{rbl:<30} | ⚠️  {result}")
        else:
            print(f"{rbl:<30} | ❌ LISTED ({result})")
            issues_found += 1

    print("-" * 60)
    if issues_found == 0:
        print("🎉 Good news! This IP is not listed on the checked RBLs.")
    else:
        print(f"warning: This IP is listed on {issues_found} blacklists.")

if __name__ == "__main__":
    main()