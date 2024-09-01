from utils import read_json
from data.config import CHECK_IN_ABI


def check_in(client):
    PROXY_CONTRACT_ADDRESS = '0x8Dc5b3f1CcC75604710d9F464e3C5D2dfCAb60d8'
    IMPLEMENTATION_CONTRACT_ADDRESS = '0xC2b6fe9C66cB72543f7434bdC610A20fD8F6038B'
    IMPLEMENTATION_ABI = read_json(CHECK_IN_ABI)

    web3 = client.w3

    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)

    check_in_data = implementation_contract.functions.checkIn()._encode_transaction_data()

    tx_hash = client.send_transaction(
        to=PROXY_CONTRACT_ADDRESS,
        data=check_in_data
    )

    return tx_hash

