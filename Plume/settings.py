from models import Plume


"""

GLOBAL_NETWORK         Сеть, в которой работаем (по умолчанию, Plume Network)

SLEEP_MODE = False     True или False | Включает сон после каждого модуля и аккаунта

SLEEP_TIME = (20, 35)   (минимум, максимум) секунд | Время сна между модулями.
"""


GLOBAL_NETWORK = Plume            # Сеть, в которой работаем
SLEEP_MODE = False               # True или False | Включает сон после каждого модуля и аккаунта
SLEEP_TIME = (20, 35)           # (минимум, максимум) секунд | Время сна между модулями.
