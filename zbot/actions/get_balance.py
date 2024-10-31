from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler
from .. import action
from .. import blockchain
from .. import utils
import logging

class GetBalanceAction(action.Action):
    def __init__(self):
        super().__init__()

    def command_name(self):
        return "balance"

    def command_help(self):
        return "Retrieve the native balance of an address"

    def description(self):
        return  {
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
        }

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.args:
            address = context.args[0]
            result = self.blockchain_client.get_balance(address)
            if result is None:
                await update.message.reply_markdown_v2(f("{address} is not valid"))
                return
            url = utils.explore_address(address)
            logging.info(f"address {address} url {url} result {result}")
            await update.message.reply_markdown_v2(f"Balance of [{address}]({url}) is `{result}`")
        else:
            account = utils.account_from_sender(update.effective_sender)
            result = self.blockchain_client.get_balance(account.address)
            if result is None:
                await update.message.reply_markdown_v2(f("{address} is not valid"))
                return
            url = utils.explore_address(account.address)
            logging.info(f"address {account.address} url {url} result {result}")
            await update.message.reply_markdown_v2(f"Balance of [{account.address}]({url}) is `{result}`")

    def try_function_call(self, update: Update, function_name: str, arguments):
        if function_name != "get_balance":
            return None
        address = arguments.get('address')
        response = blockchain.BlockchainClient().get_balance(address)
        if response is None:
            return (None, "Invalid address")
        else:
            return (response, None)

