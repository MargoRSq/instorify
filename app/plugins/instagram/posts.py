from instagram_private_api import MediaTypes
import json
from plugins.instagram.clients.private_api import private_api
from plugins.instagram.clients.web_api import web_api
from plugins.instagram.utils import username_to_pk


def fetch_user_info(username: str) -> dict:
    user = private_api.username_info(username)['user']

    object = {}

    object['id'] = user['pk']
    object['username'] = username
    object['full_name'] = user['full_name']
    object['profile_img'] = user['hd_profile_pic_url_info']['url']
    object['profile_info'] = user['biography']
    object['is_private'] = user['is_private']
    object['is_verified'] = user['is_verified']

    return object
