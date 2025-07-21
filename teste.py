import imaplib
import email
import os
from datetime import datetime
#from datetime import timedelta

def DownloadXML():
    # === CONFIGURATION ===
    EMAIL = "xml@escariz.com.br"
    PASSWORD = "8g3J?q5j3"
    IMAP_SERVER = "mail.escariz.com.br"
    SAVE_DIR = "attachments"

    # === CONNECT TO SERVER ===
    mail = imaplib.IMAP4(IMAP_SERVER, 143)
    mail.starttls()
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # === FILTER EMAILS FROM 2025 ON ===
    # Format: DD-MMM-YYYY (e.g., 01-Jan-2025)
    dia_atual = datetime.today().strftime("%d-%b-%Y")
    #dia_anterior = (dia_atual - timedelta(days=1))
    #pega todas os XMLs do dia anterior, garantindo que se a NFe foi enviada no final do dia, ainda assim vai conseguir pegar ela.
    File_object = open(r"ultimaData.txt","r")
    status, data = mail.search(None, 'SINCE', File_object.readline())
    File_object.close()
    File_object = open(r"ultimaData.txt", "w")
    File_object.write(dia_atual)
    if status != "OK" or not data or not data[0]:
        print(f"No emails from {dia_atual} or later found.")
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

        # (Optional) Parse and confirm date manually if you want extra safety
        # date_tuple = email.utils.parsedate_tz(msg.get("Date"))
        # if date_tuple:
        #     msg_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        #     if msg_date.year < 2025:
        #         continue  # Extra safeguard

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
