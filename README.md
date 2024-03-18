# WeChatBot

WeChatBot是一款基于ItChat-UOS的微信聊天机器人，可以将你的微信小号快速接入OpenAI。

* 支持OpenAI的多个Api-Key轮询使用
* 支持OpenAI的Function call
* 支持Whisper语音识别

> 注意！！！
> - 使用该项目微信账号有被封禁的风险，请使用小号登陆。
> - 建议不要给太多人高频率使用，可能会导致账号被封禁。

## 部署

### Docker

```shell
docker run -d --name wechatbot \
-e TZ=Asia/Shanghai \
-e OPENAI_API_URL=https://your.proxy.domain.com/v1 \
-e OPENAI_API_KEYS=sk-xxxxxxxxxxxxxxxxxxxxxxxx,sk-xxxxxxxxxxxxxxxxxxxxxxxx \
ghcr.io/devcxl/wechatbot:latest
```

### docker-compose

```yaml
version: '3.9'
services:
    wechatbot:
        image: ghcr.io/devcxl/wechatbot:latest
        container_name: wechatbot
        environment:
            - TZ=Asia/Shanghai
            - OPENAI_API_URL=https://your.proxy.domain.com/v1
            - OPENAI_API_KEYS=sk-xxxxxxxxxxxxxxxxxxxxxxxx,sk-xxxxxxxxxxxxxxxxxxxxxxxx
        volumes:
            - ${PWD}/data/:/data
        restart: unless-stopped
```

### 登陆微信

查看`wechatbot`的日志

`docker logs wechatbot --tail 200 -f`

扫码登陆即可。

> 注意！！！
> - 无法登陆的情况建议给小号绑上银行卡再试。

## 环境变量

| KEY                | REQUIRE | DEFAULT                      | DETAIL                                 |
|--------------------|---------|------------------------------|----------------------------------------|
| OPENAI_API_URL     | No      | https://api.openai.com/v1    | OpenAI的接口                              |
| OPENAI_API_KEYS    | Yes     | None                         | OpenAI的APIKey,使用`,`分割                  |
| MODEL              | No      | gpt-3.5-turbo                | 对话使用的模型(建议使用带Function Call功能的模型)       |
| DEFAULT_PROMPT     | No      | You are a helpful assistant. | 默认提示词                                  |
| HISTORY            | No      | 15                           | 历史消息数                                  |
| DATA_DIR           | No      | /data                        | 数据文件夹                                  |
| OPENAI_PROXY       | Yes     | None                         | 请求OpenAI的代理(eg: http://127.0.0.1:8889) |
| PLUGIN_WEATHER_KEY | No      | None                         | 高德地图的APIKey                            |

## 聊天指令

| 指令      | 功能         | 示例                                    |
|---------|------------|---------------------------------------|
| /clear  | 清理聊天历史     | `/clear`                              |
| /prompt | 设置当前聊天的提示词 | `/prompt 请你充当一个专业的心理医生，请根据以下症状判断我的病症` |

## FunctionCall插件

| 名称      | 环境变量               | 功能             | 使用示例              |
|---------|--------------------|----------------|-------------------|
| Weather | PLUGIN_WEATHER_KEY | 获取给定位置未来几天内的天气 | 明天上海天气怎么样，适合穿什么衣服 |

## 贡献FunctionCall插件

fork本项目，仿照`weather_function.py`创建自己想实现的功能开发即可

````python
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

````

然后在`function`包下的`__init__.py`中仿照`WeatherFunction`进行注册

```python
functions.register(WeatherFunction)
```

## 相关项目

- https://github.com/littlecodersh/ItChat
- https://github.com/why2lyj/ItChat-UOS