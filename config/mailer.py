import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASS")


def send_email(to_email, subject, html_content):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"Budget Buddy 2.0 <{SENDER_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Gửi email thành công tới {to_email}")
        return True
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}")
        return False
