from web3 import Web3

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]

def get_token_balance(client: BlockchainClient, token_address: str, address: str) -> str:
    token_contract = client.w3.eth.contract(
        address = self.w3.to_checksum_address(token_address),
        abi = ERC20_ABI
    )
    balance = token_contract.functions.balanceOf(address).call()
    decimals = token_contract.functions.decimals().call()
    symbol = token_contract.functions.symbol().call()
    adjusted = balance / (10**decimals)
    return (adjusted, symbol)
