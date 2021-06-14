import datetime
import hashlib
import json
import os
import random
import string
from time import sleep

import instagram_web_api

from instagram_web_api import (ClientCookieExpiredError, ClientError,
                               ClientLoginError, ClientThrottledError)
from plugins.instagram.clients.utils import (COOCKIE_PATH_WEB, LOGIN, PASS,
                                             from_json, handle_login)

MAX_TRY = 5
count = 0


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

        params = {
                'username': self.username, 
                'enc_password': enc_password, 
                'queryParams': '{}', 
                'optIntoOneTap': False}
        self._init_rollout_hash()
        
        login_res = self._make_request('https://www.instagram.com/accounts/login/ajax/', params=params)
        if not login_res.get('status', '') == 'ok' or not login_res.get ('authenticated'):
            raise ClientLoginError('Unable to login')

        if self.on_login:
            on_login_callback = self.on_login(self)
        
        return login_res


def auth_without_settings():
    return WebApiClient(
                username=LOGIN, 
                password=PASS, 
                on_login=lambda x: handle_login(x, COOCKIE_PATH_WEB))

def auth_with_settings(settings):
    return WebApiClient(
                username=LOGIN, 
                password=PASS, 
                settings=settings)          

def auth(count):
    try:
        if not os.path.isfile(COOCKIE_PATH_WEB):
            # If cookies exists
            web_api = auth_without_settings()
        else:
            # Create cookies
            with open(COOCKIE_PATH_WEB) as file_data:
                cached_settings_private = json.load(file_data, object_hook=from_json)
                # reuse auth settings
                web_api = auth_with_settings(cached_settings_private)
            
    except (ClientCookieExpiredError, ClientThrottledError, 
            ClientLoginError, ClientError, Exception) as e:
        print(f'{count + 1} try', e)
        
        if count == MAX_TRY:
            exit()
        
        sleep(1)
        auth(count + 1)
    
    return web_api


web_api = auth(count)
