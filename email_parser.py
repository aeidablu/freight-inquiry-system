import imaplib
import email
from dotenv import load_dotenv
import os
import re

load_dotenv(override=True)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def check_staff_reply(reference_number: str) -> dict:
    """Check Gmail for staff reply with rates"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(SENDER_EMAIL, SENDER_PASSWORD)
        mail.select("inbox")

        search_query = f'(SUBJECT "{reference_number}")'
        status, messages = mail.search(None, search_query)

        if status != "OK" or not messages[0]:
            mail.logout()
            return {}

        email_ids = messages[0].split()
        latest_id = email_ids[-1]

        status, msg_data = mail.fetch(latest_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        rates = extract_rates_from_email(body, reference_number)
        mail.logout()
        return rates

    except Exception as e:
        print(f"Email check error: {e}")
        return {}

def extract_rates_from_email(body: str, reference_number: str) -> dict:
    """Extract rate details from staff reply email"""

    def find_amount(pattern, text):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip().replace(',', '')
        return "0"

    rates = {
        "reference_number": reference_number,
        "ocean_freight": find_amount(
            r'ocean.*?freight.*?:?\s*\$?\s*([\d,]+(?:\.\d{2})?)', body),
        "origin_charges": find_amount(
            r'origin.*?charges?.*?:?\s*\$?\s*([\d,]+(?:\.\d{2})?)', body),
        "destination_charges": find_amount(
            r'destination.*?charges?.*?:?\s*\$?\s*([\d,]+(?:\.\d{2})?)', body),
        "inland_transport": find_amount(
            r'inland.*?transport.*?:?\s*\$?\s*([\d,]+(?:\.\d{2})?)', body),
        "insurance": find_amount(
            r'insurance.*?:?\s*\$?\s*([\d,]+(?:\.\d{2})?)', body),
        "transit_time": find_amount(
            r'transit.*?time.*?:?\s*([\d]+)', body),
        "remarks": ""
    }

    remarks_match = re.search(
        r'remarks?.*?:?\s*(.+?)(?:\n|$)', body, re.IGNORECASE)
    if remarks_match:
        rates["remarks"] = remarks_match.group(1).strip()

    return rates