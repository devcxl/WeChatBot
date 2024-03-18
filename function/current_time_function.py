from datetime import datetime

from function.base import BaseFunction


class CurrentTimeFunction(BaseFunction):

    def __init__(self):
        super().__init__()

    def declare(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "获取当前时间",
                "parameters": {},
            }
        }

    def execute(self, function_args) -> str:
        """获取当前时间"""
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_now
