# Overwriter acts like Updater but allows mapping models with different names.
# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from .ankiconnect import request_model_names
from .common import select, get_used_fonts
from .consts import *
from .importer import read_model, store_fonts
from .updater import send_note_type


def overwrite_note_type():
    anki_models = request_model_names()
    models_on_disk = {
        (model := read_model(dir_name)).name: model
        for dir_name in os.listdir(NOTE_TYPES_DIR)
    }
    model_name_on_disk = select(list(models_on_disk), "Take stored model: ")
    model_name_in_anki = select(anki_models, "Replace templates in model: ")

    print(f"Writing templates from {model_name_on_disk} onto {model_name_in_anki}...")

    model = models_on_disk[model_name_on_disk]
    store_fonts(get_used_fonts(model.css))
    send_note_type(model.rename(model_name_in_anki))

    print("Done.")
