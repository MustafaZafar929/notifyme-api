import os
from dotenv import load_dotenv
load_dotenv()  

from celery import Celery
import smtplib
from email.message import EmailMessage

app = Celery('mailing', broker='redis://localhost:6379/0')


EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

@app.task
def send_mail(receiver_address: str, subject: str, body: str):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_address
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f'Email sent to {receiver_address}')
    except Exception as e:
        print(f'Failed to send email to {receiver_address}: {e}')
        raise


#celery -A mailing worker --loglevel=info --pool=solo