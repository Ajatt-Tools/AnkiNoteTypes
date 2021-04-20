import os
from typing import Optional

JSON_INDENT = 4
JSON_FILENAME = 'template.json'
README_FILENAME = 'README.md'
SCRIPT_DIR = os.path.dirname(__file__)
NOTE_TYPES_DIR = os.path.join(SCRIPT_DIR, os.pardir, 'templates')


def read_num(msg: str = "Input number: ", min_val: int = 0, max_val: int = None) -> int:
    resp = int(input(msg))
    if resp < min_val or (max_val and resp > max_val):
        raise ValueError("Value out of range.")
    return resp


def select(items: list[str]) -> Optional[str]:
    if not items:
        print("Nothing to show.")
        return
    for idx, model in enumerate(items):
        print(f"{idx}: {model}")
    idx = read_num("\nSelect model number: ", max_val=len(items) - 1)
    return items[int(idx)]

