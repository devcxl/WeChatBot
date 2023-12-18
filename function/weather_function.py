import requests
import logging

from function.base import BaseFunction

log = logging.getLogger('weather email')


class WeatherFunction(BaseFunction):

    def __init__(self) -> None:
        super().__init__()

    def declare(self) -> dict:
        return {
            "name": "get_current_weather",
            "description": "获取给定位置的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "位置：城市，县， 例如：北京",
                    }
                },
                "required": ["location"],
            },
        }

    def execute(self, function_args) -> str:
        """Get the current weather in a given location"""
        location = function_args.get("location")
        GDKEY = 'b07a3300faadd38f99f1b10b0f9d9a25'
        weather_resp = requests.get(
            f'https://restapi.amap.com/v3/weather/weatherInfo?key={GDKEY}&city={location}&extensions=all')
        return weather_resp.text
