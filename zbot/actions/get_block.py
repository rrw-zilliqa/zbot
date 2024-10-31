from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler
from .. import action
from .. import blockchain
from .. import utils
import logging

class GetBlockAction(action.Action):
    def __init__(self):
        super().__init__()

    def command_name(self):
        return "block"

    def command_help(self):
        return "Get the number of the latest block"

    def description(self):
        return {
            "name": "get_latest_block",
            "description": "Get the number of the latest block in the blockchain",
            "parameters": {
                "type": "object",
                "properties": {
                    "dummy_property": { "type": "null" }
                    }
                }
            }

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        result = self.blockchain_client.get_latest_block()
        await update.message.reply_text(result)

    def try_function_call(self, update: Update, function_name: str, arguments):
        if function_name != "get_latest_block":
            return None
        result = self.blockchain_client.get_latest_block();
        return (result, None)
