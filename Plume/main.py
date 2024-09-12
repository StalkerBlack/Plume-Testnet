import asyncio
import random
import sys


from datetime import timedelta, datetime
from loguru import logger
from typing import Sequence, Dict

from client import Client
from config import PRIVATE_KEYS, PROXIES
from tasks.check_in_module import CheckInWorker
from tasks.faucet_module import FaucetWorker
from tasks.vote_module import VoteWorker
from tasks.rwa_deploy_module import RWADeployWorker
from tasks.cultured_module import CulturedWorker


from settings import (
    GLOBAL_NETWORK,
    SLEEP_MODE,
    SLEEP_TIME,
    WALLETS_TO_WORK,
    SHUFFLE_WALLETS,
)


logger.remove()
logger.add(
    sink=sys.stdout,
    backtrace=True,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>",
)


class Runner:

    async def get_proxy_for_account(self, index: int, private_key: str):
        try:
            private_key_index = PRIVATE_KEYS.index(private_key)
            return PROXIES[private_key_index % len(PROXIES)]

        except Exception as error:
            logger.info(f"{index} кошелек запускается без прокси: {error}")

    async def smart_sleep(self, address: str):
        if SLEEP_MODE:
            duration = random.randint(*SLEEP_TIME)
            next_run_time = datetime.now() + timedelta(seconds=duration)
            logger.info(
                f"💤 Следующее действие для кошелька {address} будет выполнено: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
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
        logger.info(f"Запуск софта")
        logger.info(
            "Всем привет! Большой благодарностью будет звездочка на Github: https://github.com/StalkerBlack/Plume-Testnet"
        )
        logger.info(
            """
            1 - CHECK IN           Регистрация
            2 - VOTING             Голосование
            3 - STONKS             Ставки
            4 - CREATE TOKEN (NFT) Создание Токена

            """
        )
        self.private_keys: list[str] = self.get_private_keys().copy()
        logger.info(f"Получено приватных ключей: {len(self.private_keys)}")

        actions_hashmap: Dict[int, str] = {
            1: "Check In",
            2: "Voting",
            # 3: "Faucet",
            4: "RWA Create Token",
            5: "Cultured"
        }
        index = 0

        while self.private_keys:
            wallet_index: int = random.choice(range(len(self.private_keys)))
            private_key: str = self.private_keys.pop(wallet_index)

            available_actions: Dict[int, str] = actions_hashmap.copy()

            while available_actions:
                action: int = random.choice(list(available_actions.keys()))
                module_name: str = available_actions.pop(action)
                proxy = await self.get_proxy_for_account(
                    index=wallet_index, private_key=private_key
                )
                logger.info(
                    f"{index} | Wallet № {wallet_index + 1} | Action № {action} | Use Proxy: {bool(proxy)}"
                )

                client = Client(
                    number=wallet_index + 1,
                    private_key=private_key,
                    network=GLOBAL_NETWORK,
                    proxy=proxy,
                )

                if action == 1:
                    logger.info(
                        f"Запуск {module_name} для {client.number} кошелька | Адрес: {client.address}"
                    )
                    check_in_worker = CheckInWorker(client=client)
                    result = await check_in_worker.check_in()
                    if not result:
                        logger.info(
                            f"{module_name} для {client.number} кошелька ранее был выполнен! Переход к следующему действию.\n"
                            f"Адрес: {client.address}"
                        )
                        continue

                if action == 2:
                    logger.info(
                        f"Запуск {module_name} для {client.number} кошелька | Адрес: {client.address}"
                    )
                    vote_worker = VoteWorker(client=client)
                    result = await vote_worker.vote()
                    if not result:
                        logger.info(
                            f"{module_name} для {client.number} кошелька ранее был выполнен! Переход к следующему действию.\n"
                            f"Адрес: {client.address}"
                        )
                        continue

                if action == 3:
                    logger.info(
                        f"Запуск {module_name} для {client.number} кошелька | Адрес: {client.address}"
                    )
                    faucet_worker = FaucetWorker(client=client)
                    try:
                        await faucet_worker.get_tokens_from_faucet()

                    except Exception as error:
                        logger.info(
                            f"Возникла ошибка в процессе работы {module_name} для {client.number} кошелька | Адрес: {client.address} | Ошибка: {str(error)}"
                        )

                if action == 4:
                    logger.info(
                        f"Запуск {module_name} для {client.number} кошелька | Адрес: {client.address}"
                    )
                    deploy_worker = RWADeployWorker(client=client)
                    result = await deploy_worker.deploy()
                    if not result:
                        logger.info(
                            f"{module_name} для {client.number} кошелька ранее был выполнен! Переход к следующему действию.\n"
                            f"Адрес: {client.address}"
                        )
                        continue

                if action == 5:
                    logger.info(
                        f"Запуск {module_name} для {client.number} кошелька | Адрес: {client.address}"
                    )
                    cultured_worker = CulturedWorker(client=client)
                    result = await cultured_worker.cultured()
                    if result:
                        logger.success(
                            f"Сделали всевозможные prediction для модуля {module_name} на {client.number} кошельке | Адрес: {client.address}"
                        )
                    else:
                        logger.info(
                            f"Возникла ошибка в процессе работы {module_name} для {client.number} кошелька | Адрес: {client.address}"
                        )
                        continue

                await self.smart_sleep(client.address)

            index += 1


if __name__ == "__main__":
    runner = Runner()
    asyncio.run(runner.run())
