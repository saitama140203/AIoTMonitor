import smtplib
from email.message import EmailMessage
from typing import Optional


class MailService:
    def __init__(self):
        self.smtp_server = "smtp.mailmug.net"
        self.smtp_port = 2525
        self.smtp_username = "0rxrksiwen9gsqhq"
        self.smtp_password = "x5om79xx0burz9dl"
        self.sender_email = "aiot-monitor@gmail.com"

    # MailMug SMTP server configuration
    # https://mailmug.net/admin 

    # Email address: heocung2407@gmail.com
    # Password: abc123@@

    def send_reset_password_email(self, to_email: str, new_password: str) -> Optional[str]:
        try:
            msg = EmailMessage()
            msg["Subject"] = "Password Reset Notification - AIOT MONITOR"
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg.set_content(
                f"""Hello,\n\nYour password has been reset.\n\nNew Password: {new_password}\n\nPlease change it after logging in.\n\nQuang Luan,\nError Not Found Team"""
            )

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            return "Email sent successfully"
        except Exception as e:
            return f"Failed to send email: {e}"
