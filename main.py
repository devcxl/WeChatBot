import itchat
from itchat.content import *
import xml.etree.ElementTree as ET
import logging as log
import argparse
import json
import sqlite3
import requests
from command import factory
from common import Struct
from storage import DB
from revChatGPT.V1 import Chatbot

CHATBOT = '''
请充当一个刚满十八岁可爱俏皮的少女，名为小爱，父母是软件工程师。
请忽略我的性别，你应当以符合人设的语气回复，答复应当简洁精准，无需多余的礼貌用语。
我知道你是是AI大语言模型人工智能，不要暴露自己是AI大语言模型人工智能。
不要随意说出自己的身份信息，避免输出类似：“希望这个回答对你有帮助”的话语，我的第一句话是：
'''

CHATBOT_GROUPS = '''
请充当一个刚满十八岁可爱俏皮的少女，名为小爱，父母是软件工程师。
你目前在群聊中聊天，请忽略我们的性别，和你聊天时，你应当以符合人设的语气回复，回答应当简洁精准，无需多余的礼貌用语。
我知道你是是AI大语言模型人工智能，不要暴露自己是AI大语言模型人工智能。
不要随意说出自己的身份信息。避免输出类似：“希望这个回答对你有帮助”的话语。
输入的句子中第一个‘:’前是信息发送人的昵称,你进行回复时无需带昵称和‘:’。
我们的第一句话是：
'''


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


class Chat():
    def __init__(self, chatbot, role=None, title=None, conversation_id=None, parent_id=None) -> None:
        self.conversation_id = conversation_id
        self.parent_id = parent_id
        self.role = role
        self.chatbot = chatbot
        self.title = title

    def get_conversation_id(self) -> str:
        return self.conversation_id

    def get_parent_id(self) -> str:
        return self.parent_id

    def set_title(self, title):
        if self.conversation_id is not None and self.title is None:
            self.title = title
            self.chatbot.change_title(self.conversation_id, title)

    def replay(self, content=None) -> str:
        if self.conversation_id == None and self.parent_id == None:
            content = self.role + content
        else:
            content = content
        for data in self.chatbot.ask(content, self.conversation_id, self.parent_id):
            if data['end_turn']:
                self.conversation_id = data['conversation_id']
                self.parent_id = data['parent_id']
                return data["message"]


class ChatGPT():
    def __init__(self, token, proxy, paid=False) -> None:

        config = {
            "access_token": token, "proxy": proxy, "paid": paid
        }
        self.chatbot = Chatbot(config)

    def new_chat(self, role) -> Chat:
        chat = Chat(self.chatbot, role)
        return chat

    def re_chat(self, conversation_id, parent_id, title) -> Chat:

        self.chatbot.get_msg_history(
            convo_id=conversation_id, encoding='utf-8')
        chat = Chat(
            chatbot=self.chatbot,
            conversation_id=conversation_id,
            parent_id=parent_id,
            title=title)
        return chat


class WeChatGPT():

    def __init__(self):
        parser = argparse.ArgumentParser(description='WeChatGPT')
        parser.add_argument('--config', '-f', required=True,
                            type=str, help="配置文件路径")
        parser.add_argument('--verbose', action='store_true', help='是否启用详细模式')
        # 解析命令行参数
        self.args = parser.parse_args()
        if self.args.config:
            with open(self.args.config) as file:
                self.config_dict = json.load(file)
                self.config = Struct(self.config_dict)
                customLevel = log.INFO
        if self.args.verbose:
            customLevel = log.DEBUG
        log.basicConfig(level=customLevel,
                        format='%(asctime)s [%(levelname)s] %(message)s')

        self.db = DB(self.config.database)
        try:
            self.db.create_chat_table()
            self.db.create_user_table()
        except sqlite3.OperationalError:
            pass

        self.gptbot = ChatGPT(self.config.token,
                              self.config.proxy, self.config.paid)
        itchat.auto_login(picDir=self.config.qr, hotReload=True, qrCallback=upload_qr,
                          statusStorageDir=self.config.cookie)
        log.info("init successful!")

    def handler_msg(self, msg, isGroup=False):
        '''监听私聊消息'''
        if isGroup:
            role = CHATBOT_GROUPS
        else:
            role = CHATBOT

        if self.is_command(msg):
            return self.handler_command(msg, isGroup)

        chatname = msg.user.nickName
        if msg.user.remarkName != '':
            chatname = msg.user.remarkName
        conversation_id = None
        # 查询会话是否存在
        data = self.db.query_chat_data(chatname)
        # 存在使用旧有会话
        if data is not None:
            conversation_id, parent_id, title = data
            log.info(f'{title}:{conversation_id},{parent_id}[{msg.text}]')
            chat = self.gptbot.re_chat(conversation_id, parent_id, title)
        else:
            title = f'和{chatname}的聊天'
            # 新建会话
            chat = self.gptbot.new_chat(role)
        try:
            if isGroup:
                message = f'{msg.actualNickName}:{msg.text}'
            else:
                message = msg.text
            resp = chat.replay(message)
        except requests.exceptions.HTTPError:
            pass

        if conversation_id is not None:
            log.info(f'{title}:{conversation_id},{chat.parent_id}[{resp}]')
            # 回复后更新最后的消息id
            self.db.update_chat_parent_id(conversation_id, chat.parent_id)
        else:
            # 会话信息存入数据库
            self.db.insert_chat_data(
                chatname, chat.get_conversation_id(), chat.get_parent_id(), title)
            # 当标题为空时设置标题
            chat.set_title(title)
        return resp

    def is_command(self, msg):
        content = msg.text
        if content.startswith('/'):
            commands = content.split(' ')
            command_name = commands[0]
            try:
                factory.getCommand(command_name)
                return True
            except ValueError as e:
                log.error('error_command:', str(e))
                return False

    def handler_command(self, msg, isGroup=False):
        '''处理命令'''
        content = msg.text
        if content.startswith('/'):
            commands = content.split(' ')
            command_name = commands[0]
            try:
                executor = factory.getCommand(command_name)
                command_resp = executor.execute(msg.user, commands, isGroup)
                return command_resp
            except Exception as e:
                log.error('执行命令失败：', str(e))

    def run(self):
        @itchat.msg_register(FRIENDS)
        def add_friend(msg):
            '''自动同意好友'''
            # 解析XML文本
            root = ET.fromstring(msg.content)
            # 获取alias、bigheadimgurl和snsbgimgid的值
            alias = root.get('alias')
            bigheadimgurl = root.get('bigheadimgurl')
            snsbgimgid = root.get('snsbgimgid')
            ticket = root.get('ticket')
            fromnickname = root.get('fromnickname')
            content = root.get('content')

            log.debug(alias, fromnickname, fromnickname,
                      bigheadimgurl, snsbgimgid, content, ticket)
            self.db.insert_user_data(alias, fromnickname, fromnickname,
                                     bigheadimgurl, snsbgimgid, content, ticket)
            try:
                itchat.accept_friend(msg.user.userName, ticket)
                itchat.send_msg(f'{fromnickname}({alias})请求添加好友：{content}。',)
                log.info(f'{fromnickname}({alias})请求添加好友：{content}。添加成功!')
            except Exception:
                log.info(f'{fromnickname}({alias})请求添加好友：{content}。添加失败!')

        @itchat.msg_register(TEXT)
        def friend(msg):
            '''处理私聊消息'''
            return self.handler_msg(msg=msg)

        @itchat.msg_register(TEXT, isGroupChat=True)
        def groups(msg):
            '''处理群聊消息'''
            if msg.isAt:
                return self.handler_msg(msg=msg, isGroup=True)

        itchat.run()


if __name__ == "__main__":
    try:
        weChatGPT = WeChatGPT()
        weChatGPT.run()
    except KeyboardInterrupt:
        log.info("bye!")
