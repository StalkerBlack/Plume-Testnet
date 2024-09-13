from loguru import logger
from web3 import Web3
from web3.eth.async_eth import AsyncContract


from client import Client
from utils import read_json
from data.config import CHECK_IN_ABI
from functions import ensure_sufficient_balance


class CheckInWorker:
    def __init__(self, client: Client):
        self.client: Client = client
        self.abi = read_json(CHECK_IN_ABI)

    @ensure_sufficient_balance(min_amount=0.05)
    async def check_in(self):
        PROXY_CONTRACT_ADDRESS = Web3.to_checksum_address(
            "0x8Dc5b3f1CcC75604710d9F464e3C5D2dfCAb60d8"
        )
        IMPLEMENTATION_CONTRACT_ADDRESS = Web3.to_checksum_address(
            "0xC2b6fe9C66cB72543f7434bdC610A20fD8F6038B"
        )

        implementation_contract: AsyncContract = self.client.w3.eth.contract(
            address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=self.abi
        )

        check_in_data = (
            implementation_contract.functions.checkIn()._encode_transaction_data()
        )

        try:
            tx_hash = await self.client.send_transaction(
                to=PROXY_CONTRACT_ADDRESS, data=check_in_data
            )
        except Exception as error:
            logger.error(
                f"Не удалось выполнить Check In на {self.client.number} кошельке: {self.client.address} | Error: {error}"
            )
            return False
        if tx_hash:
            logger.success(
                f"Хэш транзакции: {self.client.network.explorer + tx_hash} | Адрес: {self.client.address}"
            )
            return True
