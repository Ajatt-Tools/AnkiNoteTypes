# Importer imports note types from ../templates/ to Anki.

import json
import os
from urllib.error import URLError

from antp.ankiconnect import invoke
from antp.common import NOTE_TYPES_DIR, select, JSON_FILENAME


def read_template(model_name):
    with open(os.path.join(NOTE_TYPES_DIR, model_name, JSON_FILENAME), 'r') as f:
        return json.load(f)


def send_note_type(template_json):
    invoke("createModel", **template_json)


def import_note_type():
    model = select(os.listdir(NOTE_TYPES_DIR))
    if not model:
        return
    print(f"Selected model: {model}")
    send_note_type(read_template(model))
    print("Done.")


if __name__ == '__main__':
    try:
        import_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except Exception as ex:
        print(ex)
