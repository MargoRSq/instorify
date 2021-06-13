import json
import os

from plugins.instagram.clients.utils import (COOCKIE_PATH_PRIVATE, LOGIN,
                                                 PASS, from_json, handle_login, handle_login_refresh)

from instagram_private_api import (Client, ClientCookieExpiredError,
                                   ClientError, ClientLoginError,
                                   ClientLoginRequiredError, ClientThrottledError)

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

def auth_refresh():
    os.remove(COOCKIE_PATH_PRIVATE)
    return Client(
                username=LOGIN, 
                password=PASS, 
                on_login=lambda x: handle_login_refresh(x, COOCKIE_PATH_PRIVATE))

def auth():
    try:
        if not os.path.isfile(COOCKIE_PATH_PRIVATE):
            # If cookies exists
            private_api = auth_without_settings()
        else:
            # Create cookies
            with open(COOCKIE_PATH_PRIVATE) as file_data:
                cached_settings_private = json.load(file_data, object_hook=from_json)
                # reuse auth settings
                private_api = auth_with_settings(cached_settings_private)
            
    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print(e)
        # Login expired
        private_api = auth_without_settings()
    except ClientThrottledError as e:
        print(e)
        # Please wait a few minutes before you try again
        private_api = auth_refresh()
    except ClientLoginError as e:
        print(e)
        # Raised when login fails
        private_api = auth_without_settings()
    except ClientError as e:
        print(e)
        # Other login errors
        private_api = auth_without_settings()
    except Exception as e:
        print(e)
        exit()

    return private_api

      
private_api = auth()
