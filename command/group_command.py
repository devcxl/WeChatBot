
import itchat
from .base_command import BaseCommand


class GroupCommand(BaseCommand):
    '''群组'''

    def __init__(self) -> None:
        super().__init__()

    def getCommandName(self):
        return '/group'

    def execute(self, user=None, params=None, isGroup=False):
        resp = ''
        chatrooms = itchat.get_chatrooms(True)
        for c in chatrooms:
            resp += f'{c.NickName}\n'
        return resp