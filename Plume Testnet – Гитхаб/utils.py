import json
from typing import Union, Optional


def read_json(path: str, encoding: Optional[str] = None) -> list | dict:
    return json.load(open(path, encoding=encoding))


def read_list_from_file(filepath):
    """
    Читает строки из файла и возвращает их как список.
    """
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        raise RuntimeError(f"Error reading file {filepath}: {str(e)}")
