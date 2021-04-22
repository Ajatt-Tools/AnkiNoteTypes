import os
import re
from typing import Optional

JSON_INDENT = 4
JSON_FILENAME = 'template.json'
README_FILENAME = 'README.md'
SCRIPT_DIR = os.path.dirname(__file__)
NOTE_TYPES_DIR = os.path.join(SCRIPT_DIR, os.pardir, 'templates')
FONTS_DIR = os.path.join(SCRIPT_DIR, os.pardir, 'fonts')

if not os.path.isdir(FONTS_DIR):
    os.mkdir(FONTS_DIR)


def read_num(msg: str = "Input number: ", min_val: int = 0, max_val: int = None) -> int:
    resp = int(input(msg))
    if resp < min_val or (max_val and resp > max_val):
        raise ValueError("Value out of range.")
    return resp


def select(items: list[str], msg: str = "Select item number: ") -> Optional[str]:
    if not items:
        print("Nothing to show.")
        return

    for idx, model in enumerate(items):
        print(f"{idx}: {model}")
    print()

    idx = read_num(msg, max_val=len(items) - 1)
    return items[idx]


def get_used_fonts(template_css: str):
    return re.findall(r"url\([\"'](\w+\.[ot]tf)[\"']\)", template_css, re.IGNORECASE)
