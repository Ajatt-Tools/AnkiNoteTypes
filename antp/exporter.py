# Exporter exports note types from Anki to ../templates/
# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import base64
import json
import random
import shutil
from os import DirEntry
from typing import Any

from .ankiconnect import invoke, request_model_names
from .common import NoteType, CardTemplate, get_used_fonts, select
from .consts import *


def fetch_card_templates(model_name: str) -> list[CardTemplate]:
    return [
        CardTemplate(name, val["Front"], val["Back"])
        for name, val in invoke("modelTemplates", modelName=model_name).items()
    ]


def fetch_template(model_name: str) -> NoteType:
    return NoteType(
        name=model_name,
        fields=invoke("modelFieldNames", modelName=model_name),
        css=invoke("modelStyling", modelName=model_name)["css"],
        templates=fetch_card_templates(model_name),
    )


def select_model_dir_path(model_name: str) -> str:
    dir_path = os.path.join(NOTE_TYPES_DIR, model_name)
    dir_content = os.listdir(NOTE_TYPES_DIR)

    if model_name in dir_content:
        ans = input("Template with this name already exists. Overwrite [y/N]? ")
        if ans.lower() != 'y':
            while os.path.basename(dir_path) in dir_content:
                dir_path = os.path.join(NOTE_TYPES_DIR, f"{model_name}_{random.randint(0, 9999)}")

    return dir_path


def write_card_templates(model_dir_path: str, templates: list[CardTemplate]) -> None:
    for template in templates:
        dir_path = os.path.join(model_dir_path, template.name)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        for filename, content in zip((FRONT_FILENAME, BACK_FILENAME), (template.front, template.back)):
            with open(os.path.join(dir_path, filename), 'w', encoding='utf8') as f:
                f.write(content)


def format_export(model: NoteType) -> dict[str, Any]:
    return {
        "modelName": model.name,
        "inOrderFields": model.fields,
        "cardTemplates": [template.name for template in model.templates]
    }


def remove_deleted_templates(model_dir_path: str, templates: list[str]) -> None:
    for entry in os.scandir(model_dir_path):
        entry: DirEntry
        if entry.is_dir() and entry.name not in templates:
            shutil.rmtree(entry.path)


def save_note_type(model: NoteType):
    dir_path = select_model_dir_path(model.name)
    json_path = os.path.join(dir_path, JSON_FILENAME)
    css_path = os.path.join(dir_path, CSS_FILENAME)
    readme_path = os.path.join(dir_path, README_FILENAME)

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    with open(json_path, 'w', encoding='utf8') as f:
        json.dump(format_export(model), f, indent=JSON_INDENT, ensure_ascii=False)

    with open(css_path, 'w', encoding='utf8') as f:
        f.write(model.css)

    write_card_templates(dir_path, model.templates)
    remove_deleted_templates(dir_path, [template.name for template in model.templates])

    if not os.path.isfile(readme_path):
        with open(readme_path, 'w', encoding='utf8') as f:
            f.write(f"# {model.name}\n\n*Description and screenshots here.*")


def save_fonts(model: NoteType) -> None:
    linked_fonts = get_used_fonts(model.css)
    for font in linked_fonts:
        if file_b64 := invoke("retrieveMediaFile", filename=font):
            with open(os.path.join(FONTS_DIR, font), 'bw') as f:
                f.write(base64.b64decode(file_b64))


def export_note_type():
    if model := select(request_model_names()):
        print(f"Selected model: {model}")
        template = fetch_template(model)
        save_fonts(template)
        save_note_type(template)
        print("Done.")
