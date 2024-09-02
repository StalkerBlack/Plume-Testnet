from utils import read_list_from_file, get_proxies


PRIVATE_KEYS = read_list_from_file(filepath="data/privates.txt")
PROXIES: list[str] = get_proxies(filepath="data/proxies.txt")
