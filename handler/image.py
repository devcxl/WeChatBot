import base64
import logging

import openai
from openai import RateLimitError

import config
from common.load_balancer import balancer

log = logging.getLogger('image')


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        base64_string = base64.b64encode(img_file.read()).decode('utf-8')
    return base64_string


def handler_image(image_paths: list[str], content: str, prompt=config.default_prompt):
    if config.model is not 'gpt-4-vision-preview':
        return '当前模型不支持图像识别'

    client = balancer.get_next_item()

    contents = []

    contents.append({
        "type": "text",
        "text": content
    })

    for path in image_paths:
        contents.append({
            "type": "image_url",
            "image_url": {
                "url", f"data:image/jpeg;base64,{image_to_base64(path)}",
            },
        })

    messages = [
        {"role": "system", "content": f'{prompt}'},
        {"role": "user", "content": contents}]

    try:
        response = client.chat.completions.create(
            model=config.model,
            messages=messages
        )
        return response.choices[0].message.content
    except RateLimitError:
        return '请求过于频繁，请稍后再试。'
    except (openai.InternalServerError, openai.NotFoundError, openai.UnprocessableEntityError):
        return 'OpenAI接口维护中，暂时无法处理消息。请耐心等待稍后再试。'
