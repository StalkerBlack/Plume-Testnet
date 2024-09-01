import json
import asyncio
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest
from utils import read_json
from data.config import FAUCET


def token_extraction():
    # Настройки CapMonster
    client_options = ClientOptions(api_key="") #Тут нужно вставить API с Cap Monster
    cap_monster_client = CapMonsterClient(options=client_options)


    # Функция для решения CAPTCHA
    async def solve_captcha():
        recaptcha2request = RecaptchaV2ProxylessRequest(
            websiteUrl="https://faucet.plumenetwork.xyz/api/faucet",
            websiteKey="0x4AAAAAAAViEapSHoQXHmzu",  # Ключ сайта reCAPTCHA
        )
        return await cap_monster_client.solve_captcha(recaptcha2request)


    # Получение токена с помощью CAPTCHA решения
    responses = asyncio.run(solve_captcha())
    gRecaptchaResponse = responses.get("gRecaptchaResponse")
    if gRecaptchaResponse:
        try:
            # Преобразование JSON-строки в словарь
            token_data = json.loads(gRecaptchaResponse)
            captcha_token = token_data.get("token")
            if captcha_token:
                print("Полученный токен:", captcha_token)
            else:
                raise ValueError("Токен не найден в ответе.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка при декодировании JSON: {e}")
    else:
        raise ValueError("Ответ не содержит данных reCAPTCHA.")
    
    return captcha_token


def faucet(client):
    web3 = client.w3
    # Настройки контракта
    contract_address = "0x075e2D02EBcea5dbcE6b7C9F3D203613c0D5B33B"
    abi = read_json(FAUCET)

    contract = web3.eth.contract(address=contract_address, abi=abi)

    return contract


