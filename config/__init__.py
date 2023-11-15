import argparse
import logging

import json
import yaml
from pydantic import BaseModel, Field

log = logging.getLogger('config')


class LogSetting(BaseModel):
    log_file: str = Field(
        default='./app.log', description='日志文件保存地址'
    )
    level: str = Field(
        default='INFO', description='日志等级'
    )


class OpenAISetting(BaseModel):
    """OpenAI的配置"""
    api_base: str = Field(description='OpenAI接口的地址')
    api_key: str = Field(description='OpenAI的API_KEY')
    model: str = Field(description='GPT模型')
    default_prompt: str = Field(description='默认提示词')
    proxy: str = Field(description='http代理')


class EmailSetting(BaseModel):
    """电子邮件配置"""
    smtp_server: str = Field(description="SMTP发送服务器")
    # 一般为587或者465
    smtp_port: int = Field(description="SMTP发送服务器端口号")
    # 发件人的邮箱和密码
    sender_email: str = Field(description="SMTP发件人")
    sender_password: str = Field(description="SMTP密码")


class MeiliSearchSetting(BaseModel):
    search_host: str = Field(
        default='http://127.0.0.1:7700', description='搜索引擎访问地址'
    )
    search_key: str = Field(
        description='搜索引擎访问Key'
    )
    search_index: str = Field(
        description='搜索索引名称'
    )


class Setting(BaseModel):
    """配置类"""

    log: LogSetting = Field(description='Log Setting')

    openai: OpenAISetting = Field(description='OpenAI Setting')

    email: EmailSetting = Field(description="Email setting")

    database: str = Field(
        default='sqlite:///./pipimeme.sqlite', description='数据库，支持SQLite、MySQL'
    )
    verbose: bool = Field(
        default=False, description="显示DEBUG日志"
    )


def load_config(config_file: str, format: str):
    """加载配置文件"""
    log.info(f'加载配置文件:{config_file}')
    if config_file:
        with open(config_file) as file:
            if format == 'json':
                return Setting.model_validate_json(file.read(), strict=True)
            elif format == 'yaml':
                config_data = yaml.safe_load(file.read())
                json_data = json.dumps(config_data)
                return Setting.model_validate_json(json_data, strict=True)


parser = argparse.ArgumentParser(description='Pipimeme')
parser.add_argument('--config', '-f', required=True,
                    type=str, help="配置文件路径")
parser.add_argument('--format', '-t', default='json',
                    type=str, help="配置文件格式化类型。可选：json（默认），yaml")
args = parser.parse_args()

conf = load_config(args.config, args.format)
