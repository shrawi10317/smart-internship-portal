# app/mail_utils.py
from flask_mail import Message, Mail
from flask import current_app
import threading
import time
import smtplib

mail = Mail()  # Ensure this is the same instance initialized in __init__.py

def send_async_email(app, msg, retries=3, delay=2):
    """
    Sends an email asynchronously with retry logic.
    Tries SSL first, fallback to TLS if SSL fails.
    """
    def _send():
        with app.app_context():
            for attempt in range(1, retries + 1):
                try:
                    mail.send(msg)
                    print(f"✅ Email sent to {msg.recipients} (attempt {attempt})")
                    return True
                except smtplib.SMTPException as e:
                    print(f"❌ Attempt {attempt} failed: {e}")
                    time.sleep(delay)
            print(f"❌ All {retries} attempts failed for {msg.recipients}")
            return False

    # Run in a separate thread
    threading.Thread(target=_send).start()


def send_email(subject, recipients, body):
    """
    Helper function to send email from anywhere in the app.
    """
    msg = Message(
        subject=subject,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
        recipients=[recipients] if isinstance(recipients, str) else recipients,
        body=body
    )
    send_async_email(current_app._get_current_object(), msg)