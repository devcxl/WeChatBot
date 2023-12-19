import argparse
import logging
from typing import List
import json
import yaml
from pydantic import BaseModel, Field


class LogSetting(BaseModel):
    file: str = Field(
        default=None, description='日志文件保存地址'
    )
    verbose: bool = Field(
        default=False, description="显示DEBUG日志"
    )


class OpenAISetting(BaseModel):
    """OpenAI的配置"""
    api_base: str = Field(description='OpenAI接口的地址', default='')
    # api_key: str = Field(description='OpenAI的API_KEY')
    api_keys: List[str] = Field(description='OpenAI的API_KEY列表')
    model: str = Field(description='GPT模型')
    default_prompt: str = Field(description='默认提示词')
    proxy: str = Field(description='http代理', default='')


class EmailSetting(BaseModel):
    """电子邮件配置"""
    smtp_server: str = Field(description="SMTP发送服务器")
    # 一般为587或者465
    smtp_port: int = Field(description="SMTP发送服务器端口号")
    # 发件人的邮箱和密码
    sender_email: str = Field(description="SMTP发件人")
    sender_password: str = Field(description="SMTP密码")


class AmapSetting(BaseModel):
    """高德配置"""
    key: str = Field(description="高德天气预报KEY")


class Setting(BaseModel):
    """配置类"""

    log: LogSetting = Field(description='Log Setting')

    openai: OpenAISetting = Field(description='OpenAI Setting')

    email: EmailSetting = Field(description="Email setting")

    amap: AmapSetting = Field(description="Amap setting")

    voice_path: str = Field(description='语音文件保存路径')

    database: str = Field(
        default='sqlite:///./pipimeme.sqlite', description='数据库，支持SQLite、MySQL'
    )


def load_config(config_file: str):
    """加载配置文件"""
    if config_file:
        with open(config_file) as file:
            config_data = yaml.safe_load(file.read())
            json_data = json.dumps(config_data)
            return Setting.model_validate_json(json_data, strict=True)


parser = argparse.ArgumentParser(description='Pipimeme')
parser.add_argument('--config', '-f', required=True,
                    type=str, help="配置文件路径")
args = parser.parse_args()

conf = load_config(args.config)
