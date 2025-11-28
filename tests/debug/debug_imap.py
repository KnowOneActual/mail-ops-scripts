import email
import getpass
import imaplib
import sys
from email.header import decode_header


def debug_reports(username, password, server, folder="INBOX"):
    print(f"[*] Connecting to {server}...")
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(username, password)
        mail.select(folder)
    except Exception as e:
        print(f"[!] Error: {e}")
        return

    # Search for DMARC emails
    status, messages = mail.search(
        None, '(OR SUBJECT "Report Domain" SUBJECT "DMARC Aggregate Report")'
    )

    if not messages[0]:
        print("[-] No reports found.")
        return

    # Inspect the last 3 emails
    email_ids = messages[0].split()[-3:]
    print(f"[*] Inspecting the last {len(email_ids)} emails...\n")

    for e_id in email_ids:
        res, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                print(f"--- Subject: {msg['subject']} ---")

                if msg.is_multipart():
                    # Walk through the email parts
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        filename = part.get_filename()

                        print(f"   [Type]: {content_type}")
                        print(f"   [Disp]: {content_disposition}")
                        print(f"   [Name]: {filename}")
                        print("   ---")
                else:
                    print("   [!] Not multipart (Single text message?)")
                    print(f"   [Type]: {msg.get_content_type()}")

                print("\n")

    mail.logout()


if __name__ == "__main__":
    email_user = input("Email: ")
    email_pass = getpass.getpass("App Password: ")
    # Corrected function call below
    debug_reports(email_user, email_pass, "imap.mail.me.com")
