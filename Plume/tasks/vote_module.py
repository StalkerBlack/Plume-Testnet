import random


from ..utils import read_json
from ..data.config import VOTE



def vote_1(client):
    PROXY_CONTRACT_ADDRESS = '0xbd06be7621be8f92101bf732773e539a4daf7e3f'
    IMPLEMENTATION_CONTRACT_ADDRESS = '0x92D8e70879ba9Ad9C0Cf540F48FbdD692D9CE086'
    IMPLEMENTATION_ABI = read_json(VOTE)

    web3 = client.w3

    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)

    lst_data = [23, 33, 26]
    data = random.choice(lst_data)

    check_in_data = implementation_contract.functions.vote(data)._encode_transaction_data()

    tx_hash = client.send_transaction(
        to=PROXY_CONTRACT_ADDRESS,
        data=check_in_data
    )

    return tx_hash

def vote_2(client):
    PROXY_CONTRACT_ADDRESS = '0xbd06be7621be8f92101bf732773e539a4daf7e3f'
    IMPLEMENTATION_CONTRACT_ADDRESS = '0x92D8e70879ba9Ad9C0Cf540F48FbdD692D9CE086'
    IMPLEMENTATION_ABI = read_json(VOTE)

    web3 = client.w3

    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)

    lst_data = [24, 31, 27]
    data = random.choice(lst_data)

    check_in_data = implementation_contract.functions.vote(data)._encode_transaction_data()

    tx_hash = client.send_transaction(
        to=PROXY_CONTRACT_ADDRESS,
        data=check_in_data
    )

    return tx_hash


def vote_3(client):
    PROXY_CONTRACT_ADDRESS = '0xbd06be7621be8f92101bf732773e539a4daf7e3f'
    IMPLEMENTATION_CONTRACT_ADDRESS = '0x92D8e70879ba9Ad9C0Cf540F48FbdD692D9CE086'
    IMPLEMENTATION_ABI = read_json(VOTE)

    web3 = client.w3

    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)

    lst_data = [20, 32, 25]
    data = random.choice(lst_data)

    check_in_data = implementation_contract.functions.vote(data)._encode_transaction_data()

    tx_hash = client.send_transaction(
        to=PROXY_CONTRACT_ADDRESS,
        data=check_in_data
    )

    return tx_hash

