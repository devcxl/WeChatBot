import json
import logging

import openai
from sqlalchemy.orm import Session

import config
import functions
from database import SessionLocal
from database.domain import Message, User

log = logging.getLogger('text')


def handler_text(msg_id: str, user_id: int, content: str):
    db: Session = SessionLocal()
    message: Message = db.query(Message).filter(Message.id == msg_id).first()
    if message:
        log.debug('存在当前MessageId,重复消息，无需处理')
        return
    else:
        current_user: User = db.query(User).filter(User.id == user_id).first()
        if current_user:
            messages = [{"role": "system", "content": current_user.default_prompt},
                        {"role": "user", "content": content}]

            try:
                response = openai.ChatCompletion.create(
                    model=config.conf.openai.model,
                    messages=messages,
                    functions=functions.function_list,
                    function_call="auto",
                )

                response_message = response["choices"][0]["message"]

                if response_message.get("function_call"):
                    function_name = response_message["function_call"]["name"]
                    function_to_call = functions.available_functions[function_name]
                    function_args = json.loads(response_message["function_call"]["arguments"])
                    log.info(f'func:{function_name},args:{function_args}')
                    function_response = function_to_call(function_args)
                    messages.append(response_message)
                    messages.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                    second_response = openai.ChatCompletion.create(
                        model=config.conf.openai.model,
                        messages=messages,
                    )
                    return str(second_response["choices"][0]["message"]['content'])
                else:
                    return str(response["choices"][0]["message"]['content'])

            except openai.error.RateLimitError as e:
                return '请求限制，每分钟3次'

