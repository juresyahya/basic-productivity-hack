import imaplib
import email
import os
from datetime import datetime
from email.header import decode_header, make_header

EMAIL = "jures@basicinception.com"
PASSWORD = "sloo nkmu glzw mbtv"

BASE_DIR = "/mnt/g/My Drive/Basic Inception/02 - Finance/01 - Financial Documents/07 - Transactions/{year}/02 - Accounts Payable/01 - Bills Received"

BILLS = [
    {
        "name": "TIME",
        "subject": "Your Latest Time Bill",
        "sender": None,
        "reply_to": None,
    },
    {
        "name": "MACROMAC",
        "subject": "Monthly Invoice",
        "sender": "noreply@copier2u.com",
        "reply_to": None,
    },
    {
        "name": "COWAY",
        "subject": "COWAY",
        "sender": None,
        "reply_to": "nani.coway@yahoo.com",
    },
    {
        "name": "DigitalOcean",
        "subject": "DigitalOcean",
        "sender": None,
        "reply_to": None,
    },    
]

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

for bill in BILLS:
    criteria = f'(UNSEEN SUBJECT "{bill["subject"]}")'
    if bill["sender"]:
        criteria = f'(UNSEEN SUBJECT "{bill["subject"]}" FROM "{bill["sender"]}")'

    status, messages = mail.search(None, criteria)

    for num in messages[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        if bill["reply_to"]:
            reply_to = msg.get("Reply-To", "")
            if bill["reply_to"].lower() not in reply_to.lower():
                continue

        date = msg["date"]

        try:
            parsed_date = datetime.strptime(date[:25], "%a, %d %b %Y %H:%M:%S")
        except Exception:
            parsed_date = datetime.now()

        year = parsed_date.strftime("%Y")

        save_dir = os.path.join(BASE_DIR.format(year=year), bill["name"])

        for part in msg.walk():
            raw_filename = part.get_filename()

            if not raw_filename:
                continue

            filename = str(make_header(decode_header(raw_filename)))

            if not filename.lower().endswith(".pdf"):
                continue

            os.makedirs(save_dir, exist_ok=True)

            filepath = os.path.join(save_dir, filename)

            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))

            print(f"Saved: {filepath}")
