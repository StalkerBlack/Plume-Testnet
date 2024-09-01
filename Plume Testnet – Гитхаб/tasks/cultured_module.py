import random
from utils import read_json
from data.config import CULTURED
from models import sleep


def cultured(client):
    PROXY_CONTRACT_ADDRESS = '0x032139f44650481f4d6000c078820B8E734bF253'
    IMPLEMENTATION_CONTRACT_ADDRESS = '0xa92B6A07c21Ea051F833423871c34487Ecc670D6'
    IMPLEMENTATION_ABI = read_json(CULTURED)

    web3 = client.w3

    implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=IMPLEMENTATION_ABI)

    bools = [True, False]
    dates = [24, 14, 15, 16, 17, 18, 19, 20, 0, 1, 2, 6, 8, 10, 12, 3, 4, 5, 7, 9, 11, 13, 21, 22, 23, 25]
    for idx, date in enumerate(dates, start=1):
        random_bool = random.choice(bools)
        cultured_data = implementation_contract.functions.predictPriceMovement(date, random_bool)._encode_transaction_data()
        sleep(15,39)

        try:
            tx_hash = client.send_transaction(
                to=PROXY_CONTRACT_ADDRESS,
                data=cultured_data
            )

            yield tx_hash, idx
        except Exception as e:
            yield None, idx
