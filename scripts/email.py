import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

# Email you're sending from
PYTHON_EMAIL = os.getenv("PYTHON_GMAIL_ADRESS")
PYTHON_PASSWORD = os.getenv("PYTHON_GMAIL_PASSWORD")
# Email you're sending to
MY_EMAIL = os.getenv("MY_EMAIL_ADRESS")


class Email_Handler():
    def __init__(self):
        pass

    def send_contact_mail(self, user_name, user_mail_adress, user_message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=PYTHON_EMAIL, password=PYTHON_PASSWORD)
            connection.sendmail(
                from_addr=user_mail_adress,
                to_addrs=MY_EMAIL,
                msg=f"Subject:New message from {user_name}\n\n{user_message}\n\nRespond to {user_mail_adress}"
            )
