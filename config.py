import os

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL')
SEED = os.getenv("SEED")
FAUCET_URL = os.getenv('ZILLIQA_FAUCET_URL')
EXPLORER_URL =os.getenv('ZILLIQA_OTTERSCAN_URL')

# Command descriptions
COMMAND_DESCRIPTIONS = {
    'start': 'Start the bot and get welcome message',
    'help': 'Show available commands',
    'balance': 'Get ETH balance for an address',
    'block': 'Get latest block information',
    'ask': 'Ask AI about blockchain concepts',
    "whoami" : "Who am I?",
    "faucet" : "Mint 100 ZIL to my account",
}

