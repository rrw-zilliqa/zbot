from telegram import Update
from telegram.ext import ContextTypes
from .blockchain import BlockchainClient
from .config import COMMAND_DESCRIPTIONS
from . import blockchain
from telegram.ext import ApplicationBuilder, CommandHandler
from . import utils
from .utils import GiveUp
import logging

class Action:
    def __init__(self):
        self.blockchain_client = BlockchainClient()

    def command_name(self):
        raise GiveUp("Called base get_name() method")

    def command_help(self):
        return "No help available for this command"

    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise GiveUp("Called base handle() method")

    # Return the OpenAI description
    def description(self):
        raise GiveUp("Base get_description() method called")

    # Returns either None or a response.
    def try_function_call(self, update: Update, function_name: str, arguments):
        raise GiveUp("Base do_function_call() method called")

