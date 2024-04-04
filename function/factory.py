import logging

from function.base import BaseFunction
from function.error import PluginUnregisteredException, PlugInExecutionException

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

    def get(self, function_name):
        for function in self.functions:
            if function_name == function.declare().get('function').get('name'):
                return function.execute
        raise PluginUnregisteredException(function_name)

    def execute(self, function, function_args):
        try:
            return function(function_args)
        except Exception as e:
            raise PlugInExecutionException(e)
