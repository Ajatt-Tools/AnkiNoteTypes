# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import sys
from urllib.error import URLError

from .common import ANTPError
from .exporter import export_note_type
from .importer import import_note_type


def main():
    try:
        if len(sys.argv) < 2:
            print("No action provided.\n")
            print(f"import\tAdd one of the available note types to Anki.")
            print(f"export\tSave your note type as a template.")
        elif (cmd := sys.argv[1]) == 'export':
            export_note_type()
        elif cmd == 'import':
            import_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except ANTPError as ex:
        print(ex)


if __name__ == '__main__':
    main()
