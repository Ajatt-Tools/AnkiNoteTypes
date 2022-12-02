# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import sys
from typing import Callable
from urllib.error import URLError

from .common import ANTPError
from .exporter import export_note_type
from .importer import import_note_type
from .overwriter import overwrite_note_type
from .updater import update_note_type


def wrap_errors(fn: Callable):
    try:
        fn()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except ANTPError as ex:
        print(ex)
    except KeyboardInterrupt:
        print("\nAborted.")


def print_help():
    options = (
        ("import", "Add one of the stored note types to Anki."),
        ("update", "Overwrite a previously imported note type with new data. "
                   "Fields will not be updated."),
        ("overwrite", "Overwrite a note type in Anki with new data from a stored note type. "
                      "Fields will not be updated."),
        ("export", "Save your note type as a template."),
        ("-v, --verbose", "Show detailed info when errors occur."),
    )
    print(
        "Usage: antp.sh [OPTIONS]\n\n"
        "Options:"
    )
    col_width = [max(len(word) for word in col) + 2 for col in zip(*options)]
    for row in options:
        print(" " * 4, "".join(col.ljust(col_width[i]) for i, col in enumerate(row)), sep='')


def main():
    if len(sys.argv) < 2:
        print("No action provided.")
        print_help()
        return

    action = None
    wrap = True

    for arg in sys.argv[1:]:
        match arg:
            case 'export':
                action = export_note_type
            case 'import':
                action = import_note_type
            case 'update':
                action = update_note_type
            case 'overwrite':
                action = overwrite_note_type
            case '-v' | '--verbose':
                wrap = False

    if action and wrap:
        wrap_errors(action)
    elif action:
        action()
    else:
        print("Unknown action.")
        print_help()


if __name__ == '__main__':
    main()
