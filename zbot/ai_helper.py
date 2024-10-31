import json
from telegram import Update
from openai import OpenAI
from .config import OPENAI_API_KEY
import logging
from . import utils
from . import blockchain
from . import executor

MODEL = "gpt-4o"
MAX_DEPTH = 8
SHORT_TERM_MEMORY_DEPTH=32

class AIHelper:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.functions = executor.get_functions()
        self.short_term_memory = []
        self.long_term_memory = []
        self.basic_messages =[
                {"role": "system", "content": "You are a helpful assistant specializing in blockchain technology."},
                {"role": "system", "content": "You are connected to the Zilliqa 2 prototestnet, a high performance EVM-compatible blockchain network. The native token is called Zil."},
                {"role": "system", "content": "Function results are a pair of result, error."},
            ];


    def remember(self, value):
        self.long_term_memory.append(value)

    def maybe_remember(self, candidate: str) -> bool:
        messages = self.basic_messages + [
            { "role": "system", "content": "Would it be useful to remember this information? Answer yes or no only"},
            { "role" : "user", "content": candidate }
        ]
        response = self.client.chat.completions.create(
            model = MODEL,
            messages = messages,
            max_tokens=500
        )
        message = response.choices[0].message.content.lower()
        remember = message.find("yes") != 1
        logging.info(f"remember query for {candidate} == {message} remember {remember}")
        if remember:
            self.short_term_memory = self.short_term_memory[:SHORT_TERM_MEMORY_DEPTH-1] + [ candidate ]

    def process_query(self, update : Update, query: str) -> str:
        try:
            # System messages
            messages = self.basic_messages.copy()
            logging.info(f"Long term {self.long_term_memory} st {self.short_term_memory}")
            for v in self.long_term_memory:
                messages.append({"role": "user", "content" : v, "name": "long_term_memory"})
            for v in self.short_term_memory:
                messages.append({"role": "user", "content" : v, "name": "short_term_memory"})
            messages.append({"role": "user", "content": query})

            logging.info(f"messages = {messages}")
            logging.info(f"functions = {self.functions}")
            # Max number of function calls
            for i in range(0,MAX_DEPTH):
                # No function call last time around
                if i < MAX_DEPTH-1:
                    response = self.client.chat.completions.create(
                        model=MODEL,
                        messages= messages,
                        functions = self.functions,
                        function_call = "auto",
                        max_tokens=500
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=MODEL,
                        messages= messages,
                        max_tokens=500
                    )

                logging.info(f"Response {response}")
                response_message = response.choices[0].message
                logging.info(f"response_message {response_message}")
                logging.info(f"Content {response_message.content}")
                logging.info(f"Role {response_message.role}")
                logging.info(f"Call {response_message.function_call}")

                if response_message.function_call:
                    function_name = response_message.function_call.name
                    arguments = json.loads(response_message.function_call.arguments)
                    response = executor.do_function_call(update, function_name, arguments)
                    messages.append(response_message)
                    messages.append({"role": "function",
                                     "name": function_name,
                                     "content": str(response) })
                    logging.info(f"Messages second time = {messages}")
                else:
                    result =  response.choices[0].message.content
                    self.maybe_remember(f"The user asked '{query}' and you responded '{result}'")
                    return result
            return "MAX_DEPTH exceeded - this should never happen"
        except Exception as e:
            return f"Error processing query: {str(e)}"
