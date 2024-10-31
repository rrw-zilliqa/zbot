from telegram import Update
import telegram.ext
from telegram.ext import ContextTypes
from .blockchain import BlockchainClient
from .config import COMMAND_DESCRIPTIONS
from . import blockchain
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from . import utils
from . import ai_helper
import logging
from .actions import get_address
from .actions import get_balance
from .actions import get_block
from .actions import send_zil
from .actions import faucet

ACTIONS = []

def register():
    ACTIONS.append(get_address.GetAddressAction())
    ACTIONS.append(get_balance.GetBalanceAction())
    ACTIONS.append(get_block.GetBlockAction())
    ACTIONS.append(send_zil.SendZilAction())
    ACTIONS.append(faucet.FaucetAction())

def get_functions():
    functions = [ ]
    for act in ACTIONS:
        function = act.description()
        logging.info(f"function = {function}")
        if function is not None:
            functions.append(function)
    return functions

def do_function_call(update, function_name, arguments):
    for act in ACTIONS:
        result = act.try_function_call(update, function_name, arguments)
        if result is not None:
            return result
    return None

def wrap_handler(inner):
    async def wrapper(update, context):
        try:
            return await inner(update,context)
        except Exception as e:
            await update.message.reply_text(f"Error - {e}")
    return wrapper

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("An error occurred. Please try again later.")

the_ai = None

def get_ai():
    global the_ai
    if the_ai is None:
        logging.info("Constructing helper!")
        the_ai = ai_helper.AIHelper()
    return the_ai

async def handle_remember_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    helper = get_ai()
    if not context.args:
        await update.message.reply_text("Please provide something to remember")
    query = ' '.join(context.args)
    response = helper.remember(query)
    await update.message.reply_text("Remembered")

async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Available commands:\n\n"
    help_text += "/help  Prints this help text\n"
    help_text += "/ask   Ask the AI to do something for you (try \"/ask what's my balance?\")\n"
    help_text += "/remember Put the result in the AI's long term memory\n"
    for act in ACTIONS:
        help_text += f"/{act.command_name()}  {act.command_help()}\n"
    await update.message.reply_text(help_text)

async def handle_ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    helper = get_ai()
    if not context.args:
        await update.message.reply_text("Please provide a question.")
        return

    query = ' '.join(context.args)
    response = helper.process_query(update, query)
    await update.message.reply_text(response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    helper = get_ai()
    response = helper.process_query(update, update.message.text)
    await update.message.reply_text(response)

def add_commands(app):
    app.add_error_handler(wrap_handler(handle_error))
    app.add_handler(CommandHandler("help", wrap_handler(handle_help_command)))
    app.add_handler(CommandHandler("ask", wrap_handler(handle_ask_command)))
    app.add_handler(CommandHandler("remember", wrap_handler(handle_remember_command)))
    app.add_handler(MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, handle_message))
    for act in ACTIONS:
        def create_handler(call_act):
            async def call_handler(update, context):
                result = await call_act.handle(update, context)
                return result
            return call_handler
        app.add_handler(CommandHandler(act.command_name(), wrap_handler(create_handler(act))))
