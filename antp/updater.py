from typing import Any

from .ankiconnect import invoke, request_model_names
from .common import select, get_used_fonts, NoteType
from .consts import *
from .importer import read_model, store_fonts


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
    if model_dir_name := select(os.listdir(NOTE_TYPES_DIR)):
        print(f"Selected model: {model_dir_name}")
        model = read_model(model_dir_name)
        if model.name in request_model_names():
            store_fonts(get_used_fonts(model.css))
            send_note_type(model)
            print("Done.")
        else:
            print("This note type hasn't been imported yet. Aborted.")
