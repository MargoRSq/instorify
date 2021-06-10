import codecs
import datetime
import hashlib
import json
import os
import random
import string

import instagram_web_api
from instagram_private_api import (Client, ClientCookieExpiredError,
                                   ClientError, ClientLoginError,
                                   ClientLoginRequiredError)
from instagram_private_api import __version__ as client_version

PASS = os.environ['PASS_2']
LOGIN = os.environ['LOGIN_2']
COOCKIE_PATH_PRIVATE = '../cache/instagram_private_cookie.json'
COOCKIE_PATH_WEB = '../cache/instagram_web_cookie.json'


class WebApiClient(instagram_web_api.Client):

    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()

    def login(self):
        """Login to the web site."""
        if not self.username or not self.password:
            raise ClientError('username/password is blank')

        time = str(int(datetime.datetime.now().timestamp()))
        enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}"

        params = {'username': self.username, 'enc_password': enc_password, 'queryParams': '{}', 'optIntoOneTap': False}
        self._init_rollout_hash()
        
        login_res = self._make_request('https://www.instagram.com/accounts/login/ajax/', params=params)
        if not login_res.get('status', '') == 'ok' or not login_res.get ('authenticated'):
            raise ClientLoginError('Unable to login')

        if self.on_login:
            on_login_callback = self.on_login
            on_login_callback(self)
        
        return login_res


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
    cache_settings = api.settings
    with open(cookie_path, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)

try:

    if not os.path.isfile(COOCKIE_PATH_PRIVATE):
        private_api = Client(
            LOGIN, PASS,
            on_login=lambda x: handle_login(x, COOCKIE_PATH_PRIVATE))
    else:
        with open(COOCKIE_PATH_PRIVATE) as file_data:
            cached_settings_private = json.load(file_data, object_hook=from_json)
            # reuse auth settings
            private_api = Client(
                LOGIN, PASS,
                settings=cached_settings_private)
        
    if not os.path.isfile(COOCKIE_PATH_WEB):
        web_api = WebApiClient(
            username=LOGIN, 
            password=PASS, 
            on_login=lambda x: handle_login(x, COOCKIE_PATH_WEB))
        web_api.login()
    else:  
        with open(COOCKIE_PATH_WEB) as file_data:
            cached_settings_web = json.load(file_data, object_hook=from_json)

            web_api = WebApiClient(
                        username=LOGIN, 
                        password=PASS, 
                        settings=cached_settings_web)
            web_api.login()

        
except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
    # Login expired
    device_id = cached_settings_private.get('device_id')
    private_api = Client(
        LOGIN, PASS,
        device_id=device_id,
        on_login=lambda x: handle_login(x, COOCKIE_PATH_PRIVATE))
    

except ClientLoginError as e:
    exit(9)
except ClientError as e:
    exit(9)
except Exception as e:
    exit(99)
