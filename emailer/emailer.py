import os

import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class Session(smtplib.SMTP):

    def __init__(self, sender=os.environ.get('EMAIL_ADDRESS'), password=os.environ.get('EMAIL_PASSWORD')):

        self.sender = sender
        self.password = password
        self.session_info = self.info()

    def info(self):

        provider = self.sender.split('@')[1].split('.')[-2]

        filler = ''
        tld = 'com'
        port = 587

        if provider in ['yahoo', 'att']:
            filler = '.mail'
        elif provider == 'outlook':
            filler = '-mail'

        if filler in ['att', 'comcast', 'verizon']:
            tld = 'net'

        host = f'smtp{filler}.{provider}.{tld}'

        if provider in ['att', 'verizon']:
            port = 465

        return dict(host=host, port=port)

    def start(self):

        session = smtplib.SMTP(**self.session_info)
        session.ehlo()
        session.starttls()
        session.login(self.sender, self.password)

        return session


class Email():

    def __init__(self, recipient, subject, body, files=[], session=None):

        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.files = files

        if session:
            self.session = session
            self.close_session = False
        else:
            self.session = Session()
            self.close_session = True

        self.message = self.build_msg()

    def send(self):

        try:
            server = self.session.start()
            server.sendmail(self.session.sender, self.recipient, self.message.as_string())

            print("Successfully sent email")

        except Exception as e:
            print("Failed to send email because of: " + str(e))

        if self.close_session:
            server.close()

    def build_msg(self):
        msg = MIMEMultipart()
        msg['From'] = self.session.sender
        msg['To'] = ', '.join(self.recipient) if type(self.recipient) is list else ', '.join([self.recipient])
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.body))

        for file in self.files:
            # part = MIMEApplication(attachment.read(), Name=basename(file))
            filename = file.split('/')[-1]
            attachment = open(file, "rb").read()

            part = MIMEApplication(attachment, Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'

            msg.attach(part)

        return msg
