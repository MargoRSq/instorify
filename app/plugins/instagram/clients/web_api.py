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

from plugins.instagram.clients.utils import (COOCKIE_PATH_WEB, LOGIN, PASS,
                                                 from_json, handle_login)

class WebApiClient(instagram_web_api.Client):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login()

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


try:

    if not os.path.isfile(COOCKIE_PATH_WEB):
        web_api = WebApiClient(
            username=LOGIN, 
            password=PASS, 
            on_login=lambda x: handle_login(x, COOCKIE_PATH_WEB))
    else:  
        with open(COOCKIE_PATH_WEB) as file_data:
            cached_settings_web = json.load(file_data, object_hook=from_json)
            # reuse auth settings
            web_api = WebApiClient(
                        username=LOGIN, 
                        password=PASS, 
                        settings=cached_settings_web)
        
except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
    # Login expired
    web_api = WebApiClient(
            username=LOGIN, 
            password=PASS, 
            on_login=lambda x: handle_login(x, COOCKIE_PATH_WEB))

except ClientLoginError as e:
    exit(9)
except ClientError as e:
    exit(9)
except Exception as e:
    exit(99)
