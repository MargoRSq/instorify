import codecs
import json
import os


PASS = os.environ['PASS']
LOGIN = os.environ['LOGIN']

COOKIE_PATH = '../cache'
COOCKIE_PATH_PRIVATE = COOKIE_PATH + '/instagram_private_cookie.json'
COOCKIE_PATH_WEB = COOKIE_PATH + '/instagram_web_cookie.json'


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def handle_login(api, cookie_path):
    if not os.path.isdir(COOKIE_PATH):
        os.mkdir(COOKIE_PATH)
    cache_settings = api.settings
    with open(cookie_path, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json, indent='\t')
