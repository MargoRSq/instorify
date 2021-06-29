import json
import os
from time import sleep

from instagram_private_api import (Client, ClientCookieExpiredError,
                                   ClientError, ClientLoginError,
                                   ClientThrottledError)

from plugins.instagram.clients.utils import (COOCKIE_PATH_PRIVATE, LOGIN, PASS,
                                             from_json, handle_login)

MAX_TRY = 5


def auth_without_settings() -> Client:
    return Client(
        username=LOGIN,
        password=PASS,
        on_login=lambda x: handle_login(x, COOCKIE_PATH_PRIVATE))


def auth_with_settings(settings) -> Client:
    return Client(
        username=LOGIN,
        password=PASS,
        settings=settings)


def auth(count=0) -> Client:
    try:
        if not os.path.isfile(COOCKIE_PATH_PRIVATE):
            # If cookies exists
            private_api = auth_without_settings()
        else:
            # Create cookies
            with open(COOCKIE_PATH_PRIVATE) as file_data:
                cached_settings_private = json.load(
                    file_data, object_hook=from_json)
                # reuse auth settings
                private_api = auth_with_settings(cached_settings_private)

    except (ClientCookieExpiredError, ClientThrottledError,
            ClientLoginError, ClientError, Exception) as e:
        print(f'{count + 1} try', e)

        if count == MAX_TRY:
            raise e
        sleep(1)
        auth(count + 1)

    return private_api


private_api = auth()
