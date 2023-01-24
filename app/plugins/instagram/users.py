from models.schemas.instagram import User
from plugins.instagram.clients.private_api import private_api


def fetch_user_info(username: str) -> User:
    user = private_api.username_info(username)['user']

    obj = {}

    obj['id'] = user['pk']
    obj['username'] = username
    obj['full_name'] = user['full_name']
    obj['profile_img'] = user['hd_profile_pic_url_info']['url']
    if user['biography']:
        obj['profile_info'] = user['biography']
    obj['is_private'] = user['is_private']
    obj['is_verified'] = user['is_verified']
    obj['follower_count'] = user['follower_count']
    obj['following_count'] = user['following_count']
    obj['media_count'] = user['media_count']

    return obj
