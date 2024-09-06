import asyncio
import random


from loguru import logger
from web3 import Web3
from web3.eth.async_eth import ChecksumAddress, AsyncContract

from Plume.client import Client
from Plume.data.config import VOTE
from Plume.utils import read_json


class VoteWorker:
    def __init__(self, client: Client):
        self.client: Client = client
        self.abi = read_json(VOTE)

    async def vote(self):
        PROXY_CONTRACT_ADDRESS: ChecksumAddress = Web3.to_checksum_address(
            "0xbd06be7621be8f92101bf732773e539a4daf7e3f"
        )
        IMPLEMENTATION_CONTRACT_ADDRESS: ChecksumAddress = Web3.to_checksum_address(
            "0x92D8e70879ba9Ad9C0Cf540F48FbdD692D9CE086"
        )

        implementation_contract: AsyncContract = self.client.w3.eth.contract(
            address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=self.abi
        )

        lst_data = [18, 21]
        data = random.choice(lst_data)

        vote_data = implementation_contract.functions.vote(
            data
        )._encode_transaction_data()

        for _ in range(3):
            tx_hash = await self.client.send_transaction(
                to=PROXY_CONTRACT_ADDRESS, data=vote_data
            )
            if tx_hash:
                logger.success(
                    f"Успешно проголосовали!\nХэш транзакции: {self.client.network.explorer + tx_hash} | Адрес: {self.client.address}"
                )
            else:
                logger.info(
                    f"Не удалось проголосовать на {self.client.number} кошельке: {self.client.address}"
                )

            # Спим 2 минуты
            await asyncio.sleep(120)
