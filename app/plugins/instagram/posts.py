from pprint import pprint
from instagram_private_api import MediaTypes
import json
from plugins.instagram.clients.private_api import private_api
from plugins.instagram.clients.web_api import web_api
from plugins.instagram.utils import username_to_pk

from pprint import pprint

def carousel_item(item: dict) -> list:
    items = []
    for media in item['carousel_media']:
        object = {}
        if 'video_duration' in media:
            object.update(video_item(media))

        else:
            object.update(photo_item(media))
        items.append(object)
    return items

def video_item(item: dict) -> dict:
    object = {}
    object['content_url'] = item['video_versions'][0]['url']
    object['type'] = MediaTypes.VIDEO
    object['duration'] = item['video_duration']

    return object

def photo_item(item: dict) -> dict:

    height = None
    width = None
    object = {}
    if 'original_height' in item:
        height = item['original_height']
        object['height'] = height
    if 'original_width' in item:
        width = item['original_width']
        object['width'] = width

    if height and width:
        for image in item['image_versions2']['candidates']:
            if height == image['height'] and width == image['width']:
                object['content_url'] = image['url']
                object['type'] = MediaTypes.PHOTO
    else:
        max_height = 0
        for image in item['image_versions2']['candidates']:
            if height > max_height:
                object['content_url'] = image['url']
                object['type'] = MediaTypes.PHOTO

    return object


def post_items_raw_to_object(items: list) -> list[dict]:
    objects = []

    for item in items:
        object = {}

        if 'created_at' in item:
            object['created_at'] = item['caption']['created_at']
        object['like_count'] = item['like_count']

        object['id'] = int(item['id'])

        if 'video_duration' in item:
            object.update(video_item(item))

        elif 'carousel_media' in item:
            object['type'] = MediaTypes.CAROUSEL
            object['items'] = carousel_item(item)
        else:
            object.update(photo_item(item))

        objects.append(object)

    return objects

def fetch_posts(username: str)  -> list[dict]:
    posts = private_api.username_feed(username)
    is_next = posts['more_available']

    items = [*posts['items']]
    while is_next:
        next_max_id = posts['next_max_id']
        posts = private_api.username_feed(username, max_id=next_max_id)
        is_next = posts['more_available']
        items = [*items, *posts['items']]

    objects = post_items_raw_to_object(items)

    return objects

def fetch_one_post(username: str, index: int) -> dict:
    posts = private_api.username_feed(username)
    media_count = private_api.username_info(username)['user']['media_count']
    items = [*posts['items']]

    count = len(items)

    if len(items) >= index:
        obj = items[index - 1]
        objects = post_items_raw_to_object([obj])
        return objects[0]
    elif index >= len(items) and index <= media_count:
        is_next = posts['more_available']
        while is_next:
            next_max_id = posts['next_max_id']
            posts = private_api.username_feed(username, max_id=next_max_id)
            is_next = posts['more_available']
            items = [*items, *posts['items']]

            count+= len(items)
            if count >= index:
                obj = items[index - 1]
                pprint(obj)
                objects = post_items_raw_to_object([obj])
                return objects[0]
    else:
        return None
