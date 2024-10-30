from telegram import Update
from telegram.ext import ContextTypes
from blockchain import BlockchainClient
from ai_helper import AIHelper
from config import COMMAND_DESCRIPTIONS

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
    if not context.args:
        await update.message.reply_text("Please provide an Ethereum address.")
        return
    
    address = context.args[0]
    result = blockchain_client.get_balance(address)
    await update.message.reply_text(result)

async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = blockchain_client.get_latest_block()
    await update.message.reply_text(result)

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a question.")
        return
    
    query = ' '.join(context.args)
    response = ai_helper.process_query(query)
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("An error occurred. Please try again later.")
