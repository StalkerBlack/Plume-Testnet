import json


from loguru import logger


from Plume.client import Client
from Plume.utils import read_json
from Plume.data.config import CHECK_IN_ABI


class CheckInWorker:
    def __init__(self,
                 client: Client
                 ):
        self.client: Client = client
        self.abi = read_json(CHECK_IN_ABI)

    async def check_in(self):
        PROXY_CONTRACT_ADDRESS = '0x8Dc5b3f1CcC75604710d9F464e3C5D2dfCAb60d8'
        IMPLEMENTATION_CONTRACT_ADDRESS = '0xC2b6fe9C66cB72543f7434bdC610A20fD8F6038B'

        web3 = self.client.w3

        implementation_contract = web3.eth.contract(address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=self.abi)

        check_in_data = implementation_contract.functions.checkIn()._encode_transaction_data()

        tx_hash = self.client.w3.eth.send_transaction(
            to=PROXY_CONTRACT_ADDRESS,
            data=check_in_data
        )
        logger.info(f"Tx hash for check in: {tx_hash.hex()}")
        return tx_hash
