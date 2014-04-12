import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import settings

class MailClient(object):

    def __init__(self):
        '''
        Creates a new client
        '''

        self.client = smtplib.SMTP(**settings.SMTP)
        self.sender = settings.SENDER
        self.client.starttls()
        self.client.login(self.sender, settings.PASSWORD)

    def send(self, recipient, body, subject):
        '''
        Sends an email
        recipient = A User objet from the User table
        body = The body of the email
        subject = The subject of the email

        All emails are sent from the address defined in settings.SENDER
        '''

        email = MIMEMultipart('alternative')
        email['From'] = self.sender
        email['To'] = recipient.email
        email['Subject'] = subject
        email.attach(MIMEText(body, 'html'))

        if settings.DEBUG:
            print email.as_string()
        else:
            print "sending"
            self.client.sendmail(self.sender, recipient.email, email.as_string())


class Subjects:
    DIGEST = '[Teachboost] Task Digest'
    HELP = '[Teachboost] Message Help'
    RESPONSE = '[Teachboost] Manager Response'
