import imaplib
import email
import os

# === CONFIGURATION ===
EMAIL = "xml@escariz.com.br"
PASSWORD = "8g3J?q5j3"
IMAP_SERVER = "mail.escariz.com.br"
SAVE_DIR = "attachments"

# === CONNECT TO SERVER ===
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# === FETCH ALL EMAIL IDs ===
status, data = mail.search(None, "ALL")
if status != "OK" or not data or not data[0]:
    print("No emails found.")
    mail.logout()
    exit()

email_ids = data[0].split()

os.makedirs(SAVE_DIR, exist_ok=True)

# === PROCESS EACH EMAIL ===
for e_id in email_ids:
    status, msg_data = mail.fetch(e_id, "(RFC822)")
    if status != "OK":
        continue

    msg = email.message_from_bytes(msg_data[0][1])
    sender = msg.get("From", "(Unknown sender)")
    subject = msg.get("Subject", "(No Subject)")

    xml_attachments = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()
            if filename and filename.lower().endswith(".xml"):
                xml_attachments.append((filename, part))

    if not xml_attachments:
        continue  # Skip if no .xml attachments

    print(f"Processing email from {sender}, subject: '{subject}'")

    for filename, part in xml_attachments:
        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(part.get_payload(decode=True))
        print(f"Saved: {filename}")

mail.logout()
