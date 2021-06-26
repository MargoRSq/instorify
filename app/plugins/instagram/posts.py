from instagram_private_api import MediaTypes
from plugins.instagram.clients.private_api import private_api


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
    else:
        max_height = 0
        for image in item['image_versions2']['candidates']:
            if height > max_height:
                object['content_url'] = image['url']

    return object


def post_items_raw_to_object(items: list) -> list[dict]:
    objects = []

    for item in items:
        object = {}

        if 'taken_at' in item:
            object['created_at'] = item['taken_at']
        if 'view_count' in item:
            object['view_count'] = item['view_count']

        object['like_count'] = item['like_count']
        object['id'] = item['id']

        if item['media_type'] == MediaTypes.VIDEO:
            object['type'] = MediaTypes.VIDEO
            object.update(video_item(item))

        elif item['media_type'] == MediaTypes.CAROUSEL:
            object['type'] = MediaTypes.CAROUSEL
            object['items'] = carousel_item(item)

        elif item['media_type'] == MediaTypes.PHOTO:
            object['type'] = MediaTypes.PHOTO
            object.update(photo_item(item))

        objects.append(object)

    return objects


def fetch_count_posts(username: str) -> list[dict]:
    return private_api.username_info(username)['user']['media_count']


def fetch_posts_by_max_id(username: str, max_id: str):
    posts = private_api.username_feed(username, max_id=max_id)
    return post_items_raw_to_object(posts['items'])


def fetch_one_post(username: str, index: int) -> dict:
    posts = private_api.username_feed(username)
    media_count = private_api.username_info(username)['user']['media_count']
    items = [*posts['items']]

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

            if len(items) >= index:
                obj = items[index - 1]
                objects = post_items_raw_to_object([obj])
                return objects[0]
    else:
        return None
