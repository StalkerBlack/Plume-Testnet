import json
import os


from better_proxy import Proxy
from typing import Union, Optional


def read_json(path: str, encoding: Optional[str] = None) -> list | dict:
    return json.load(open(path, encoding=encoding))


def read_list_from_file(filepath) -> list[str]:
    """
    Читает строки из файла и возвращает их как список.
    """
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    except Exception as e:
        raise RuntimeError(f"Error reading file {filepath}: {str(e)}")


def get_proxies(filepath: str, mode: str = "r") -> list[str]:
    if os.path.exists(filepath):
        return [Proxy.from_str(proxy=row.strip()
        if '://' in row.strip() else f'http://{row.strip()}').as_url or None
        for row in open(filepath, mode) if row]
