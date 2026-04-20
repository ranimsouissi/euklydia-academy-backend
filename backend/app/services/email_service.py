from app.core.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_email: str, subject: str, html_content: str):

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())


def send_reset_password_email(to_email: str, reset_link: str):

    subject = "Reset your password - Euklydia"

    html = f"""
    <h2>Reset your password</h2>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">{reset_link}</a>
    """

    send_email(to_email, subject, html)