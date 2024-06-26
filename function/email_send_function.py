import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from function.base import BaseFunction
from function.factory import FunctionRegisterError

log = logging.getLogger('plugin email')


class EmailFunction(BaseFunction):

    def __init__(self):
        self.server = os.getenv('PLUGIN_EMAIL_SMTP_SERVER', None)
        self.port: int = os.getenv('PLUGIN_EMAIL_SMTP_PORT', None)
        self.email = os.getenv('PLUGIN_EMAIL_ADDRESS', None)
        self.password = os.getenv('PLUGIN_EMAIL_PASSWORD', None)
        if any(v is None or v == '' for v in
               [self.server, self.port, self.email, self.password]):
            raise FunctionRegisterError("One or more values are empty")

        log.debug(f'server:{self.server},port:{self.port},email:{self.email},password:{self.password}')
        try:
            self.server = smtplib.SMTP_SSL(self.server, self.port)
            self.server.login(self.email, self.password)
            log.info("email login successful")
        except RuntimeError:
            raise FunctionRegisterError('Email login failed!')
        super().__init__()

    def declare(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "向指定的邮箱发送邮件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "电子邮件地址",
                        },
                        "subject": {
                            "type": "string",
                            "description": "电子邮件主题",
                        },
                        "content": {
                            "type": "string",
                            "description": "电子邮件内容",
                        }
                    },
                    "required": ["to", "subject", "content"]
                },
            }
        }

    def execute(self, function_args) -> str:
        to = function_args.get("to")
        subject = function_args.get("subject")
        content = function_args.get("content")
        log.debug(f'function_args->to:{to},subject: {subject}, content:{content}')
        try:
            self.server.sendmail(self.email, to, self.build_message(to, subject, content))
            log.info(f"send to {to} successful")
            return f"邮件发送成功。标题：{subject}, 内容：{content}"
        except smtplib.SMTPException as e:
            log.error("email send failed:", str(e))
            return "邮件发送失败"

    def build_message(self, to, subject, context, format='plain') -> str:
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(context, format))
        return message.as_string()
