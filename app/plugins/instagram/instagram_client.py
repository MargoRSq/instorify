import os
import json
import codecs

from instagram_private_api import (
    Client, ClientError, ClientLoginError,
    ClientCookieExpiredError, ClientLoginRequiredError,
    __version__ as client_version)


PASS = os.environ['PASS']
LOGIN = os.environ['LOGIN']
COOCKIE_PATH = '../cache/instagram_cookie.json'


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def handle_login():
    cache_settings = api.settings
    with open(COOCKIE_PATH, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)

try:

    if not os.path.isfile(COOCKIE_PATH):

        # login new
        api = Client(
            LOGIN, PASS,
            on_login=lambda x: handle_login(x, COOCKIE_PATH))
    else:
        with open(COOCKIE_PATH) as file_data:
            cached_settings = json.load(file_data, object_hook=from_json)

        # reuse auth settings
        api = Client(
            LOGIN, PASS,
            settings=cached_settings)

except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
    # Login expired
    # Do relogin but use default ua, keys and such
    device_id = cached_settings.get('device_id')
    api = Client(
        LOGIN, PASS,
        device_id=device_id,
        on_login=handle_login)

except ClientLoginError as e:
    exit(9)
except ClientError as e:
    exit(9)
except Exception as e:
    exit(99)
