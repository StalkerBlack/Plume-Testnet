import requests
from client import Client
from data.config_accounts import ACCOUNTS
from models import Plume, sleep, print_with_time, check_proxy_ip
from tasks.check_in_module import check_in
from tasks.faucet_module import token_extraction, faucet
from tasks.vote_module import vote_1, vote_2, vote_3
from tasks.cultured_module import cultured


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
