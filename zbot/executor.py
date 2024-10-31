from telegram import Update
from telegram.ext import ContextTypes
from .blockchain import BlockchainClient
from .config import COMMAND_DESCRIPTIONS
from . import blockchain
from telegram.ext import ApplicationBuilder, CommandHandler
from . import utils
import logging
from .actions import get_address
from .actions import get_balance

ACTIONS = []

def register():
    ACTIONS.append(get_address.GetAddressAction())
    ACTIONS.append(get_balance.GetBalanceAction())

def get_functions():
    functions = [ ]
    for act in ACTIONS:
        function = act.description()
        logging.info("function = {function}")
        if function is not None:
            functions.append(function)
    return functions

def do_function_call(update, function_name, arguments):
    for act in ACTIONS:
        result = act.try_function_call(update, function_name, arguments)
        if result is not None:
            return result
    return None

def add_commands(app):
    for act in ACTIONS:
        async def call_handler(update, context):
            result = await act.handle(update, context)
            return result
        app.add_handler(CommandHandler(act.command_name(), call_handler))
