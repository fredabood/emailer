import os

import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class Email():

    def __init__(self, recipient, subject, body, files=[], sender=os.environ.get('EMAIL_ADDRESS'), password=os.environ.get('EMAIL_PASSWORD')):

        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.sender = sender
        self.password = password
        self.files = files
        self.message = self.build_msg()

    def send(self):

        try:
            server = smtplib.SMTP(host="smtp.gmail.com", port=587)
            server.ehlo()
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.recipient, self.message.as_string())
            server.close()
            print("Successfully sent email")

        except Exception as e:
            print("Failed to send email because of: " + e)

    def build_msg(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender
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
