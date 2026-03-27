import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time

def send_email(to_email, subject, html_content, retries=3, delay=5):
    """
    Send email via SendGrid API with optional retry logic.
    """
    message = Mail(
        from_email=os.environ.get("MAIL_USERNAME"),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    for attempt in range(1, retries + 1):
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(f"✅ Email sent! Status: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return False