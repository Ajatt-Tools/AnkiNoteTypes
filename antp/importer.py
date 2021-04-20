# Importer imports note types from ../templates/ to Anki.

import json
import os
from urllib.error import URLError

from antp.ankiconnect import invoke
from antp.common import NOTE_TYPES_DIR, select, JSON_FILENAME, FONTS_DIR, get_used_fonts


def read_template(model_name: str):
    with open(os.path.join(NOTE_TYPES_DIR, model_name, JSON_FILENAME), 'r') as f:
        return json.load(f)


def send_note_type(template_json: dict):
    models = invoke('modelNames')
    while template_json["modelName"] in models:
        template_json["modelName"] = input("Model with this name already exists. Enter new name: ")
    invoke("createModel", **template_json)


def store_fonts(fonts: list[str]):
    for file in os.listdir(FONTS_DIR):
        if file in fonts:
            invoke("storeMediaFile", filename=file, path=os.path.join(FONTS_DIR, file))


def import_note_type():
    model = select(os.listdir(NOTE_TYPES_DIR))
    if not model:
        return
    print(f"Selected model: {model}")
    template = read_template(model)
    store_fonts(get_used_fonts(template['css']))
    send_note_type(template)
    print("Done.")


if __name__ == '__main__':
    try:
        import_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except Exception as ex:
        print(ex)
