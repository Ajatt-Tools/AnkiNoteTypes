# Importer imports note types from ../templates/ to Anki.

import json
import os
from urllib.error import URLError

import antp.common as ac
from antp.ankiconnect import invoke


def read_template(model_name: str):
    with open(os.path.join(ac.NOTE_TYPES_DIR, model_name, ac.JSON_FILENAME), 'r') as f:
        return json.load(f)


def send_note_type(template_json: dict):
    models = invoke('modelNames')
    while template_json["modelName"] in models:
        template_json["modelName"] = input("Model with this name already exists. Enter new name: ")
    invoke("createModel", **template_json)


def store_fonts(fonts: list[str]):
    for file in os.listdir(ac.FONTS_DIR):
        if file in fonts:
            invoke("storeMediaFile", filename=file, path=os.path.join(ac.FONTS_DIR, file))


def import_note_type():
    model = ac.select(os.listdir(ac.NOTE_TYPES_DIR))
    if not model:
        return
    print(f"Selected model: {model}")
    template = read_template(model)
    store_fonts(ac.get_used_fonts(template['css']))
    send_note_type(template)
    print("Done.")


if __name__ == '__main__':
    try:
        import_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except Exception as ex:
        print(ex)
