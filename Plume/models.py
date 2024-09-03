import random
import time
import requests
from dataclasses import dataclass
from decimal import Decimal
from typing import Union
from datetime import datetime


@dataclass
class DefaultABIs:
    """
    The default ABIs.
    """
    Token = [
        {
            'constant': True,
            'inputs': [],
            'name': 'name',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'symbol',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'totalSupply',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'decimals',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': 'who', 'type': 'address'}],
            'name': 'balanceOf',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': '_owner', 'type': 'address'}, {'name': '_spender', 'type': 'address'}],
            'name': 'allowance',
            'outputs': [{'name': 'remaining', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'approve',
            'outputs': [],
            'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'transfer',
            'outputs': [], 'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        }]


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals


class Network:
    def __init__(self,
                 name: str,
                 rpc: str,
                 chain_id: int,
                 eip1559_tx: bool,
                 coin_symbol: str,
                 explorer: str,
                 decimals: int = 18,
                 ):
        self.name: str = name
        self.rpc: str = rpc
        self.chain_id: int = chain_id
        self.eip1559_tx: bool = eip1559_tx
        self.coin_symbol: str = coin_symbol
        self.decimals: int = decimals
        self.explorer: str = explorer

    def __str__(self):
        return f'{self.name}'


Arbitrum = Network(
    name='arbitrum',
    rpc='https://rpc.ankr.com/arbitrum/',
    chain_id=42161,
    eip1559_tx=True,
    coin_symbol='ETH',
    explorer='https://arbiscan.io/',
)


Plume = Network(
    name='plume testnet',
    rpc='https://testnet-rpc.plumenetwork.xyz/http',
    chain_id=161221135,
    eip1559_tx=True,
    coin_symbol='ETH',
    explorer='https://testnet-explorer.plumenetwork.xyz/tx/',
)



def check_proxy_ip(proxies):
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxies)
        print_with_time(f"\033[32m Прокси IP: {response.json()['origin']} \033[0m")
    except Exception as e:
        print_with_time(f"\033[31m Не удалось получить IP через прокси: {str(e)} \033[0m")


def print_with_time(message: str, flush: bool = True):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] {message}", flush=flush)



def sleep(up, to):
    delay = random.uniform(up, to)
    print_with_time(f"\033[34m Ожидаем {delay:.2f} секунд ...\033[0m")
    time.sleep(delay)