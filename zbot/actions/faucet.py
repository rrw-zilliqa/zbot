from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler
from .. import action
from .. import blockchain
from .. import utils
import logging

class FaucetAction(action.Action):
    def __init__(self):
        super().__init__()

    def command_name(self):
        return "faucet"

    def command_help(self):
        return "Obtain some zil from the faucet"

    def description(self):
        return  {
            "name": "get_zil_from_faucet",
            "description": "Calls the faucet to add Zil to your account. The return value is a tuple of result, transaction id, error message",
            "parameters": {
                "type" : "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "hex-encoded address of the account to give Zil to"
                    },
                },
                "required": ["address"],
            }
        }

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        account = utils.account_from_sender(update.effective_sender)
        (result, txid, error) = self.blockchain_client.run_faucet(account.address)
        if error is not None:
            await update.message.reply_text(f"Couldn't request ZIL - {error}")
        else:
            explorer_url = utils.explore_txid(txid)
            await update.message.reply_markdown_v2(f"All done - txid [{txid}]({explorer_url})")

    def try_function_call(self, update: Update, function_name: str, arguments):
        if function_name != "get_zil_from_faucet":
            return None
        address = arguments.get('address')
        (result, txid, error) = self.blockchain_client.run_faucet(address)
        return (result, txid, error)
