# Anki Note Type Picker
import json
from urllib.error import URLError

from ankiconnect import invoke

JSON_INDENT = 4


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
    template = fetch_template(model)
    print(json.dumps(template, indent=JSON_INDENT))


if __name__ == '__main__':
    try:
        export_note_type()
    except URLError:
        print("Couldn't connect. Make sure Anki is open and AnkiConnect is installed.")
    except Exception as ex:
        print(ex)
