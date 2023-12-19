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
        itchat.auto_login(picDir='./qr.png', hotReload=True,
                          statusStorageDir='./tmp.ipkl')

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
            # print(msg.content)
            root = ET.fromstring(msg.content)
            # 获取alias、bigheadimgurl和snsbgimgid的值
            wechat_id = root.get('alias')
            head_img = root.get('bigheadimgurl')
            bg_img = root.get('snsbgimgid')
            ticket = root.get('ticket')
            nick_name = root.get('fromnickname')
            content = root.get('content')
            # itchat.accept_friend(msg.user.userName, ticket)
            user = itchat.search_friends(remarkName='u155')[0]
            itchat.send_msg(f'{nick_name}({wechat_id})请求添加好友：{content}', user.userName)
            log.info(f'{nick_name}({wechat_id})请求添加好友：{content}')
            msg.user.verify()

        @itchat.msg_register(TEXT)
        def friend(msg):
            """处理私聊消息"""
            tmp_uid: str = msg.user.RemarkName
            content: str = msg.text
            user_id = int(tmp_uid.replace('u', ''))
            return handler_text(msg_id=msg.MsgId, user_id=user_id, content=content)

        @itchat.msg_register(VOICE)
        def friend(msg):
            """处理私聊消息"""
            msg.download(msg.fileName)
            tmp_uid: str = msg.user.RemarkName
            user_id = int(tmp_uid.replace('u', ''))
            audio_file = open(msg.fileName, "rb")
            client = balancer.get_next_item()
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            content = transcript.text
            return handler_text(msg_id=msg.MsgId, user_id=user_id, content=content)

        # @itchat.msg_register(TEXT, isGroupChat=True)
        # def groups(msg):
        #     """处理群聊消息"""
        #     if msg.isAt:
        #         return self.handler_msg(msg)

        itchat.run()


if __name__ == "__main__":
    try:
        weChatGPT = WeChatGPT()
        weChatGPT.run()
    except KeyboardInterrupt:
        log.info("bye!")
