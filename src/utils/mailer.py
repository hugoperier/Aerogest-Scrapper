import smtplib, ssl
from src.utils.formatReservation import email_format
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer:
    def __init__(self, config, format = email_format):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = config.get("SENDER_EMAIL")
        self.password = config.get("SENDER_PASSWORD")
        self.receiver_email = config.get("RECEIVER_EMAIL")
        self.format = format

    def notify(self, matches):
        message = self.format(matches)
        subject = f"Aerogest Scrapper: {len(matches)} matches found"
        self.send_email(subject, message)

    def notifyError(self, error):
        subject = "Aerogest Scrapper: Error"
        message = error
        self.send_email(subject, message)

    def send_email(self, subject, message):
        email = MIMEMultipart('alternative')
        email['From'] = self.sender_email
        email['To'] = self.receiver_email
        email['Subject'] = subject
        email.attach(MIMEText(message, 'html'))

        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(self.sender_email, self.password) #login with mail_id and password
        text = email.as_string()
        session.sendmail(self.sender_email, self.receiver_email, text)
        session.quit()