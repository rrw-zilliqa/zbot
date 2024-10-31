import telegram
import hashlib
from web3 import Web3
from eth_account import Account
import secrets
import binascii
from . import config
import logging
from . import blockchain

class GiveUp(Exception):
    pass

def bytes_from_hex(hex_in):
    if hex_in.startsWith('0x'):
        hex_in = hex_in[2:]

    return bytes.fromhex(hex_in)

def txn_id_to_hex(txid):
    return f"0x{txid.hex()}"

def explore_txid(txid):
    return f"{config.EXPLORER_URL}tx/{txid}"

def explore_address(address):
    return f"{config.EXPLORER_URL}address/{address}"

def connect_to_sender(sender):
    return blockchain.connect(account_from_sender(sender))

def account_from_sender(sender):
    user = user_from_effective_sender(sender)
    user_len = f"{len(user):08x}"
    logging.info(f"user {user} len {user_len} seed {config.SEED}")
    # X ensures that SEED can't end with the start of a user_len
    some_data = config.SEED + "X" + user_len + user + "***END***"
    hashed = hashlib.sha3_256(some_data.encode('utf-8')).digest()
    return Account.from_key(hashed)

def user_from_effective_sender(sender):
    if sender:
        if isinstance(sender, telegram.Chat):
            # It's a chat
            if sender.username:
                return f"chat#{sender.id}"
            else:
                return None
        else:
            return f"user#{sender.id}"
    return None
