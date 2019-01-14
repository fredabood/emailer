import os

import smtplib
import imapclient
import pyzmail

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class Email():

    def __init__(self, username=os.environ.get('EMAIL_ADDRESS'), password=os.environ.get('EMAIL_PASSWORD')):

        if username and password:

            try:
                self.username = username
                self.password = password
                self.session = Session(self.username, self.password)
                self.smtp, self.imap = self.session.start()

            except Exception as e:
                print("Failed because of: " + e)

        else:
            print("Please pass a username and password.")

    def send(self, recipient, subject, body, files=[], close_session=False):

        message = self.build_msg(recipient, subject, body, files)

        try:
            self.smtp.sendmail(self.session.sender, recipient, message.as_string())

            if close_session:
                self.smtp.close()

            print("Successfully sent email")

        except Exception as e:
            print("Failed to send email because of: " + str(e))

    def read(self, folder, queries, close_session=False):

        self.imap.select_folder(folder, readonly=True)
        uids = self.imap.search(queries)

        messages = {}
        for uid in uids:
            rawMessages = self.imap.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(rawMessages[uid]['BODY[]'])

            messages[uid] = dict(
                subject=message.get_subject(),
                sender=message.get_addresses('from'),
                recipient=message.get_addresses('to'),
                cc=message.get_addresses('cc'),
                bcc=message.get_addresses('bcc'),
                text_part=message.text_part.get_payload().decode(message.text_part.charset),
                html_part=message.html_part.get_payload().decode(message.html_part.charset),
            )

        if close_session:
            self.imap.logout()

        return messages

    def build_msg(self, recipient, subject, body, files):
        msg = MIMEMultipart()
        msg['From'] = self.session.sender
        msg['To'] = ', '.join(recipient) if type(recipient) is list else ', '.join([recipient])
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(body))

        for file in files:
            filename = file.split('/')[-1]
            attachment = open(file, "rb").read()

            part = MIMEApplication(attachment, Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'

            msg.attach(part)

        return msg


class Session():

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.smtp_host, self.imap_host, self.smtp_port = self.info()

    def info(self):

        provider = self.username.split('@')[1].split('.')[-2]

        filler = ''
        tld = 'com'

        if provider in ['yahoo', 'att']:
            filler = '.mail'
        elif provider == 'outlook':
            filler = '-mail'

        if filler in ['att', 'comcast', 'verizon']:
            tld = 'net'

        imap = dict(prefix='imap', filler=filler, provider=provider, tld=tld)
        smtp = dict(prefix='smtp', filler=filler, provider=provider, tld=tld)

        imap = '{prefix}{filler}.{provider}.{tld}'.format(**imap)
        smtp = '{prefix}{filler}.{provider}.{tld}'.format(**smtp)

        return smtp, imap, 465

    def start(self, prefix=None):

        smtp_info = dict(host=self.smtp_host, port=self.smtp_port)

        smtp = smtplib.SMTP_SSL(**smtp_info)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.username, self.password)

        imap = imapclient.IMAPClient(host=self.imap_host, ssl=True)
        imap.login(self.username, self.password)

        return smtp, imap
