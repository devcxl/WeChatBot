import argparse
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
    history: int = Field(description='历史记录轮次')
    proxy: str = Field(description='http代理', default='')


class Setting(BaseModel):
    """配置类"""

    log: LogSetting = Field(description='Log Setting')

    openai: OpenAISetting = Field(description='OpenAI Setting')


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
