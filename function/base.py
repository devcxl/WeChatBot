import logging
from abc import ABC

log = logging.getLogger('function base')


class BaseFunction(ABC):
    def __init__(self) -> None:
        log.info(f'函数:{self.declare().get("name")}加载成功！')

    def declare(self) -> dict:
        """GPT函数定义"""
        raise NotImplementedError

    def execute(self, function_args) -> str:
        """GPT执行函数"""
        raise NotImplementedError
