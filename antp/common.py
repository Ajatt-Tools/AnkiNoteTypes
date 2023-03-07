# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import dataclasses
import re
from dataclasses import dataclass

from .consts import *


class ANTPError(Exception):
    pass


@dataclass(frozen=True)
class CardTemplate:
    name: str
    front: str
    back: str


@dataclass(frozen=True)
class NoteType:
    name: str
    fields: list[str]
    css: str
    templates: list[CardTemplate]

    def rename(self, new_name: str):
        _d = dataclasses.asdict(self)
        del _d['name']
        return type(self)(name=new_name, **_d)


def read_num(msg: str = "Input number: ", min_val: int = 0, max_val: int = None) -> int:
    try:
        resp = int(input(msg))
    except ValueError as ex:
        raise ANTPError(ex) from ex
    if resp < min_val or (max_val and resp > max_val):
        raise ANTPError("Value out of range.")
    return resp


def select(items: list[str], msg: str = "Select item number: ") -> str | None:
    if not items:
        print("Nothing to show.")
        return

    for idx, model in enumerate(items):
        print(f"{idx}: {model}")
    print()

    idx = read_num(msg, max_val=len(items) - 1)
    return items[idx]


def get_used_fonts(template_css: str):
    return re.findall(r"url\([\"'](\w+\.(?:[ot]tf|woff\d?))[\"']\)", template_css, re.IGNORECASE)


def init():
    from .consts import NOTE_TYPES_DIR, FONTS_DIR

    for path in (NOTE_TYPES_DIR, FONTS_DIR):
        if not os.path.isdir(path):
            os.mkdir(path)


init()
