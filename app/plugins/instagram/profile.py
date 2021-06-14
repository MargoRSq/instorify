from instagram_private_api import MediaTypes
import json
from plugins.instagram.clients.private_api import private_api
from plugins.instagram.clients.web_api import web_api
from plugins.instagram.utils import username_to_pk


def fetch_user_info(username: str):
    user = private_api.username_info(username)['user']

    ojbect = {}

    ojbect['id'] = user['pk']
    ojbect['username'] = username
    ojbect['full_name'] = user['full_name']
    ojbect['profile_img'] = user['hd_profile_pic_url_info']['url']
    ojbect['profile_info'] = user['biography']
    ojbect['is_private'] = user['is_private']
    ojbect['is_verified'] = user['is_verified']

    return ojbect
