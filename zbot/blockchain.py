from web3 import Web3
from web3.middleware import SignAndSendRawMiddlewareBuilder
from .config import ETHEREUM_RPC_URL
from eth_account.signers.local import LocalAccount
import logging
import requests
import re
from . import config
from . import utils

def connect(account):
    client = BlockchainClient()
    client.w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account),layer=0)
    client.account = account
    return client

class BlockchainClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
        self.account = None

    def wait_for_receipt(self, txid):
        return self.w3.eth.wait_for_transaction_receipt(txid)

    def send_zil(self, to_address, amount):
        # @TODO remove - useful for testing, but ..
        to_address = Web3.to_checksum_address(to_address)
        transaction = {
            'to': to_address,
            'from': self.account.address,
            'value': Web3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'chainId': 1  # Mainnet = 1, Ropsten = 3, Rinkeby = 4, etc.
        }
        # Sign the transaction
        signed_txn = self.account.sign_transaction(transaction)
        # Send the transaction
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        # Wait for the transaction to be mined
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        logging.info(f"receipt {txn_receipt}")
        return (txn_receipt.status==1, utils.txn_id_to_hex(txn_hash), None)

    def get_balance(self, address: str) -> str:
        try:
            if not self.w3.is_address(address):
                return None
            # Force it to be a checksum address
            address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return balance_eth
        except Exception as e:
            return f"Error fetching balance: {str(e)}"

    def get_latest_block(self) -> str:
        try:
            block = self.w3.eth.get_block('latest')
            return (
                f"Latest Block:\n"
                f"Number: {block.number}\n"
                f"Timestamp: {block.timestamp}\n"
                f"Transactions: {len(block.transactions)}\n"
                f"Gas Used: {block.gasUsed}"
            )
        except Exception as e:
            return f"Error fetching block: {str(e)}"

    # Returns (txn_id, error)
    def run_faucet(self, for_address):
        try:
            resp = requests.post(config.FAUCET_URL, data={'address': for_address})
            # Find a transaction id in the response
            resp_text = resp.text
            logging.info(f"resp_text = {resp.text}")
            txn_id = re.search(r'(0x[0-9a-fA-F]{64})', resp_text)
            if txn_id:
                logging.info(f"txn id {txn_id[0]}")
                receipt = self.wait_for_receipt(txn_id[0])
                logging.info(f"receipt {receipt}")
                return (receipt.status==1, txn_id, None)
            else:
                return (None, None, "No transaction id found in response - likely too soon for another batch of ZIL")
        except Exception as e:
            return (None, None, f"Failed - {e}")
