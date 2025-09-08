import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Dummy config – তোমার নিজের SMTP কনফিগ লাগবে
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "raju.niceschool@gmail.com"
SMTP_PASSWORD = "aiap prpm csyl ylqf"   # বা App Password

FROM_EMAIL = "raju.niceschool@gmail.com"

def send_email(to_email: str, subject: str, body: str):
    """Send an email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False
