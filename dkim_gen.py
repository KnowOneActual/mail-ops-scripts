import subprocess
import sys
import os
import argparse
import shutil

def check_openssl():
    """Checks if OpenSSL is installed and available in the PATH."""
    if not shutil.which("openssl"):
        print("Error: 'openssl' command not found.")
        print("This script requires OpenSSL to generate keys without external Python dependencies.")
        sys.exit(1)

def generate_keys(selector, output_dir="."):
    """
    Generates a 2048-bit RSA private key and extracts the public key.
    Returns the public key string (base64) for the DNS record.
    """
    priv_filename = os.path.join(output_dir, f"{selector}.private")
    
    print(f"[*] Generating 2048-bit RSA key for selector '{selector}'...")

    # 1. Generate Private Key
    # cmd: openssl genrsa -out {selector}.private 2048
    try:
        subprocess.run(
            ["openssl", "genrsa", "-out", priv_filename, "2048"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        print(f"Error generating private key: {e}")
        sys.exit(1)
    
    # 2. Extract Public Key
    # cmd: openssl rsa -in {selector}.private -pubout -outform PEM
    try:
        result = subprocess.run(
            ["openssl", "rsa", "-in", priv_filename, "-pubout", "-outform", "PEM"],
            check=True,
            capture_output=True,
            text=True
        )
        raw_public_key = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error extracting public key: {e}")
        sys.exit(1)

    # 3. Clean up Public Key (remove headers/footers and newlines)
    lines = raw_public_key.splitlines()
    clean_key = "".join(line for line in lines if "-----" not in line)
    
    print(f"✅ Private key saved to: {priv_filename}")
    print("⚠️  KEEP THIS FILE SAFE! Never share it.")
    
    return clean_key

def main():
    parser = argparse.ArgumentParser(description="Generate DKIM RSA keys and DNS records.")
    parser.add_argument('selector', help="The DKIM selector (e.g., 'mail', 'k1', 'default')")
    parser.add_argument('--domain', help="The domain name (optional, for formatted output)", default="yourdomain.com")
    
    args = parser.parse_args()
    
    check_openssl()
    
    public_key_data = generate_keys(args.selector)
    
    # Construct the DNS Record
    dkim_record_name = f"{args.selector}._domainkey.{args.domain}"
    dkim_value = f"v=DKIM1; k=rsa; p={public_key_data}"
    
    print("\n" + "="*60)
    print("DNS TXT RECORD TO ADD")
    print("="*60)
    print(f"Host/Name:  {args.selector}._domainkey")
    print(f"Value:      {dkim_value}")
    print("-" * 60)
    print("NOTE: If your DNS provider (like Godaddy) splits long strings,")
    print("      you may need to break the 'p=' value into chunks.")
    print("="*60)

if __name__ == "__main__":
    main()