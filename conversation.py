import openai
import json
from functions import function_list, available_functions


class Conversation:

    def __init__(self, prompt, num_of_round, model='gpt-3.5-turbo-0613'):
        self.prompt = prompt
        self.model = model
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({"role": "system", "content": self.prompt})

    def ask(self, question):
        try:
            self.messages.append({"role": "user", "content": question})
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                functions=function_list,
                function_call="auto",
                temperature=0.5,
                max_tokens=2048,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            print(response_message["function_call"]["arguments"])
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )

            self.messages.append(response_message)
            self.messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )
            second_response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
            )

            message = second_response["choices"][0]["message"]['content']
        else:
            message = response["choices"][0]["message"]['content']

        self.messages.append({"role": "assistant", "content": message})

        if len(self.messages) > self.num_of_round * 2 + 1:
            del self.messages[1:3]
        return message
