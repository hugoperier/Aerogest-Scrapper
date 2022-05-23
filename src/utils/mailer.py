import smtplib, ssl

class Mailer:
    def __init__(self, config):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = config.get("SENDER_EMAIL")
        self.password = config.get("SENDER_PASSWORD")
        self.receiver_email = config.get("RECEIVER_EMAIL")
        self.message = """\
        Subject: Hi there
        """


    def send_email(self, receiver_email, message):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.sender_email, self.password)
            fullMessage = self.message + message
            server.sendmail(self.sender_email, receiver_email, fullMessage)