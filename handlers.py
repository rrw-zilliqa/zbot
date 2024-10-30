from telegram import Update
from telegram.ext import ContextTypes
from blockchain import BlockchainClient
from ai_helper import AIHelper
from config import COMMAND_DESCRIPTIONS
import utils
import logging

blockchain_client = BlockchainClient()
ai_helper = AIHelper()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome to the Blockchain AI Bot!\n\n"
        "I can help you with blockchain queries and answer your questions.\n"
        "Type /help to see available commands."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Available commands:\n\n"
    for command, description in COMMAND_DESCRIPTIONS.items():
        help_text += f"/{command} - {description}\n"
    await update.message.reply_text(help_text)

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if context.args:
            address = context.args[0]
            result = blockchain_client.get_balance(address)
            url = utils.explore_address(address)
            logging.info(f"address {address} url {url} result {result}")
            await update.message.reply_markdown_v2(f"Balance of [{address}]({url}) is `{result}`")
        else:
            account = utils.account_from_sender(update.effective_sender)
            result = blockchain_client.get_balance(account.address)
            url = utils.explore_address(account.address)
            logging.info(f"address {account.address} url {url} result {result}")
            await update.message.reply_markdown_v2(f"Balance of [{account.address}]({url}) is `{result}`")
    except Exception as e:
        await update.message.reply_text(f"Error - {e}")


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = blockchain_client.get_latest_block()
    await update.message.reply_text(result)

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a question.")
        return

    try:
        query = ' '.join(context.args)
        response = ai_helper.process_query(update, query)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error - {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("An error occurred. Please try again later.")

async def send_zil_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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
    except Exception as e:
        logging.info("A005")
        await update.message.reply_text(f"Error - {e}")

async def faucet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        account = utils.account_from_sender(update.effective_sender)
        (result, txid, error) = blockchain_client.run_faucet(account.address)
        if error is not None:
            await update.message.reply_text(f"Couldn't request ZIL - {error}")
        else:
            explorer_url = utils.explore_txid(txid)
            await update.message.reply_markdown_v2(f"All done - txid [{txid}]({explorer_url})")
    except Exception as e:
        await update.message.reply_text(f"Error - {e}")

async def whoami_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
