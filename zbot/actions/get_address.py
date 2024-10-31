from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler
from .. import action
from .. import blockchain
from .. import utils
import logging

class GetAddressAction(action.Action):
    def __init__(self):
        super().__init__()

    def command_name(self):
        return "whoami"

    def description(self):
        # OpenAI doesn't believe in parameterless functions
        return {
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

    async def whoami_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = utils.user_from_effective_sender(update.effective_sender)
            account = utils.account_from_sender(update.effective_sender)
            if user:
                reply_text = f"I think you are {user} with address {account.address}"
            else:
                reply_text = "Cannot determine who you are - sorry"
            await update.message.reply_text(reply_text)
        except Exception as e:
            logging.info(f"e - {e}")

    def try_function_call(self, update: Update, function_name: str, arguments):
        if function_name != "get_my_address":
            return None
        account = utils.account_from_sender(update.effective_sender)
        response = account.address
        return (response, None)
