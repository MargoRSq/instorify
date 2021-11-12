import codecs
import json
import os

from app.core.config import INSTAGRAM_LOGIN, PLUGINS_ACCOUNTS_COOKIE_PATH

COOCKIE_PATH_PRIVATE = PLUGINS_ACCOUNTS_COOKIE_PATH + f'/instagram_private_cookie_{INSTAGRAM_LOGIN}.json'
COOCKIE_PATH_WEB = PLUGINS_ACCOUNTS_COOKIE_PATH + f'/instagram_web_cookie_{INSTAGRAM_LOGIN}.json'


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def handle_login_private(api, PLUGINS_ACCOUNTS_COOKIE_PATH):
    if not os.path.isdir(PLUGINS_ACCOUNTS_COOKIE_PATH):
        os.mkdir(PLUGINS_ACCOUNTS_COOKIE_PATH)
    cache_settings = api.settings
    with open(COOCKIE_PATH_PRIVATE, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json, indent='\t')

def handle_login_web(api, PLUGINS_ACCOUNTS_COOKIE_PATH):
    if not os.path.isdir(PLUGINS_ACCOUNTS_COOKIE_PATH):
        os.mkdir(PLUGINS_ACCOUNTS_COOKIE_PATH)
    cache_settings = api.settings
    with open(COOCKIE_PATH_WEB, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json, indent='\t')