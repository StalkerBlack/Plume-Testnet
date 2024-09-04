import asyncio
import random
import requests
import sys


from loguru import logger
from typing import Sequence

from Plume.tasks.vote_module import VoteWorker
from client import Client
from config import PRIVATE_KEYS, PROXIES
from tasks.check_in_module import CheckInWorker
# from data.config_accounts import ACCOUNTS
# from models import Plume, sleep, print_with_time, check_proxy_ip
# from tasks.check_in_module import check_in
# from tasks.faucet_module import token_extraction, faucet
# from tasks.vote_module import vote_1, vote_2, vote_3
# from tasks.cultured_module import cultured
from settings import GLOBAL_NETWORK, SLEEP_MODE, SLEEP_TIME, WALLETS_TO_WORK, SHUFFLE_WALLETS


logger.remove()
logger.add(sink=sys.stdout,
           backtrace=True,
           level="INFO",
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>"
           )


"""# Check In
for account in ACCOUNTS:
    sleep(33, 368)
    try:
        print_with_time(f"\033[33m Выполнение задания: Check In на {account['name']}\033[0m")

        # Создание клиента для каждого аккаунта
        client = Client(private_key=account['private_key'], network=Plume)

        if not client.w3.is_connected():
            print_with_time(f"\033[31m Не удалось подключиться: {account['name']}\033[0m")
            continue

        # Выполнение Check-In
        tx_hash = check_in(client=client)

        if tx_hash:
            print_with_time(f"\033[32m Chek In выполнен {account['name']}!!! Hash: {tx_hash.hex()}\033[0m")
        else:
            print_with_time(f"\033[31m Chek In не удался {account['name']}!!!\033[0m")
 
    except Exception as e:
        print_with_time(f"\033[31m Возникла ошибка {account['name']}: {str(e)}\033[0m")
print('************************************************************************')
print_with_time(f'\033[32m Чек-ин на всех аккаунтах: Завершен!!!\033[0m')
print('************************************************************************')
"""


"""# Голосовалка
for account in ACCOUNTS:
    sleep(33, 368)
    try:
        print_with_time(f"\033[33m Выполнение задания с голосованием {account['name']}\033[0m")

        # Создание клиента для каждого аккаунта
        client = Client(private_key=account['private_key'], network=Plume, proxies=account.get("proxies", None))

        check_proxy_ip(account['proxies']) # Вывод о статусе прокси

        if not client.w3.is_connected():
            print_with_time(f"\033[31m Не удалось подключиться: {account['name']}\033[0m")
            continue

        # Голосование
        votes =[vote_1, vote_2, vote_3]
        for vote in votes:
            tx_hash = vote(client=client)

            if tx_hash:
                print_with_time(f"\033[32m Успешно проголосованно на {account['name']}!!! Hash: {tx_hash.hex()}\033[0m")
            else:
                print_with_time(f"\033[31m Не удалось проголосовать {account['name']}\033[0m")

            sleep(22, 63)
 
    except Exception as e:
        print_with_time(f"\033[31m Возникла ошибка {account['name']}: {str(e)}\033[0m")
print('************************************************************************')
print_with_time(f'\033[32m Голосование на всех аккаунтах: Завершенно\033[0m')
print('************************************************************************')
"""


'''#  Ставки
for account in ACCOUNTS:
    sleep(1, 5)
    try:
        print_with_time(f"\033[33m Выполнения задания по ставкам: {account['name']}\033[0m")

        # Создание клиента для каждого аккаунта
        client = Client(private_key=account['private_key'], network=Plume, proxies=account.get("proxies", None))
        

        check_proxy_ip(account['proxies']) # Вывод о статусе прокси

        if not client.w3.is_connected():
            print_with_time(f"\033[31m Не удалось подключиться: {account['name']}\033[0m")
            continue

        # Выполнение Cultured
        # for tx_hash, idx in cultured(client=client):
        #     if tx_hash:
        #         print_with_time(f"\033[32m Ставка №{idx} успешно поставленна!!! Hash: {tx_hash.hex()}\033[0m")
        #     else:
        #         print_with_time(f"\033[31m Не удалось поставить ставку №{idx}\033[0m")
 
    except Exception as e:
        print_with_time(f"\033[31m Возникла ошибка {account['name']}: {str(e)}\033[0m")
print('************************************************************************')
print_with_time(f'\033[32m Ставки сделаны - на всех аккаунтах\033[0m')
print('************************************************************************')
'''


class Runner:

    async def get_proxy_for_account(self, index: int, private_key: str):
        try:
            private_key_index = PRIVATE_KEYS.index(private_key) + 1
            return PROXIES[private_key_index % len(PROXIES)]

        except Exception as error:
            logger.info(f"{index} кошелек запускается без прокси: {error}")

    async def smart_sleep(self):
        if SLEEP_MODE:
            duration = random.randint(*SLEEP_TIME)
            logger.info(f"💤 Спим {duration} секунд")
            await asyncio.sleep(duration)

    def get_private_keys(self):
        logger.info("Getting private keys ...")
        if WALLETS_TO_WORK == 0:
            private_keys: list[str] = PRIVATE_KEYS

        elif isinstance(WALLETS_TO_WORK, int):
            private_keys: list[str] = [PRIVATE_KEYS[WALLETS_TO_WORK - 1]]

        elif isinstance(WALLETS_TO_WORK, tuple):
            private_keys: Sequence[str] = [PRIVATE_KEYS[i - 1] for i in WALLETS_TO_WORK]

        elif isinstance(WALLETS_TO_WORK, list):
            range_count = range(WALLETS_TO_WORK[0], WALLETS_TO_WORK[-1] + 1)
            private_keys: Sequence[str] = [PRIVATE_KEYS[i - 1] for i in range_count]
        else:
            private_keys = []

        if SHUFFLE_WALLETS:
            random.shuffle(private_keys)

        return private_keys

    async def run(self):
        logger.info("Всем привет! Большой благодарностью будет звездочка на Github: https://github.com/StalkerBlack/Plume-Testnet")
        logger.info(
            """ 
            1 - CHECK IN         Регистрация
            2 - VOTING           Голосование
            3 - STONKS           Ставки
            
            """
        )
        private_keys: list[str] = self.get_private_keys()

        while True:
            action = int(input("Выберите действие: "))
            logger.info(f"Вы выбрали {action} действие.")

            for index, private_key in enumerate(private_keys, start=1):
                proxy = await self.get_proxy_for_account(index=index, private_key=private_key)
                logger.info(f"Wallet № {index} | Use Proxy: {bool(proxy)}")

                client = Client(number=index,
                                private_key=private_key,
                                network=GLOBAL_NETWORK,
                                proxy=proxy
                                )

                if action == 1:
                    check_in_worker = CheckInWorker(client=client)
                    await check_in_worker.check_in()

                if action == 2:
                    vote_worker = VoteWorker(client=client)
                    await vote_worker.vote()

                if action == 3:
                    pass

                await self.smart_sleep()


if __name__ == "__main__":
    runner = Runner()
    asyncio.run(runner.run())
