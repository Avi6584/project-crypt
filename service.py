import smtplib
from email.message import EmailMessage
from fastapi import HTTPException

class MailService:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_mail(self, from_mail: str, to_mail: str, subject: str, body: str):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_mail
        msg['To'] = to_mail

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return {"error": False, "message": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")