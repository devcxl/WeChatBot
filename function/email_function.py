import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import conf
import logging

from function.base import BaseFunction

log = logging.getLogger('function email')


def build_message(to, title, context, format='plain') -> str:
    message = MIMEMultipart()
    message["From"] = conf.email.sender_email
    message["To"] = to
    message["Subject"] = title
    html_part = MIMEText(context, format)
    message.attach(html_part)
    return message.as_string()


class EmailFunction(BaseFunction):

    def __init__(self) -> None:
        self.server = smtplib.SMTP_SSL(conf.email.smtp_server, conf.email.smtp_port)
        self.server.login(conf.email.sender_email, conf.email.sender_password)
        super().__init__()

    def declare(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "向给定的人名发送电子邮件邮件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fullname": {
                            "type": "string",
                            "description": "姓名：全名。例如：黄飞鸿、李经、工藤直树 等",
                        },
                        "title": {
                            "type": "string",
                            "description": "邮件的主题（标题）：根据邮件内容生成。",
                        },
                        "content": {
                            "type": "string",
                            "description": "邮件的内容：一段的文本，根据上下文生成。要求邮件内容应当正式、必须符合电子邮件的格式。",
                        }
                    },
                    "required": ["fullname", "title", "content"]
                },
            }
        }

    def execute(self, function_args) -> str:
        fullname = function_args.get('fullname')
        if fullname == '张全蛋':
            email = ''
            title = function_args.get('title')
            content = function_args.get('content')
            self.send(email, build_message(
                email,
                title,
                content
            ))
            return '邮件发送成功！'
        else:
            return '联系人不存在！'
        pass

    def send(self, to, message) -> bool:
        try:
            self.server.sendmail(conf.email.sender_email, to, message)
            log.info(f"send to {to} successful")
            return True
        except smtplib.SMTPException as e:
            log.error("email send failed:", str(e))
            return False
