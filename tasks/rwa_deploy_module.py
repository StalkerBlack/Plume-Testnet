import random


from faker import Faker
from loguru import logger
from typing import Dict, Any
from web3 import Web3
from web3.eth.async_eth import AsyncContract, ChecksumAddress


from client import Client
from data.config import RWA_DEPLOY_ABI
from utils import read_json
from functions import ensure_sufficient_balance


class RWADeployWorker:
    def __init__(self, client: Client):
        self.client: Client = client
        self.abi = read_json(RWA_DEPLOY_ABI)

    @ensure_sufficient_balance(min_amount=0.05)
    async def deploy(self):
        PROXY_CONTRACT_ADDRESS: ChecksumAddress = Web3.to_checksum_address(
            "0x485D972889Ee8fd0512403E32eE94dE5c7a5DC7b"
        )
        IMPLEMENTATION_CONTRACT_ADDRESS: ChecksumAddress = Web3.to_checksum_address(
            "0xe1F9e3D1293f92c1dF87aeC9258C5EE68ebF6087"
        )

        implementation_contract: AsyncContract = self.client.w3.eth.contract(
            address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=self.abi
        )

        random_image: Dict[str, Any] = random.choice(
            [
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/art.webp",
                    "rwaType": 0,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/collectible-cards.webp",
                    "rwaType": 1,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/farming.webp",
                    "rwaType": 2,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/investment-alcohol.webp",
                    "rwaType": 3,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/investment-cigars.webp",
                    "rwaType": 4,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/investment-watch.webp",
                    "rwaType": 5,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/rare-sneakers.webp",
                    "rwaType": 6,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/real-estate.webp",
                    "rwaType": 7,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/solar-energy.webp",
                    "rwaType": 8,
                },
                {
                    "image": f"https://miles.plumenetwork.xyz/images/arc/tokenized-gpus.webp",
                    "rwaType": 9,
                },
            ]
        )

        fake = Faker()
        data: Dict[str, str] = {
            "name": f"{fake.name()}",
            "symbol": "ITEM",
            "description": f"{fake.text(random.randint(10, 30))}",
        }

        data.update(random_image)
        print(data)

        check_in_data = implementation_contract.functions.createToken(
            **data
        )._encode_transaction_data()
        try:
            tx_hash = await self.client.send_transaction(
                to=PROXY_CONTRACT_ADDRESS, data=check_in_data
            )
        except Exception as error:
            logger.info(
                f"Не удалось выполнить RWA Create Token на {self.client.number} кошельке | Error: {error}\n"
                f"Адрес: {self.client.address}"
            )
            return False

        if tx_hash:
            logger.success(
                f"Хэш транзакции: {self.client.network.explorer + tx_hash} | Адрес: {self.client.address}"
            )
            return True
