import json
import os

from plugins.instagram.clients.utils import (COOCKIE_PATH_PRIVATE, LOGIN,
                                                 PASS, from_json, handle_login)

from instagram_private_api import (Client, ClientCookieExpiredError,
                                   ClientError, ClientLoginError,
                                   ClientLoginRequiredError)

def auth_without_settings():
    return Client(
                username=LOGIN, 
                password=PASS, 
                on_login=lambda x: handle_login(x, COOCKIE_PATH_PRIVATE))


def auth_with_settings(settings):
    return Client(
                username=LOGIN, 
                password=PASS, 
                settings=settings) 

      
try:

    if not os.path.isfile(COOCKIE_PATH_PRIVATE):
        private_api = auth_without_settings()
    else:
        with open(COOCKIE_PATH_PRIVATE) as file_data:
            cached_settings_private = json.load(file_data, object_hook=from_json)
            # reuse auth settings
            private_api = auth_with_settings(cached_settings_private)
        
except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
    # Login expired
    private_api = auth_without_settings()

except ClientLoginError as e:
    private_api = auth_without_settings()
except ClientError as e:
    private_api = auth_without_settings()
except Exception as e:
    print(e)
    private_api = auth_without_settings()
