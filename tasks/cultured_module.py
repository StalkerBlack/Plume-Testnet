import asyncio
import random

from loguru import logger
from typing import List
from web3.eth.async_eth import AsyncContract, ChecksumAddress

from utils import read_json
from data.config import CULTURED
from client import Client
from functions import ensure_sufficient_balance


class CulturedWorker:
    def __init__(self, client: Client):
        self.client: Client = client
        self.abi = read_json(CULTURED)

    @ensure_sufficient_balance(min_amount=0.0005)
    async def cultured(self):
        PROXY_CONTRACT_ADDRESS: ChecksumAddress = self.client.w3.to_checksum_address(
            "0x032139f44650481f4d6000c078820B8E734bF253"
        )
        IMPLEMENTATION_CONTRACT_ADDRESS: ChecksumAddress = self.client.w3.to_checksum_address(
            "0xa92B6A07c21Ea051F833423871c34487Ecc670D6"
        )
        implementation_contract: AsyncContract = self.client.w3.eth.contract(
            address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=self.abi
        )

        pairs_indexes: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27]

        for idx, pair in enumerate(pairs_indexes, start=1):
            random_prediction: bool = random.choice([True, False])
            cultured_data = implementation_contract.functions.predictPriceMovement(
                pair,
                random_prediction
            )._encode_transaction_data()

            try:
                tx_hash = await self.client.send_transaction(
                    to=PROXY_CONTRACT_ADDRESS,
                    data=cultured_data
                )

            except Exception as error:
                logger.info(
                    f"Не удалось выполнить RWA Create Token на {self.client.number} кошельке | Error: {error}\n"
                    f"Адрес: {self.client.address}"
                )
                continue

            if tx_hash:

                logger.success(
                    f"Успешно сделали prediction на {pair} пару на {self.client.number} кошельке | "
                    f"Хэш транзакции: {self.client.network.explorer + tx_hash}\nАдрес: {self.client.address}"
                )
                delay = random.randint(25, 45)
                logger.info(f"Ждем {delay} секунд до начала следующего prediction | Адрес {self.client.address}")
                await asyncio.sleep(delay)
        return True
