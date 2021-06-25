from models.schemas.instagram import UserInfoObject

from plugins.instagram.clients.private_api import private_api


def fetch_user_info(username: str) -> UserInfoObject:
    user = private_api.username_info(username)['user']

    object = {}

    object['id'] = user['pk']
    object['username'] = username
    object['full_name'] = user['full_name']
    object['profile_img'] = user['hd_profile_pic_url_info']['url']
    object['profile_info'] = user['biography']
    object['is_private'] = user['is_private']
    object['is_verified'] = user['is_verified']
    object['follower_count'] = user['follower_count']
    object['following_count'] = user['following_count']
    object['media_count'] = user['media_count']

    return object
