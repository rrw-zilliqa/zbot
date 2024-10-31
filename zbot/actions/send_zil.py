from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler
from .. import action
from .. import blockchain
from .. import utils
import logging

class SendZilAction(action.Action):
    def __init__(self):
        super().__init__()

    def command_name(self):
        return "send"

    def command_help(self):
        return "Send ZIL to another address; specify address then amount in Zil"

    def description(self):
        return  {
            "name": "send_zil",
            "description": "Send some zil to another address. Returns a triple (result, txn_id, error)",
            "parameters": {
                "type" : "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "hex-encoded address of the account to send zil to"
                    },
                    "amount": {
                        "type": "string",
                        "description": "Decimal amount of zil to send. Must be less than your balance"
                    },
                },
                "required": ["address", "amount"],
            }
        }

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info("A000")
        account = utils.account_from_sender(update.effective_sender)
        if not context.args:
            await update.message.reply_text("Please provide a recipient and an amount.")
            return
        logging.info("A001");
        to_address = context.args[0]
        amount = context.args[1]
        logging.info("A002");
        connected = utils.connect_to_sender(update.effective_sender)
        await update.message.reply_text(f"Sending {amount} to {to_address}")
        (result, txn_id, err) = connected.send_zil(to_address, amount)
        if result:
            url = utils.explore_txid(txn_id)
            await update.message.reply_markdown_v2(f"All done [{txn_id}]({url})")
        else:
            await update.message.reply_text(f"Failed - {err}")

    def try_function_call(self, update: Update, function_name: str, arguments):
        if function_name != "send_zil":
            return None
        to_address = arguments["address"]
        amount = arguments["amount"]
        connected = utils.connect_to_sender(update.effective_sender)
        (result, txn_id, err) = connected.send_zil(to_address, amount)
        return (result, txn_id, err)
