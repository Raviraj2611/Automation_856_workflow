import pandas as pd
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from ErrorHandler.error_handler import email_error 

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

dc_email_map = {
    "DC01": "lavanya.p8620@gmail.com",
    "DC02": "piyushraviraj2611@gmail.com",
    "DC03": "lavanya.p8620@gmail.com",
    "DC04": "piyushraviraj2611@gmail.com",
    "DC05": "lavanya.p8620@gmail.com"
}

def authenticate_gmail():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Email/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with open(attachment_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
    msg.attach(part)

    return {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def send_email(service, sender, to, subject, body, attachment_path): 
    try:
        message = create_message(sender, to, subject, body, attachment_path)
        sent = service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {to} | Message ID: {sent['id']}")
    except Exception as e:
        print("Error sending email:", e)
        email_error("Error sending email","ERROR")

def send_reports(excel_file, sender_email):
    xl = pd.ExcelFile(excel_file)
    sheets = xl.sheet_names

    service = authenticate_gmail()

    for sheet in sheets:
        if sheet not in dc_email_map:
            print(f"No email mapped for sheet: {sheet} — skipping")
            continue

        recipient_email = dc_email_map[sheet]

        sheet_data = xl.parse(sheet)
        sheet_csv = f"{sheet}.csv"
        sheet_data.to_csv(sheet_csv, index=False)

        subject = f"Order Status Report {sheet}"
        body = f"Hello Team,\n\nPlease find the attached order status for {sheet}.\n\nRegards\nAutomation Bot"

        send_email(service, sender_email, recipient_email, subject, body, sheet_csv)

        os.remove(sheet_csv)
        