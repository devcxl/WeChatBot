from abc import ABC
from common import Logger

log = Logger('wechatbot')


class BaseCommand(ABC):
    def __init__(self) -> None:
        log.info(f'命令:{self.getCommandName()}加载成功！')
        pass

    def getCommandName(self) -> str:
        raise NotImplementedError

    def execute(self, user=None, params=None, isGroup=False) -> str:
        raise NotImplementedError
