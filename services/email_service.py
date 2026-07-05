import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config_email import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    ALERT_EMAIL_TO
)


def send_email_alert(subject: str, body: str):

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = ALERT_EMAIL_TO
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        server.sendmail(
            EMAIL_USER,
            ALERT_EMAIL_TO,
            msg.as_string()
        )

        server.quit()

        print("EMAIL SENT ✔")

    except Exception as e:
        print("EMAIL FAILED ❌", str(e))


import asyncio

def send_email_async(subject, body):
    asyncio.to_thread(send_email_alert, subject, body)