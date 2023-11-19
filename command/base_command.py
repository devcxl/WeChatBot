import logging
from abc import ABC

log = logging.getLogger('email')


class BaseCommand(ABC):
    def __init__(self) -> None:
        log.info(f'命令:{self.getCommandName()}加载成功！')
        pass

    def getCommandName(self) -> str:
        raise NotImplementedError

    def execute(self, user=None, params=None, isGroup=False) -> str:
        raise NotImplementedError
