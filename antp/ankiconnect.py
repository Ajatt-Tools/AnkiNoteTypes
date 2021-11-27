# Taken from https://github.com/FooSoft/anki-connect
# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

__all__ = ['invoke']

import json
import urllib.request

from .common import ANTPError


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    request_json = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', request_json)))
    if len(response) != 2:
        raise ANTPError('response has an unexpected number of fields')
    if 'error' not in response:
        raise ANTPError('response is missing required error field')
    if 'result' not in response:
        raise ANTPError('response is missing required result field')
    if response['error'] is not None:
        raise ANTPError(response['error'])
    return response['result']
