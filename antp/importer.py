# Importer imports note types from ../templates/ to Anki.
# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import json
from typing import Any, Collection, Iterable

from .ankiconnect import invoke, request_model_names
from .common import select, get_used_fonts, NoteType, CardTemplate
from .consts import *


def read_css(model_dir_name: str) -> str:
    with open(os.path.join(NOTE_TYPES_DIR, model_dir_name, CSS_FILENAME), encoding='utf8') as f:
        return f.read()


def read_card_templates(model_dir_name: str, template_names: list[str]) -> list[CardTemplate]:
    templates = []
    for template_name in template_names:
        dir_path = os.path.join(NOTE_TYPES_DIR, model_dir_name, template_name)
        with (
            open(os.path.join(dir_path, FRONT_FILENAME), encoding='utf8') as front,
            open(os.path.join(dir_path, BACK_FILENAME), encoding='utf8') as back
        ):
            templates.append(CardTemplate(template_name, front.read(), back.read()))
    return templates


def read_model_dict(model_dir_name: str) -> dict[str, Any]:
    with open(os.path.join(NOTE_TYPES_DIR, model_dir_name, JSON_FILENAME), encoding='utf8') as f:
        return json.load(f)


def read_model(model_dir_name: str) -> NoteType:
    model_dict = read_model_dict(model_dir_name)
    return NoteType(
        name=model_dict['modelName'],
        fields=model_dict['inOrderFields'],
        css=read_css(model_dir_name),
        templates=read_card_templates(model_dir_name, model_dict['cardTemplates']),
    )


def format_import(model: NoteType) -> dict[str, Any]:
    return {
        "modelName": model.name,
        "inOrderFields": model.fields,
        "css": model.css,
        "cardTemplates": [
            {
                "Name": template.name,
                "Front": template.front,
                "Back": template.back,
            }
            for template in model.templates
        ]
    }


def send_note_type(model: NoteType):
    template_json = format_import(model)
    while template_json["modelName"] in request_model_names():
        template_json["modelName"] = input("Model with this name already exists. Enter new name: ")
    invoke("createModel", **template_json)


def available_fonts(required_fonts: Collection[str]) -> Iterable[str]:
    """ Filter required fonts and leave only those available on disk. """
    for file in os.listdir(FONTS_DIR):
        if file in required_fonts:
            yield file


def store_fonts(fonts: list[str]):
    for file in available_fonts(fonts):
        invoke("storeMediaFile", filename=file, path=os.path.join(FONTS_DIR, file))


def import_note_type():
    if model_dir_name := select(os.listdir(NOTE_TYPES_DIR)):
        print(f"Selected model: {model_dir_name}")
        model = read_model(model_dir_name)
        store_fonts(get_used_fonts(model.css))
        send_note_type(model)
        print("Done.")
