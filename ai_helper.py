import json
from telegram import Update
from openai import OpenAI
from config import OPENAI_API_KEY
import logging
import utils
import blockchain

FUNCTIONS = [
    {
        "name": "get_balance",
        "description": "Retrieves the balance of a blockchain account",
        "parameters": {
            "type" : "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": "hex-encoded address of the account to query"
                },
            },
            "required": ["address"],
            }
    },
    # OpenAI doesn't believe in parameterless functions
    {
        "name": "get_my_address",
        "description": "Retrieves the blockchain address of the user who called this function",
        "parameters": {
            "type" :"object",
            "properties": {
                "dummy_property": {
                    "type": "null"
                }
            }
        }
    }
]


MODEL = "gpt-4o"

def do_function_call(update, function_name, arguments):
    if function_name == 'get_balance':
        address = arguments.get('address')
        response = blockchain.BlockchainClient().get_balance(address)
    elif function_name == 'get_my_address':
        account = utils.account_from_sender(update.effective_sender)
        response = account.address
    else:
        response = None
    return response


class AIHelper:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def process_query(self, update : Update, query: str) -> str:
        try:
            messages =[
                    {"role": "system", "content": "You are a helpful assistant specializing in blockchain technology."},
                    {"role": "user", "content": query}
                ]; 
            response = self.client.chat.completions.create(
                model=MODEL,
                messages= messages,
                functions = FUNCTIONS,
                function_call = "auto",
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
                response = do_function_call(update, function_name, arguments)
                messages.append(response_message)
                messages.append({"role": "function",
                                 "name": function_name,
                                 "content": str(response) })
                logging.info(f"Messages second time = {messages}")
                second_response = self.client.chat.completions.create(
                    model = MODEL,
                    messages = messages,
                    max_tokens = 500
                )
                logging.info(f"second {second_response}")
                return second_response.choices[0].message.content
            else:
                return response.choices[0].message.content
        except Exception as e:
            return f"Error processing query: {str(e)}"
