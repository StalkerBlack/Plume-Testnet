from loguru import logger
from web3 import Web3, AsyncWeb3
from web3.exceptions import ContractCustomError, Web3RPCError
from typing import Optional, Dict

from models import Network


class Client:
    def __init__(
            self,
            number: int,
            private_key: str,
            network: Network,
            proxy: str | None = None,
        ) -> None:
        """ 
        
        Инициализируем клиента, с которым будем работать
        
        """

        self.number: int = number
        self.private_key: str = private_key
        self.network: Network = network
        self.network_name: str = self.network.name
        self.chain_id: int = self.network.chain_id
        self.explorer: str = self.network.explorer
        self.proxy: str | None = proxy

        # Проверяем, переданы ли прокси
        if proxy:
            # Если прокси переданы, используем их при создании HTTPProvider
            self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'proxy': self.proxy, "verify_ssl": False}
            ))

        else:
            # Если прокси не переданы, создаем обычный HTTPProvider
            self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'verify_ssl': False}
            ))

        self.address = AsyncWeb3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)

        log_message = f"Инициализирован {self.number} клиент | Адрес {self.address} | Прокси: {self.proxy}"
        logger.info(log_message)


    async def get_max_priority_fee_per_gas(self, block: dict) -> int:
        block_number = block['number']
        latest_block_transaction_count = await self.w3.eth.get_block_transaction_count(block_number)
        max_priority_fee_per_gas_lst = []
        for i in range(latest_block_transaction_count):
            try:
                transaction = await self.w3.eth.get_transaction_by_block(block_number, i)
                if 'maxPriorityFeePerGas' in transaction:
                    max_priority_fee_per_gas_lst.append(transaction['maxPriorityFeePerGas'])
            except Exception as error:
                continue

        if not max_priority_fee_per_gas_lst:
            max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
        else:
            max_priority_fee_per_gas_lst.sort()
            max_priority_fee_per_gas = max_priority_fee_per_gas_lst[len(max_priority_fee_per_gas_lst) // 2]
        return max_priority_fee_per_gas

    async def send_transaction(
            self,
            to,
            data=None,
            from_=None,
            increase_gas: float = 1.125,
            value=None,
            max_priority_fee_per_gas: Optional[int] = None,
            max_fee_per_gas: Optional[int] = None
        ):
        if not from_:
            from_ = self.address

        tx_params: dict = {
            'chainId': await self.w3.eth.chain_id,
            'nonce': await self.w3.eth.get_transaction_count(self.address),
            'from': AsyncWeb3.to_checksum_address(from_),
            'to': AsyncWeb3.to_checksum_address(to),
        }
        if data:
            tx_params['data'] = data

        if self.network.eip1559_tx:
            last_block = await self.w3.eth.get_block('latest')
            base_fee = int(last_block['baseFeePerGas'] * increase_gas)
            
            if not max_priority_fee_per_gas:
                max_priority_fee_per_gas = await self.get_max_priority_fee_per_gas(block=last_block)
            if not max_fee_per_gas or max_fee_per_gas < base_fee:
                max_fee_per_gas = base_fee + max_priority_fee_per_gas
            
            tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            tx_params['maxFeePerGas'] = max_fee_per_gas

        else:
            tx_params['gasPrice'] = await self.w3.eth.gas_price

        if value:
            tx_params['value'] = value

        try:
            logger.info(f"Выполняем estimate_gas для {self.address} | {tx_params}")
            tx_params['gas'] = int(await self.w3.eth.estimate_gas(tx_params) * increase_gas)
            logger.info(f"Выполняем send_transaction для {self.address} | {tx_params}")

        except Web3RPCError as error:
            logger.error(f"Не удалось выполнить estimate_gas для {self.address} | {error}")

            if "gas required exceeds allowance" in error.message:
                logger.error(f"Недостаточно баланса для расчета газа! Адрес: {self.address} | Error: {error}")

            return None

        except ContractCustomError as error:
            logger.info(f"Check In уже ранее был выполнен на кошельке {self.address} | {error}")
            return None

        sign = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
        return self.w3.to_hex(await self.w3.eth.send_raw_transaction(sign.raw_transaction))
