import aiohttp
import asyncio
import certifi
import json
import ssl


from loguru import logger
from typing import Any
from web3 import Web3
from web3.eth.async_eth import AsyncContract, ChecksumAddress
from web3.exceptions import Web3RPCError

from Plume.client import Client
from Plume.config import CAP_MONSTER_API
from Plume.utils import read_json
from Plume.data.config import FAUCET


class FaucetWorker:
    def __init__(self, client: Client):
        self.client: Client = client
        self.abi = read_json(FAUCET)
        self.counter: int = 0

    async def check_balance(self):
        """
        Проверяем баланс на сайте
        """
        try:
            async with aiohttp.ClientSession() as session:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                response = await session.post(
                    url="https://api.capmonster.cloud/getBalance",
                    json={"clientKey": CAP_MONSTER_API},
                    ssl=ssl_context,
                )
                response_bytes: bytes = await response.read()

                response_text: str = response_bytes.decode("utf-8")
                response_json: dict[str, Any] = json.loads(response_text)

                if response_json["errorId"] == 0:
                    if float(response_json["balance"]) <= 0.01:
                        logger.info(
                            f"Недостаточно денег для решения капч Capmonster! Пополните баланс"
                        )
                else:
                    logger.error(f"Произошла ошибка {response_json['errorCode']}")

                return True

        except aiohttp.ClientError as error:
            logger.error(f"Ошибка сети при проверке баланса: {error}")

        except json.JSONDecodeError:
            logger.error("Ошибка при разборе JSON ответа от CapMonster API")

        except Exception as error:
            logger.error(f"Непредвиденная ошибка при проверке баланса: {error}")

        return False

    async def send_captcha(self):
        """
        Отправляем запрос на решение капчи
        """
        try:
            async with aiohttp.ClientSession() as session:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                response: aiohttp.ClientResponse = await session.post(
                    url="https://api.capmonster.cloud/createTask",
                    json={
                        "clientKey": CAP_MONSTER_API,
                        "task": {
                            "type": "TurnstileTask",
                            "websiteURL": "https://miles.plumenetwork.xyz/faucet",
                            "websiteKey": "0x4AAAAAAAViEapSHoQXHmzu",
                            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                        },
                    },
                    ssl=ssl_context,
                )
                if not response:
                    logger.error(f"Нет ответа от API CapMonster. ")
                    return False

                response_bytes: bytes = await response.read()
                response_text: str = response_bytes.decode("utf-8")
                response_json: dict[str, Any] = json.loads(response_text)

                if response_json["errorId"] == 0:
                    return response_json["taskId"]

                logger.error(f"Ошибка API CapMonster: {response_json['errorCode']}")
                return False

        except aiohttp.ClientError as error:
            logger.error(f"Ошибка сети при отправке капчи: {error}")

        except json.JSONDecodeError:
            logger.error("Ошибка при разборе JSON ответа от CapMonster API")

        except Exception as error:
            logger.error(f"Непредвиденная ошибка при отправке капчи: {error}")

        return False

    async def result_captcha(self, taskId: int):
        """
        Разгадываем капчу
        """
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())

            async with aiohttp.ClientSession() as session:
                while True:
                    if self.counter >= 40:
                        logger.error(
                            f"Превышено время ожидания решения капчи ( >40 секунд )"
                        )
                        return False

                    response: aiohttp.ClientResponse = await session.post(
                        url="https://api.capmonster.cloud/getTaskResult",
                        json={"clientKey": CAP_MONSTER_API, "taskId": taskId},
                        ssl=ssl_context,
                    )
                    if response:
                        response_bytes: bytes = await response.read()
                        response_text: str = response_bytes.decode("utf-8")
                        response_json: dict[str, Any] = json.loads(response_text)

                        if response_json["status"] == "processing":
                            await asyncio.sleep(3)
                            self.counter += 1
                            continue

                        elif response_json["status"] == "ready":
                            return response_json["solution"]

                        else:
                            logger.error(
                                f"Ошибка получения результата капчи: {response_json}"
                            )
                            return False

        except aiohttp.ClientError as error:
            logger.error(f"Ошибка сети при получении результата капчи: {error}")

        except json.JSONDecodeError:
            logger.error("Ошибка при разборе JSON ответа от CapMonster API")

        except Exception as error:
            logger.error(
                f"Непредвиденная ошибка при получении результата капчи: {error}"
            )

        return False

    async def get_tokens_from_faucet(self):
        if not await self.check_balance():
            pass

        taskId = await self.send_captcha()
        if not taskId:
            logger.error(f"Не удалось создать задачу для решения капчи.")

        result = await self.result_captcha(taskId=taskId)

        if not result:
            logger.error(f"Не удалось пройти капчу!")

        token = result["token"]

        payload = {
            "token": "ETH",
            "verified": token,
            "walletAddress": self.client.address,
        }
        headers: dict[str, str] = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://faucet.plumenetwork.xyz",
            "Referer": "https://faucet.plumenetwork.xyz/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await session.post(
                url="https://faucet.plumenetwork.xyz/api/faucet",
                json=payload,
                proxy=self.client.proxy,
                headers=headers,
                ssl=ssl_context,
            )

            response_bytes: bytes = await response.read()
            response_text: str = response_bytes.decode("utf-8")
            response_json: dict[str, Any] = json.loads(response_text)

        if "error" in response_json:
            raise ValueError(f"API вернул ошибку: {response_json['error']}")

        if "salt" in response_json and "signature" in response_json:
            salt = response_json["salt"]
            signature = response_json["signature"]

            IMPLEMENTATION_CONTRACT_ADDRESS: ChecksumAddress = Web3.to_checksum_address(
                "0x075e2D02EBcea5dbcE6b7C9F3D203613c0D5B33B"
            )

            implementation_contract: AsyncContract = self.client.w3.eth.contract(
                address=IMPLEMENTATION_CONTRACT_ADDRESS, abi=self.abi
            )

            faucet_data = implementation_contract.functions.getToken(
                "ETH", salt, signature
            )._encode_transaction_data()

            try:
                tx_hash = await self.client.send_transaction(
                    to=IMPLEMENTATION_CONTRACT_ADDRESS, data=faucet_data
                )
            except Exception as error:
                logger.error(
                    f"Не удалось получить тестовые токены на {self.client.number} кошельке: {self.client.address} | Error: {error}"
                )
                return False

            if tx_hash:
                logger.success(
                    f"Хэш транзакции: {self.client.network.explorer + tx_hash} | Адрес: {self.client.address}"
                )
                return True

        else:
            raise ValueError(
                f"Ответ от API не содержит 'salt' или 'signature'. Ответ: {response_json}"
            )
