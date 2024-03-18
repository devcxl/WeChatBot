import json
import logging

import openai
from openai import RateLimitError

import config
import function
from common.load_balancer import balancer

log = logging.getLogger('text')


def handler_text(content: str, history: []):
    client = balancer.get_next_item()
    messages = [{"role": "system", "content": f'{config.default_prompt}'}]
    for item in history:
        messages.append(item)
    messages.append({"role": "user", "content": content})
    history.append({"role": "user", "content": content})
    try:
        response = client.chat.completions.create(
            model=config.model,
            messages=messages,
            tools=function.function_declares,
            tool_choice="auto"
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = function.available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(function_args)
                messages.append(response_message)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

            second_response = client.chat.completions.create(
                model=config.model,
                messages=messages,
            )
            resp = str(second_response.choices[0].message.content)
            history.append({"role": "assistant", "content": resp})
            return resp
        else:
            resp = str(response.choices[0].message.content)
            history.append({"role": "assistant", "content": resp})
            return resp
    except RateLimitError:
        return '请求过于频繁，请稍后再试。'
    except (openai.InternalServerError, openai.NotFoundError, openai.UnprocessableEntityError):
        return 'OpenAI接口维护中，暂时无法处理消息。请耐心等待稍后再试。'
