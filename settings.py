from models import Plume


"""

GLOBAL_NETWORK                Сеть, в которой работаем (по умолчанию, Plume Network)

SLEEP_MODE = False            True или False | Включает сон после каждого модуля и аккаунта

SLEEP_MODE = True             True или False | Включает сон после каждого модуля и кошелька

SLEEP_TIME = (3600, 86400)    (минимум, максимум) секунд | Время сна между кошельками.

SHUFFLE_WALLETS = False                     # Перемешать кошельки или нет

WALLETS_TO_WORK: int | tuple | list = 0     # 0 - все кошельки

"""


GLOBAL_NETWORK = Plume                   # Сеть, в которой работаем
SLEEP_MODE = True                        # True или False | Включает сон после каждого отработанного кошелька
SLEEP_TIME = (490, 1400)                 # (минимум, максимум) секунд | Время сна между модулями.


SHUFFLE_WALLETS = False                  # Перемешать кошельки или нет
WALLETS_TO_WORK: int | tuple | list = 0  # 0 - все кошельки
                                         # 1 - кошелек 1
                                         # 1, 7 - кошельки 1 и 7
                                         # [5, 25] - с 5 по 25 кошельки включительно
