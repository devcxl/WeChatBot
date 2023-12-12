import requests

from command.tts_command import TTSCommand
from utils import email_sender


def get_current_weather(function_args):
    """Get the current weather in a given location"""
    location = function_args.get("location")
    GDKEY = 'b07a3300faadd38f99f1b10b0f9d9a25'
    weather_resp = requests.get(
        f'https://restapi.amap.com/v3/weather/weatherInfo?key={GDKEY}&city={location}&extensions=all')
    return weather_resp.text


def generate_voice(function_args):
    content = function_args.get('content')
    tts = TTSCommand()
    return tts.azure_tts(content)


def send_email(function_args):
    fullname = function_args.get('fullname')
    if fullname == '张全蛋':
        email = ''
        title = function_args.get('title')
        content = function_args.get('content')
        email_sender.send(email, email_sender.build_message(
            email,
            title,
            content
        ))
    return '邮件发送成功！'


function_list = [
    {
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
    },
    {
        "name": "generate_voice",
        "description": "生成给定内容的语音文件",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "内容：一段文本。一个短句 例如：今天天气真好，我们一起去玩吧。",
                }
            },
            "required": ["content"],
        },
    },
    {
        "name": "send_email",
        "description": "向给定的人名发送电子邮件邮件",
        "parameters": {
            "type": "object",
            "properties": {
                "fullname": {
                    "type": "string",
                    "description": "姓名：全名。例如：黄飞鸿、李经、工藤直树 等",
                },
                "title": {
                    "type": "string",
                    "description": "邮件的主题（标题）：根据邮件内容生成。",
                },
                "content": {
                    "type": "string",
                    "description": "邮件的内容：一段的文本，根据上下文生成。要求邮件内容应当正式、必须符合电子邮件的格式。",
                }
            },
            "required": ["fullname", "title", "content"]
        },
    }

]

available_functions = {
    'get_current_weather': get_current_weather,
    'generate_voice': generate_voice,
    'send_email': send_email,
}
