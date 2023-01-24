import json
import os
from time import sleep

from instagram_private_api import (Client, ClientCookieExpiredError,
                                   ClientError, ClientLoginError,
                                   ClientThrottledError)

from plugins.instagram.clients.utils import (COOCKIE_PATH_PRIVATE,
                                             from_json,
                                             handle_login_private)
from core.config import (INSTAGRAM_LOGIN,
                         INSTAGRAM_PASS,
                         PLUGINS_ACCOUNTS_MAX_RETRY,
                         PLUGINS_ACCOUNTS_COOKIE_PATH)


def auth_without_settings() -> Client:
    return Client(
        username=INSTAGRAM_LOGIN,
        password=INSTAGRAM_PASS,
        on_login=lambda x: handle_login_private(x, PLUGINS_ACCOUNTS_COOKIE_PATH))


def auth_with_settings(settings) -> Client:
    return Client(
        username=INSTAGRAM_LOGIN,
        password=INSTAGRAM_PASS,
        settings=settings)


def auth(count=0) -> Client:
    try:
        if not os.path.isfile(COOCKIE_PATH_PRIVATE):
            # If cookies exists
            private_api_auth = auth_without_settings()
        else:
            # Create cookies
            with open(COOCKIE_PATH_PRIVATE) as file_data:
                cached_settings_private = json.load(
                    file_data, object_hook=from_json)
                # reuse auth settings
                private_api_auth = auth_with_settings(cached_settings_private)

    except (ClientCookieExpiredError, ClientThrottledError,
            ClientLoginError, ClientError) as error:
        print(f'{count + 1} try', error)

        if count == PLUGINS_ACCOUNTS_MAX_RETRY:
            raise error
        sleep(1)
        auth(count + 1)

    return private_api_auth


private_api = auth()
