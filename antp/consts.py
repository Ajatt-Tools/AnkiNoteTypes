# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os

JSON_INDENT = 4
JSON_FILENAME = 'template.json'
CSS_FILENAME = 'template.css'
FRONT_FILENAME = 'front.html'
BACK_FILENAME = 'back.html'
README_FILENAME = 'README.md'
SCRIPT_DIR = os.path.dirname(__file__)
NOTE_TYPES_DIR = os.path.join(SCRIPT_DIR, os.pardir, 'templates')
FONTS_DIR = os.path.join(SCRIPT_DIR, os.pardir, 'fonts')
