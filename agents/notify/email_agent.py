import smtplib
import os
from email.message import EmailMessage
from agents.base import BaseAgent

class GenericEmailAgent(BaseAgent):
    def run(self, **kwargs):
        sender = kwargs.get("sender")
        recipient = kwargs.get("recipient")
        subject = kwargs.get("subject")
        body = kwargs.get("body")
        password = kwargs.get("password")
        smtp_server = kwargs.get("smtp_server", "smtp.gmail.com")
        smtp_port = kwargs.get("smtp_port", 587)

        if not all([sender, recipient, subject, body, password]):
            return {"status": "error", "details": "Missing required fields."}

        msg = EmailMessage()
        msg.set_content(body.encode("utf-8").decode("utf-8"))  # Normalize body
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_charset("utf-8")

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
            return {"status": "success", "details": f"Email sent to {recipient}"}
        except Exception as e:
            return {"status": "error", "details": str(e)}
