import logging
import os
import signal
import sys
import time
import xml.etree.ElementTree as ET
import base64
import openai
import requests

import config
import itchat
from common.load_balancer import balancer
from handler.text import handler_text
from itchat.content import *

log = logging.getLogger('main')


def stop_program(signal, frame):
    log.info('WeChatbot Closing Save some data')
    itchat.dump_login_status()
    sys.exit(0)


signal.signal(signal.SIGTERM, stop_program)


class WeChatGPT:

    def __init__(self):
        itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir=os.path.join(config.data_dirs, 'cookie.bin'))

        self.history = {}
        self.prompts = {}
        if config.api_url:
            openai.api_base = config.api_url

        if config.proxy:
            openai.proxy = config.proxy
        os.makedirs(os.path.join(config.data_dirs, 'voices'), exist_ok=True)
        log.debug(config.default_prompt)
        log.info("init successful!")

    def handler_history(self, msg):
        self.history.setdefault(msg.user.userName, [])
        history = self.history[msg.user.userName]
        need_remove_len = len(history) - config.history
        if need_remove_len > 0:
            for i in range(need_remove_len):
                history.pop(0)
        log.debug(history)
        return history

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
            try:
                current_chat_prompt = self.prompts[msg.user.userName]
            except KeyError:
                current_chat_prompt = config.default_prompt
            return handler_text(content=msg.text, history=self.handler_history(msg), prompt=current_chat_prompt)

        @itchat.msg_register(VOICE)
        def friend(msg):
            """处理私聊消息"""
            try:
                current_chat_prompt = self.prompts[msg.user.userName]
            except KeyError:
                current_chat_prompt = config.default_prompt
            filepath = os.path.join(config.data_dirs, 'voices', msg.fileName)
            msg.download(filepath)
            audio_file = open(filepath, "rb")
            client = balancer.get_next_item()
            try:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                content = transcript.text
                return handler_text(content=content, history=self.handler_history(msg), prompt=current_chat_prompt)
            except openai.InternalServerError as e:
                return '暂时无法处理语音消息'

        @itchat.msg_register(TEXT, isGroupChat=True)
        def groups(msg):
            """处理群聊消息"""
            if msg.isAt:
                return handler_text(msg.text, history=self.handler_history(msg))

        @itchat.command(name='/clear', detail='清理聊天上下文', friend=True, group=True)
        def command_clean(message, user):
            try:
                self.history[user.userName].clear()
                return '清理完毕！'
            except KeyError:
                return '不存在消息记录，无需清理'

        @itchat.command(name='/prompt', detail='设置当前私聊的提示词', friend=True, group=False)
        def command_prompt(message, user):
            self.prompts[user.userName] = message
            return '设置成功！开始对话吧！'

        @itchat.command(name='/imagine', detail='使用DALL-E-3生成图像', friend=True, group=False)
        def command_clean(message, user):
            bytes_to_encode = ",".join(message).encode('utf-8')
            base64_bytes = base64.b64encode(bytes_to_encode)
            encoded_text = base64_bytes.decode('utf-8')
            filename = f'{encoded_text}.jpg'
            filepath = os.path.join(config.data_dirs, 'dall-e-3', filename)
            if os.path.exists(filepath):
                return f'@img@{filepath}'

            client = balancer.get_next_item()
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=message,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = response.data[0].url
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    return f'@img@{filepath}'
                else:
                    return '获取图像失败，请稍后重新再试'
            except (openai.InternalServerError, openai.NotFoundError, openai.UnprocessableEntityError):
                return 'OpenAI接口维护中，暂时无法处理画图命令。请耐心等待稍后再试'

        itchat.run()


if __name__ == "__main__":
    try:
        weChatGPT = WeChatGPT()
        weChatGPT.run()
    except KeyboardInterrupt:
        log.info("bye!")
