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

from app.plugins.instagram.clients.utils import (COOCKIE_PATH_WEB,
                                             from_json,
                                             handle_login_web)
from app.core.config import INSTAGRAM_LOGIN, INSTAGRAM_PASS, PLUGINS_ACCOUNTS_MAX_RETRY, PLUGINS_ACCOUNTS_COOKIE_PATH


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

        login_res = self._make_request(
            'https://www.instagram.com/accounts/login/ajax/', params=params)
        if not login_res.get('status', '') == 'ok' or not login_res.get('authenticated'):
            raise ClientLoginError('Unable to login')

        if self.on_login:
            self.on_login(self)

        return login_res


def auth_without_settings() -> WebApiClient:
    return WebApiClient(
        username=INSTAGRAM_LOGIN,
        password=INSTAGRAM_PASS,
        on_login=lambda x: handle_login_web(x, PLUGINS_ACCOUNTS_COOKIE_PATH))


def auth_with_settings(settings) -> WebApiClient:
    return WebApiClient(
        username=INSTAGRAM_LOGIN,
        password=INSTAGRAM_PASS,
        settings=settings)


def auth(count=0) -> WebApiClient:
    try:
        if not os.path.isfile(COOCKIE_PATH_WEB):
            # If cookies exists
            web_api = auth_without_settings()
        else:
            # Create cookies
            with open(COOCKIE_PATH_WEB) as file_data:
                cached_settings_private = json.load(
                    file_data, object_hook=from_json)
                # Reuse auth settings
                web_api = auth_with_settings(cached_settings_private)

    except (ClientCookieExpiredError, ClientThrottledError,
            ClientLoginError, ClientError, Exception) as e:
        print(f'{count + 1} try |', e)

        if count == PLUGINS_ACCOUNTS_MAX_RETRY:
            raise e

        sleep(1)
        auth(count + 1)

    return web_api


web_api = auth()
