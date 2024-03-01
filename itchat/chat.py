from itchat.message import Message


class Chat:

    @property
    def id(self):
        pass

    @property
    def name(self):
        for attr in 'remark_name', 'display_name', 'nick_name', 'wxid':
            _name = getattr(self, attr, None)
            if _name:
                return _name

    def send(self, message: Message):
        # 实现发送消息的逻辑
        pass

    def revoke(self, message: Message):
        pass

    def receive(self, message: Message):
        # 实现接收消息的逻辑
        pass


class SingleChat(Chat):
    """
    私聊
    """
    pass


class GroupChat(Chat):
    """
    群聊
    """
    pass
