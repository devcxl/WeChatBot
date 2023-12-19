import requests
import logging

from function.base import BaseFunction

log = logging.getLogger('weather')


class WeatherFunction(BaseFunction):

    def __init__(self) -> None:
        super().__init__()

    def declare(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "获取给定位置的天气预报",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市或区县，例如北京市",
                        },
                        "unit": {"type": "string", "enum": ["摄氏", "华氏"]},
                    },
                    "required": ["location"],
                },
            }
        }

    def execute(self, function_args) -> str:
        """Get the current weather in a given location"""
        log.debug(f'参数：{function_args}')
        location = function_args.get("location")
        GDKEY = 'b07a3300faadd38f99f1b10b0f9d9a25'
        resp = requests.get(
            f'https://restapi.amap.com/v3/weather/weatherInfo?key={GDKEY}&city={location}&extensions=all')

        response = resp.text
        log.debug(f'返回结果:{response}')
        return response
