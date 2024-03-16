import logging
import os

import requests

from function.base import BaseFunction
from function.factory import FunctionRegisterError

log = logging.getLogger('plugin weather')


class WeatherFunction(BaseFunction):

    def __init__(self):
        self.key = os.getenv('PLUGIN_WEATHER_KEY', None)
        if self.key is None:
            raise FunctionRegisterError('Not set PLUGIN_WEATHER_KEY')
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
        location = function_args.get("location")

        city_code_url = f'https://restapi.amap.com/v3/geocode/geo?key={self.key}&address={location}'
        city_code_resp = requests.get(city_code_url)
        if city_code_resp.status_code == 200:
            city_data = city_code_resp.json()
            city_code = city_data['geocodes'][0]['adcode']
            weather_info_url = f'https://restapi.amap.com/v3/weather/weatherInfo?key={self.key}&city={city_code}&extensions=all'
            weather_resp = requests.get(weather_info_url)
            if weather_resp.status_code == 200:
                return weather_resp.text

        return '获取天气信息失败'
