# Updater updates previously imported note types.
# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from typing import Any

from .ankiconnect import invoke, request_model_names
from .common import select, get_used_fonts, NoteType
from .consts import *
from .importer import read_model_dict, read_model, store_fonts


def read_model_name(model_dir_name: str) -> str:
    return read_model_dict(model_dir_name)['modelName']


def format_templates(model: NoteType) -> dict[str, Any]:
    return {
        "model": {
            "name": model.name,
            "templates": {
                template.name: {"Front": template.front, "Back": template.back} for template in model.templates
            }
        }
    }


def format_styling(model: NoteType) -> dict[str, Any]:
    return {
        "model": {
            "name": model.name,
            "css": model.css
        }
    }


def send_note_type(model: NoteType):
    invoke("updateModelTemplates", **format_templates(model))
    invoke("updateModelStyling", **format_styling(model))


def update_note_type():
    anki_models = set(request_model_names())
    dir_names = [dir_name for dir_name in os.listdir(NOTE_TYPES_DIR)
                 if read_model_name(dir_name) in anki_models]
    if not dir_names:
        print("No note types can be updated.")
        return
    if model_dir_name := select(dir_names):
        print(f"Selected note type: {model_dir_name}")
        model = read_model(model_dir_name)
        store_fonts(get_used_fonts(model.css))
        send_note_type(model)
        print("Done.")
