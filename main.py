import logging
import xml.etree.ElementTree as ET

import itchat
import openai

from common.load_balancer import balancer
from itchat.content import *

import config
from handler.text import handler_text

log = logging.getLogger('main')


class WeChatGPT:

    def __init__(self):
        itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='cookie.ipkl')
        self.history = {}
        if config.conf.openai.api_base:
            openai.api_base = config.conf.openai.api_base

        if config.conf.openai.proxy:
            openai.proxy = config.conf.openai.proxy

        log.info("init successful!")

    def run(self):
        @itchat.msg_register(FRIENDS)
        def add_friend(msg):
            """自动同意好友"""
            # 解析XML文本
            root = ET.fromstring(msg.content)

            realwxid = root.get('fromusername')
            wechat_id = root.get('alias')
            head_img = root.get('bigheadimgurl')
            bg_img = root.get('snsbgimgid')
            nick_name = root.get('fromnickname')
            content = root.get('content')

            ticket = root.get('ticket')
            itchat.accept_friend(msg.user.userName, ticket)

        @itchat.msg_register(TEXT)
        def friend(msg):
            """处理私聊消息"""
            self.history.setdefault(msg.user.userName, [])
            history = self.history[msg.user.userName]
            need_remove_len = len(history) - config.conf.openai.history
            if need_remove_len > 0:
                for i in range(need_remove_len):
                    history.pop(0)

            return handler_text(content=msg.text, history=history)

        @itchat.msg_register(VOICE)
        def friend(msg):
            """处理私聊消息"""
            self.history.setdefault(msg.user.userName, [])
            history = self.history[msg.user.userName]
            need_remove_len = len(history) - config.conf.openai.history
            if need_remove_len > 0:
                for i in range(need_remove_len):
                    history.pop(0)

            msg.download(msg.fileName)
            audio_file = open(msg.fileName, "rb")
            client = balancer.get_next_item()
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            content = transcript.text
            return handler_text(content=content, history=history)

        @itchat.msg_register(TEXT, isGroupChat=True)
        def groups(msg):
            """处理群聊消息"""
            if msg.isAt:
                self.history.setdefault(msg.user.userName, [])
                history = self.history[msg.user.userName]
                need_remove_len = len(history) - config.conf.openai.history
                if need_remove_len > 0:
                    for i in range(need_remove_len):
                        history.pop(0)
                return handler_text(msg.text, history=history)

        itchat.run()


if __name__ == "__main__":
    try:
        weChatGPT = WeChatGPT()
        weChatGPT.run()
    except KeyboardInterrupt:
        log.info("bye!")
