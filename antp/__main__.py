# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import sys
from urllib.error import URLError

from .common import ANTPError
from .exporter import export_note_type
from .importer import import_note_type
from .updater import update_note_type


def main():
    if len(sys.argv) < 2:
        return print(
            "No action provided.\n\n"
            f"import\tAdd one of the available note types to Anki.\n"
            f"update\tOverwrite a previously imported note type with new data.\n"
            f"export\tSave your note type as a template.\n"
        )

    try:
        match sys.argv[1]:
            case 'export':
                export_note_type()
            case 'import':
                import_note_type()
            case 'update':
                update_note_type()
            case _:
                print("Unknown action.")
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except ANTPError as ex:
        print(ex)


if __name__ == '__main__':
    main()
