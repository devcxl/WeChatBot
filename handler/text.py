import json
import logging
import time

import openai
from sqlalchemy import desc, func
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

            messages_from_db = db.query(Message).filter(Message.user_id == current_user.id).order_by(
                desc(Message.timestamp)).limit(10).all()
            messages = [{"role": "system", "content": f'{current_user.default_prompt}\n- Please remember my name: {current_user.user_name}'}]

            for message in messages_from_db:
                if message.replay:
                    messages.append({
                        "role": "assistant",
                        "content": message.content
                    })
                else:
                    messages.append({
                        "role": "user",
                        "content": message.content
                    })

            messages.append({"role": "user", "content": content})
            try:
                response = openai.ChatCompletion.create(
                    model=config.conf.openai.model,
                    messages=messages,
                    functions=functions.function_list,
                    function_call="auto",
                )

                response_message = response["choices"][0]["message"]

                print(response_message)

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

                    resp = str(second_response["choices"][0]["message"]['content'])
                    return resp
                else:
                    resp = str(response["choices"][0]["message"]['content'])
                    presave = Message(type='text', content=content, timestamp=func.now(), user_id=user_id)
                    db.add(presave)
                    db.commit()
                    db.refresh(presave)

                    msg = Message(type='text', content=resp, timestamp=func.now(), user_id=user_id,
                                  replay=True)
                    db.add(msg)
                    db.commit()
                    db.refresh(msg)
                    db.close()
                    return resp

            except openai.error.RateLimitError as e:
                return '请求限制，每分钟3次'
