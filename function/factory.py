import logging

from function.base import BaseFunction

log = logging.getLogger('functions factory')


class FunctionRegisterError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class Functions:
    """函数"""

    def __init__(self) -> None:
        self.functions = []
        self.declares = []
        self.available = {}

    def register(self, function) -> None:
        try:
            self.functions.append(function())
        except FunctionRegisterError as e:
            log.warning(e)

    def all(self) -> list[BaseFunction]:
        return self.functions

    def get_all_declare(self) -> list:
        for function in self.functions:
            self.declares.append(function.declare())
        return self.declares

    def get_all_available(self):
        for function in self.functions:
            self.available[function.declare().get('function').get('name')] = function.execute
        return self.available
