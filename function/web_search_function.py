import logging

import requests
from requests import HTTPError

from function.base import BaseFunction

log = logging.getLogger('plugin search')


class WebSearchFunction(BaseFunction):

    def __init__(self):
        super().__init__()

    def declare(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "从网络上搜索内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "要搜索的内容",
                        }
                    },
                    "required": ["query"],
                },
            }
        }

    def execute(self, function_args) -> str:
        """Get the current weather in a given location"""
        query = function_args.get("query")
        search_url = f'https://websearch.plugsugar.com/api/plugins/websearch'
        try:
            response = requests.post(search_url, json={"query": query})
            response.raise_for_status()
            data = response.json()
            return data["result"]
        except HTTPError as e:
            return f"获取网络内容失败,原因：{str(e)}"
