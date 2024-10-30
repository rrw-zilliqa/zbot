from web3 import Web3
from config import ETHEREUM_RPC_URL

class BlockchainClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))

    def get_balance(self, address: str) -> str:
        try:
            if not self.w3.is_address(address):
                return "Invalid Ethereum address"
            # Force it to be a checksum address
            address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return f"Balance: {balance_eth:.4f} ETH"
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
