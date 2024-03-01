from abc import ABC
from datetime import datetime

from itchat.contact import SingleContact


class Message(ABC):

    def __init__(self, raw):
        self.raw = raw
        self._receive_time = datetime.now()

    @property
    def id(self):
        """
        消息的唯一 ID (通常为大于 0 的 64 位整型)
        """
        return self.raw.get('NewMsgId')

    @property
    def type(self):
        return self.raw.get('Type')

    @property
    def sender(self) -> SingleContact:
        """
        消息的发送者
        """
        return self._get_chat_by_user_name(self.raw.get('FromUserName'))

    @property
    def receiver(self):
        """
        消息的接收者
        """
        return self._get_chat_by_user_name(self.raw.get('ToUserName'))

    @property
    def create_time(self):
        """
        服务端发送时间
        """
        try:
            return datetime.fromtimestamp(self.raw.get('CreateTime'))
        except:
            pass

    @property
    def receive_time(self):
        """
        本地接收时间
        """
        return self._receive_time

    @property
    def latency(self):
        """
        消息的延迟秒数 (发送时间和接收时间的差值)
        """
        create_time = self.create_time
        if create_time:
            return (self.receive_time - create_time).total_seconds()


class TextMessage(Message):
    """
    文本消息
    """

    def __init__(self, raw):
        super().__init__(raw)

    @property
    def text(self):
        return self.raw.get('Content')


class VoiceMessage(Message):
    """
    语音消息
    """

    def __init__(self, raw):
        super().__init__(raw)

    @property
    def voice_length(self) -> int:
        """
        语音长度
        """
        return self.raw.get('VoiceLength')

