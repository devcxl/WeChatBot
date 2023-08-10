from abc import ABC

class BaseCommand(ABC):
    def __init__(self) -> None:
        pass

    def getCommandName() -> str:
        raise NotImplementedError

    def execute(self, user=None, params=None, isGroup=False) -> str:
        raise NotImplementedError



