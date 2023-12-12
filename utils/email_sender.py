import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import conf
import logging

log = logging.getLogger('email')

server = smtplib.SMTP_SSL(conf.email.smtp_server, conf.email.smtp_port)
server.login(conf.email.sender_email, conf.email.sender_password)
log.info("email login successful")


def build_message(to, title, context, format='plain') -> str:
    message = MIMEMultipart()
    message["From"] = conf.email.sender_email
    message["To"] = to
    message["Subject"] = title
    html_part = MIMEText(context, format)
    message.attach(html_part)
    return message.as_string()


def send(to, message) -> bool:
    try:
        server.sendmail(conf.email.sender_email, to, message)
        log.info(f"send to {to} successful")
        return True
    except smtplib.SMTPException as e:
        log.error("email send failed:", str(e))
        return False
