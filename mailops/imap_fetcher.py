import imaplib
import email
import os
import argparse
import getpass
from email.header import decode_header
import sys
import traceback

def clean_filename(filename):
    """Sanitizes filenames to prevent directory traversal issues."""
    if not filename:
        return None
    return "".join(c for c in filename if c.isalnum() or c in "._-!")

def get_safe_date(msg):
    """Extracts a safe YYYY-MM-DD date from the email."""
    date_str = msg.get("Date")
    if date_str:
        try:
            date_obj = email.utils.parsedate_to_datetime(date_str)
            return date_obj.strftime("%Y-%m-%d")
        except:
            pass
    return "unknown_date"

def safe_decode(value):
    """Safely decodes bytes to string."""
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='ignore')
    return str(value)

def fetch_reports(username, password, server, folder="INBOX"):
    print(f"[*] Connecting to {server}...")
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(username, password)
    except Exception as e:
        print(f"[!] Login Failed: {e}")
        return

    print("[*] Login successful. Searching for DMARC reports...")
    mail.select(folder)

    # Search for likely DMARC emails
    search_criteria = '(OR SUBJECT "Report Domain" SUBJECT "DMARC Aggregate Report")'
    status, messages = mail.search(None, search_criteria)
    
    if status != "OK" or not messages[0]:
        print("[-] No DMARC reports found in INBOX.")
        return

    email_ids = messages[0].split()
    print(f"[*] Found {len(email_ids)} potential report emails. Processing...")

    count = 0
    
    for e_id in email_ids:
        try:
            e_id_str = safe_decode(e_id)
            
            # Switch to BODY[] for more reliable fetching
            res, msg_data = mail.fetch(e_id, "(BODY[])")
            if res != 'OK': 
                continue
            
            raw_email = None
            
            # Strategy 1: Look for the standard tuple response
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Usually the email body is the second element in the tuple
                    raw_email = response_part[1]
                    break
            
            # Strategy 2: Fallback (Nuclear Option)
            # If no tuple found, find the largest bytes object in the list
            if raw_email is None:
                largest_part = b""
                for part in msg_data:
                    if isinstance(part, bytes) and len(part) > len(largest_part):
                        largest_part = part
                
                # If we found a substantial chunk of data, assume it's the email
                if len(largest_part) > 100: # Arbitrary small size check
                    raw_email = largest_part

            if raw_email is None:
                print(f"    [!] Skipping email {e_id_str}: Could not locate message body in response.")
                continue

            # Parse the bytes into an email object
            msg = email.message_from_bytes(raw_email)
            folder_date = get_safe_date(msg)

            # Walk through parts
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                
                filename = part.get_filename()
                
                # 1. Header Decoding
                if filename:
                    try:
                        decoded_list = decode_header(filename)
                        filename_bytes, encoding = decoded_list[0]
                        if isinstance(filename_bytes, bytes):
                            filename = filename_bytes.decode(encoding or "utf-8", errors='ignore')
                        else:
                            filename = str(filename_bytes)
                    except Exception:
                        filename = str(filename)
                
                # 2. Content Type sniffing
                content_type = part.get_content_type()
                if not filename and ('gzip' in content_type or 'zip' in content_type or 'xml' in content_type):
                    safe_subject = clean_filename(msg.get("Subject", "report"))
                    ext = ".gz" if "gzip" in content_type else ".zip" if "zip" in content_type else ".xml"
                    filename = f"autoname_{safe_subject}_{e_id_str}{ext}"

                # 3. Save
                if filename:
                    filename = clean_filename(filename)
                    if filename and filename.lower().endswith(('.xml', '.gz', '.zip')):
                        save_dir = os.path.join("dmarc_reports", folder_date)
                        os.makedirs(save_dir, exist_ok=True)
                        
                        filepath = os.path.join(save_dir, filename)
                        
                        if not os.path.exists(filepath):
                            payload = part.get_payload(decode=True)
                            if payload:
                                with open(filepath, "wb") as f:
                                    f.write(payload)
                                print(f"    [+] Saved: {folder_date}/{filename}")
                                count += 1

        except Exception as e:
            print(f"    [!] Critical error processing email {e_id}: {e}")
            continue

    mail.close()
    mail.logout()
    print(f"\n[*] Download complete. Saved {count} new reports locally.")
    print(f"[*] Reports are located in: {os.path.abspath('dmarc_reports')}")

def main():
    parser = argparse.ArgumentParser(description="Download DMARC reports from IMAP.")
    parser.add_argument('--email', required=True, help="Your email address")
    parser.add_argument('--server', default="imap.mail.me.com", help="IMAP Server")
    
    args = parser.parse_args()
    
    print(f"Enter IMAP Password for {args.email}")
    try:
        password = getpass.getpass("> ")
    except KeyboardInterrupt:
        sys.exit(0)
    
    fetch_reports(args.email, password, args.server)

if __name__ == "__main__":
    main()