from loguru import logger
from web3 import Web3
from web3.exceptions import ContractCustomError
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
            self.w3 = Web3(Web3.HTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'proxy': self.proxy if self.proxy else {}}
            ))

        else:
            # Если прокси не переданы, создаем обычный HTTPProvider
            self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.network.rpc))

        self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)

        log_message = f"Инициализирован {self.number} клиент | Адрес {self.address} | Прокси: {self.proxy}"
        logger.info(log_message)


    def get_max_priority_fee_per_gas(self, block: dict) -> int:
        block_number = block['number']
        latest_block_transaction_count = self.w3.eth.get_block_transaction_count(block_number)
        max_priority_fee_per_gas_lst = []
        for i in range(latest_block_transaction_count):
            try:
                transaction = self.w3.eth.get_transaction_by_block(block_number, i)
                if 'maxPriorityFeePerGas' in transaction:
                    max_priority_fee_per_gas_lst.append(transaction['maxPriorityFeePerGas'])
            except Exception as error:
                continue

        if not max_priority_fee_per_gas_lst:
            max_priority_fee_per_gas = self.w3.eth.max_priority_fee
        else:
            max_priority_fee_per_gas_lst.sort()
            max_priority_fee_per_gas = max_priority_fee_per_gas_lst[len(max_priority_fee_per_gas_lst) // 2]
        return max_priority_fee_per_gas

    def send_transaction(
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
            'chainId': self.w3.eth.chain_id,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'from': Web3.to_checksum_address(from_),
            'to': Web3.to_checksum_address(to),
        }
        if data:
            tx_params['data'] = data

        if self.network.eip1559_tx:
            last_block = self.w3.eth.get_block('latest')
            base_fee = int(last_block['baseFeePerGas'] * increase_gas)
            
            if not max_priority_fee_per_gas:
                max_priority_fee_per_gas = self.get_max_priority_fee_per_gas(block=last_block)
            if not max_fee_per_gas or max_fee_per_gas < base_fee:
                max_fee_per_gas = base_fee + max_priority_fee_per_gas
            
            tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            tx_params['maxFeePerGas'] = max_fee_per_gas

        else:
            tx_params['gasPrice'] = self.w3.eth.gas_price

        if value:
            tx_params['value'] = value

        try:
            tx_params['gas'] = int(self.w3.eth.estimate_gas(tx_params) * increase_gas)

        except ContractCustomError as error:
            logger.info(f"Check In уже ранее был выполнен на кошельке {self.address} | {error}")
            # print(f'{self.address} | Transaction failed | {err}')
            return None

        sign = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
        return self.w3.eth.send_raw_transaction(sign.raw_transaction)
