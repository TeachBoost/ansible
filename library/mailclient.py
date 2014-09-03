import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import settings


class MailClient(object):

    def __init__(self):
        '''
        Creates a new client
        '''

    def smtp_login(self):
        '''
        Logs into the smtp server
        Returns the sender's credentials
        '''
        self.client = smtplib.SMTP(**settings.SMTP)
        self.sender = settings.SENDER
        self.client.ehlo()
        self.client.starttls()
        self.client.ehlo()
        self.client.login(self.sender, settings.PASSWORD)
        return self.sender

    def send(self, recipient, body, subject):
        '''
        Sends an email
        recipient = A User objet from the User table
        body = The body of the email
        subject = The subject of the email

        All emails are sent from the address defined in settings.SENDER
        '''

        email = MIMEMultipart('alternative')
        email['From'] = settings.SENDER
        email['To'] = recipient.email
        email['Subject'] = subject
        email.attach(MIMEText(body, 'html'))

        if settings.SEND_EMAIL:
            sender = self.smtp_login()
            self.client.sendmail(sender, recipient.email, email.as_string())
        return email.as_string().split('\n')


class Subjects:
    DIGEST = '[Teachboost] Task Digest'
    HELP = '[Teachboost] Message Help'
    RESPONSE = '[Teachboost] Manager Response'
    SUBSCRIPTIONS = '[Teachboost] Your Subscriptions'
