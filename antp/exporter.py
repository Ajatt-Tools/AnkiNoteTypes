# Exporter exports note types from Anki to ../templates/

import base64
import json
import os
import random
from typing import AnyStr
from urllib.error import URLError

import antp.common as ac
from antp.ankiconnect import invoke


def fetch_card_templates(model_name: str):
    card_templates = []
    for key, val in invoke("modelTemplates", modelName=model_name).items():
        card_templates.append({
            "Name": key,
            "Front": val["Front"],
            "Back": val["Back"],
        })
    return card_templates


def fetch_template(model_name: str):
    return {
        "modelName": model_name,
        "inOrderFields": invoke("modelFieldNames", modelName=model_name),
        "css": invoke("modelStyling", modelName=model_name)["css"],
        "cardTemplates": fetch_card_templates(model_name),
    }


def create_template_dir(template_name: str) -> AnyStr:
    dir_path = os.path.join(ac.NOTE_TYPES_DIR, template_name)
    dir_content = os.listdir(ac.NOTE_TYPES_DIR)

    if template_name in dir_content:
        ans = input("Template with this name already exists. Overwrite [y/N]? ")
        if ans.lower() != 'y':
            while os.path.basename(dir_path) in dir_content:
                dir_path = os.path.join(ac.NOTE_TYPES_DIR, f"{template_name}_{random.randint(0, 9999)}")
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    return dir_path


def save_note_type(template_json: dict):
    template_dir = create_template_dir(template_json["modelName"])
    template_fp = os.path.join(template_dir, ac.JSON_FILENAME)
    readme_fp = os.path.join(template_dir, ac.README_FILENAME)

    with open(template_fp, 'w') as f:
        f.write(json.dumps(template_json, indent=ac.JSON_INDENT))

    if not os.path.isfile(readme_fp):
        with open(readme_fp, 'w') as f:
            f.write(f"# {template_json['modelName']}\n\n*Description and screenshots here.*")


def save_fonts(template_json: dict):
    linked_fonts = ac.get_used_fonts(template_json['css'])
    for font in linked_fonts:
        file_b64 = invoke("retrieveMediaFile", filename=font)
        if file_b64 is False:
            continue
        with open(os.path.join(ac.FONTS_DIR, font), 'bw') as f:
            f.write(base64.b64decode(file_b64))


def export_note_type():
    model = ac.select(invoke('modelNames'))
    if not model:
        return
    print(f"Selected model: {model}")
    template = fetch_template(model)
    save_fonts(template)
    save_note_type(template)
    print("Done.")


if __name__ == '__main__':
    try:
        export_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except Exception as ex:
        print(ex)
