# Anki Note Type Picker
import json
import os
import random
from typing import AnyStr
from urllib.error import URLError

from antp.ankiconnect import invoke

JSON_INDENT = 4
SCRIPT_DIR = os.path.dirname(__file__)
NOTE_TYPES_DIR = os.path.join(SCRIPT_DIR, os.pardir, 'templates')


def read_num(msg: str = "Input number: ", min_val: int = 0, max_val: int = None) -> int:
    resp = int(input(msg))
    if resp < min_val or (max_val and resp > max_val):
        raise ValueError("Value out of range.")
    return resp


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


def create_template_dir(template_name) -> AnyStr:
    dir_path = os.path.join(NOTE_TYPES_DIR, template_name)
    dir_content = os.listdir(NOTE_TYPES_DIR)

    if template_name in dir_content:
        ans = input(f"\"{template_name}\" already exists. Overwrite [y/N]?")
        if ans.lower() != 'y':
            while template_name in dir_content:
                dir_path = os.path.join(NOTE_TYPES_DIR, f"{template_name}_{random.randint(0, 9999)}")
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    return dir_path


def save_note_type(template_json):
    template_dir = create_template_dir(template_json["modelName"])
    template_fp = os.path.join(template_dir, 'template.json')
    readme_fp = os.path.join(template_dir, 'README.md')

    with open(template_fp, 'w') as f:
        f.write(json.dumps(template_json, indent=JSON_INDENT))

    with open(readme_fp, 'w') as f:
        f.write(f"# {template_json['modelName']}\n\n*Descriptions and screenshots here.*")


def export_note_type():
    models = invoke('modelNames')
    if not models:
        print("Nothing to show.")
        return
    for idx, model in enumerate(models):
        print(f"{idx}: {model}")
    idx = read_num("\nSelect model number: ", max_val=len(models) - 1)
    model = models[int(idx)]
    print(f"Selected model: {model}")
    save_note_type(fetch_template(model))
    print("Done.")


if __name__ == '__main__':
    try:
        export_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except Exception as ex:
        print(ex)
