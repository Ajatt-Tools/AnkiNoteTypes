from urllib.error import URLError
import sys
from antp.exporter import export_note_type
from antp.importer import import_note_type


def main():
    try:
        if len(sys.argv) < 2:
            print("No action provided.")
            return
        cmd = sys.argv[1]
        if cmd == 'export':
            export_note_type()
        elif cmd == 'import':
            import_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
