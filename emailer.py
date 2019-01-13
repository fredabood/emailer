import os
import smtplib


def send_email(recipient, subject, body, sender=os.environ.get('EMAIL_ADDRESS'), password=os.environ.get('EMAIL_PASSWORD')):

    message = f"From: {sender}\nTo: {recipient}\nSubject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, message)
        server.close()
        print("Successfully sent email")

    except Exception as e:
        print("Failed to send email because of: " + e)
