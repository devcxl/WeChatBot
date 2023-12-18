from function.base import BaseFunction


class Functions:
    """函数"""

    def __init__(self) -> None:
        self.functions = []
        self.declares = []
        self.available = {}

    def register(self, function: BaseFunction) -> None:
        self.functions.append(function)

    def all(self) -> list[BaseFunction]:
        return self.functions

    def get_all_declare(self) -> list:
        for function in self.functions:
            self.declares.append(function.declare())
        return self.declares

    def get_all_available(self):
        for function in self.functions:
            self.available[function.declare().get('name')] = function.execute
        return self.available
