import argparse
import json
import logging
import sqlite3
import xml.etree.ElementTree as ET

import itchat
import openai
import requests
from itchat.content import *

from command import factory
from common import Struct, Logger
from storage import ChatGPTChat, Message, Model, SQLiteDB, WeChatUser
from functions import get_current_weather, function_list,available_functions

log = Logger('wechatbot')


def upload_image_bytes(bytes):
    try:
        files = {'smfile': bytes}
        url = 'https://smms.app/api/v2/upload'
        headers = {'Authorization': 'n5aRWU7BNLzK8fqyrXXOLXemSlQOm5tX'}
        res = requests.post(
            url, files=files, headers=headers).json()
        if res['success']:
            return res['data']['url']
        else:
            raise Exception(res['message'])
    except Exception as e:
        print(e)


def upload_qr(uuid, status, qrcode):
    url = upload_image_bytes(qrcode)
    log.info(f'loginURL:{url}')


class WeChatGPT:

    def __init__(self):
        parser = argparse.ArgumentParser(description='WeChatGPT')
        parser.add_argument('--config', '-f', required=True,
                            type=str, help="配置文件路径")
        parser.add_argument('--verbose', '-v',
                            action='store_true', help='是否启用详细模式')
        # 解析命令行参数
        self.args = parser.parse_args()
        if self.args.config:
            with open(self.args.config) as file:
                self.config_dict = json.load(file)
                self.config = Struct(self.config_dict)
                custom_level = logging.INFO
        if self.args.verbose:
            custom_level = logging.DEBUG
        log = Logger(name=self.__class__.__name__, level=custom_level)

        self.db = SQLiteDB(self.config.database)
        Model.initialize(self.db)
        try:
            ChatGPTChat.create_table()
            WeChatUser.create_table()
            Message.create_table()
        except sqlite3.OperationalError as e:
            print(e)
            pass

        openai.proxy = {"http": self.config.proxy, "https": self.config.proxy}
        openai.api_key = self.config.token
        self.functions = function_list
        itchat.auto_login(picDir=self.config.qr, hotReload=True, qrCallback=upload_qr,
                          statusStorageDir=self.config.cookie)
        log.info("init successful!")

    def is_command(self, msg):
        """判断是否为命令"""
        content = msg.text
        if content.startswith('/'):
            commands = content.split(' ')
            command_name = commands[0]
            try:
                factory.getCommand(command_name)
                return True
            except ValueError as e:
                log.error(f'error_command:{str(e)}', )
                return False

    def handler_command(self, msg, isGroup=False):
        """处理命令"""
        content = msg.text
        if content.startswith('/'):
            commands = content.split(' ')
            command_name = commands[0]
            try:
                executor = factory.getCommand(command_name)
                command_resp = executor.execute(msg.user, commands, isGroup)
                return command_resp
            except Exception as e:
                log.error(f'执行命令失败：{str(e)}')

    def handler_msg(self, msg):
        """处理消息"""

        # 已经处理过的消息不进行处理
        flag = Message.fetch_one(f'msg_id=?', (msg.MsgId,))
        if flag is not None:
            return

        message = Message()
        message.context = msg.text
        message.msg_id = msg.MsgId
        message.fromUserName = msg.user.NickName
        message.toUserName = "ME"
        message.save()

        if self.is_command(msg):
            return self.handler_command(msg)

        messages = [{"role": "system", "content": self.config.defaultRole}, {"role": "user", "content": msg.text}]
        try:
            response = openai.ChatCompletion.create(
                model=self.config.model,
                messages=messages,
                functions=self.functions,
                function_call="auto",
            )
            response_message = response["choices"][0]["message"]
            if response_message.get("function_call"):
                function_name = response_message["function_call"]["name"]
                function_to_call = available_functions[function_name]
                function_args = json.loads(response_message["function_call"]["arguments"])
                log.info(f'func:{function_name},args:{function_args}')
                function_response = function_to_call(function_args)
                messages.append(response_message)
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                second_response = openai.ChatCompletion.create(
                    model=self.config.model,
                    messages=messages,
                )
                return str(second_response["choices"][0]["message"]['content'])
            else:
                return str(response["choices"][0]["message"]['content'])
        except openai.error.RateLimitError as e:
            return '请求限制，每分钟3次'

    def run(self):
        @itchat.msg_register(FRIENDS)
        def add_friend(msg):
            """自动同意好友"""
            # 解析XML文本
            root = ET.fromstring(msg.content)
            # 获取alias、bigheadimgurl和snsbgimgid的值
            wechat_id = root.get('alias')
            head_img = root.get('bigheadimgurl')
            bg_img = root.get('snsbgimgid')
            ticket = root.get('ticket')
            nick_name = root.get('fromnickname')
            content = root.get('content')
            # itchat.accept_friend(msg.user.userName, ticket)
            log.info(f'{nick_name}({wechat_id})请求添加好友：{content}')

        @itchat.msg_register(TEXT)
        def friend(msg):
            """处理私聊消息"""
            return self.handler_msg(msg)

        @itchat.msg_register(TEXT, isGroupChat=True)
        def groups(msg):
            """处理群聊消息"""
            if msg.isAt:
                return self.handler_msg(msg)

        itchat.run()


if __name__ == "__main__":
    try:
        weChatGPT = WeChatGPT()
        weChatGPT.run()
    except KeyboardInterrupt:
        log.info("bye!")
