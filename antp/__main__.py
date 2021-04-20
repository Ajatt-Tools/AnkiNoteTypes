from urllib.error import URLError

from antp.exporter import export_note_type

try:
    export_note_type()
except URLError:
    print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
except Exception as ex:
    print(ex)
