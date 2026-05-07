import imaplib
import email
import os
from datetime import datetime

EMAIL = "jures@basicinception.com"
PASSWORD = "sloo nkmu glzw mbtv"

year = datetime.now().strftime("%Y")

# Google Drive folder (Windows mounted in WSL)
SAVE_DIR = f"/mnt/g/My Drive/Basic Inception/02 - Finance/01 - Financial Documents/07 - Transactions/{year}/02 - Accounts Payable/01 - Bills Received/TIME"

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Search unread emails with attachments
status, messages = mail.search(None, '(UNSEEN SUBJECT "Your Latest Time Bill")')

for num in messages[0].split():
    status, data = mail.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    subject = msg["subject"] or ""
    date = msg["date"]

    try:
        parsed_date = datetime.strptime(date[:25], "%a, %d %b %Y %H:%M:%S")
    except:
        parsed_date = datetime.now()

    year = parsed_date.strftime("%Y")
    month = parsed_date.strftime("%m")

    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()

            if not filename:
                continue

            if not filename.lower().endswith(".pdf"):
                continue

            # Create folder
            folder = f"{SAVE_DIR}"
            os.makedirs(folder, exist_ok=True)

            filepath = os.path.join(folder, filename)

            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))

            print(f"Saved: {filepath}")