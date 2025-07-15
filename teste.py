import imaplib
import email
import os

# === CONFIGURATION ===
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"
IMAP_SERVER = "mail.escariz.com.br"
SENDERS = ["alice@example.com", "bob@example.com"]
SAVE_DIR = "attachments"

# === CONNECT TO SERVER ===
mail = imaplib.IMAP4_SSL(465)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# === COMBINE EMAIL IDS FROM MULTIPLE SENDERS ===
all_email_ids = set()

for sender in SENDERS:
    status, data = mail.search(None, f'(FROM "{sender}")')
    if status == "OK":
        ids = data[0].split()
        all_email_ids.update(ids)

if not all_email_ids:
    print("No matching emails found.")
    mail.logout()
    exit()

os.makedirs(SAVE_DIR, exist_ok=True)

# === PROCESS EACH MATCHING EMAIL ===
for e_id in all_email_ids:
    status, msg_data = mail.fetch(e_id, "(RFC822)")
    if status != "OK":
        continue

    msg = email.message_from_bytes(msg_data[0][1])

    # Count attachments
    attachments = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()
            if filename:
                attachments.append((filename, part))

    # ✅ Only process if exactly 2 attachments
    sender = msg.get("From", "(Unknown sender)")
    subject = msg.get("Subject", "(No Subject)")
    print(f"Processing email from {sender}, subject: '{subject}'")

    for filename, part in attachments:
        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(part.get_payload(decode=True))
        print(f"Saved: {filename}")
mail.logout()
