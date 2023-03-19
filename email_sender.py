import smtplib
import ssl
from email.message import EmailMessage
import os

class EmailSender:
    def __init__(self) -> None:
        # Define email sender and receiver
        self.email_sender = os.environ['MAIL_ADDR']
        self.email_password = os.environ['MAIL_PASS']
    def send_mail(self,email_receiver:str, subject:str,message:str) -> None:
        """
        Send to email_receiver an email with subject and message
        """
        em = EmailMessage()
        em['From'] = self.email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(message)
        # Add SSL (layer of security)
        context = ssl.create_default_context()
        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, email_receiver, em.as_string())