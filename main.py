#! /usr/bin/env python3

import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from zbot.config import TELEGRAM_BOT_TOKEN
import zbot.executor as executor

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
    executor.add_commands(application)

    # Start the bot
    logging.info("Starting bot...")
    application.run_polling(poll_interval=1.0)

if __name__ == '__main__':
    main()
