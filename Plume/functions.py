from functools import wraps
from loguru import logger
from typing import Callable
from web3 import AsyncWeb3

from decimal import Decimal

from Plume.tasks.faucet_module import FaucetWorker
from Plume.client import Client


def ensure_sufficient_balance(min_amount: float):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            client: Client = args[0].client
            logger.info(f"Проверяем баланс {client.number} кошелька: {client.address}")
            faucet_worker = FaucetWorker(client=client)

            balance: Decimal = AsyncWeb3.from_wei(
                await client.w3.eth.get_balance(client.address), "ether"
            )
            if balance <= min_amount:
                logger.info(
                    f"Текущий баланс меньше минимального. Пополняем через кран Plume Faucet | Адрес: {client.address}"
                )
                result = await faucet_worker.get_tokens_from_faucet()

                if not result:
                    logger.error(
                        f"Не удалось пополнить баланс {client.number} кошелька: {client.address}"
                    )
                    return False

                logger.success(
                    f"Баланс успешно пополнен. Текущий баланс: {balance} | Минимальный баланс: {min_amount} | Адрес: {client.address}"
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
