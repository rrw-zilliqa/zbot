#! /usr/bin/env python3

import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from config import TELEGRAM_BOT_TOKEN
from handlers import (
    start_command,
    help_command,
    balance_command,
    block_command,
    ask_command,
    error_handler,
    faucet_handler,
    send_zil_handler
)
import executor

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # Register actions - do this so we run init after logging is configured.
    executor.register()
    # Initialize the bot
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    #application.add_handler(CommandHandler('balance', balance_command))
    application.add_handler(CommandHandler('block', block_command))
    application.add_handler(CommandHandler('ask', ask_command))
    #application.add_handler(CommandHandler('whoami', whoami_handler))
    application.add_handler(CommandHandler('faucet', faucet_handler))
    application.add_handler(CommandHandler('send', send_zil_handler))

    executor.add_commands(application)

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logging.info("Starting bot...")
    application.run_polling(poll_interval=1.0)

if __name__ == '__main__':
    main()
