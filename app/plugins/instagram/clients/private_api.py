import json
import os

from plugins.instagram.clients.utils import (COOCKIE_PATH_PRIVATE, LOGIN,
                                                 PASS, from_json, handle_login)

from instagram_private_api import (Client, ClientCookieExpiredError,
                                   ClientError, ClientLoginError,
                                   ClientLoginRequiredError)

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
        
except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
    # Login expired
    private_api = Client(
        LOGIN, PASS,
        on_login=lambda x: handle_login(x, COOCKIE_PATH_PRIVATE))

except ClientLoginError as e:
    exit(9)
except ClientError as e:
    exit(9)
except Exception as e:
    exit(99)
