from typing import List, Dict
from instagram_private_api import MediaTypes

from app.plugins.instagram.clients.private_api import private_api
from app.models.schemas.instagram import Post, PostPhotoObject, PostVideoObject, PostCarouselList


def get_mentions(item: Dict) -> List[int]:
    mentions = []
    if 'usertags' in item:
        for tag in item['usertags']['in']:
            mentions.append(tag['user']['pk'])

    return mentions


def carousel_item(item: Dict) -> PostCarouselList:
    items = []

    for media in item['carousel_media']:
        obj = {}
        if media['media_type'] == MediaTypes.VIDEO:
            obj.update(video_item(media))
        elif media['media_type'] == MediaTypes.PHOTO:
            obj.update(photo_item(media))
        items.append(obj)

    return items


def video_item(item: Dict) -> PostVideoObject:
    obj = {}
    obj['type'] = MediaTypes.VIDEO

    obj['content_url'] = item['video_versions'][0]['url']
    obj['height'] = item['video_versions'][0]['height']
    obj['width'] = item['video_versions'][0]['width']

    obj['duration'] = item['video_duration']

    if 'view_count' in item:
        obj['view_count'] = item['view_count']

    obj['mentions'] = get_mentions(item)

    return obj


def photo_item(item: Dict) -> PostPhotoObject:
    obj = {}
    obj['type'] = MediaTypes.PHOTO

    height = None
    width = None
    if 'original_height' in item:
        height = item['original_height']
        obj['height'] = height
    if 'original_width' in item:
        width = item['original_width']
        obj['width'] = width

    if height and width:
        for image in item['image_versions2']['candidates']:
            if height == image['height'] and width == image['width']:
                obj['content_url'] = image['url']
    else:
        max_height = 0
        for image in item['image_versions2']['candidates']:
            if height > max_height:
                obj['content_url'] = image['url']

    obj['mentions'] = get_mentions(item)

    return obj


def post_items_raw_to_object(items: List) -> List[Post]:
    objs = []

    for item in items:
        obj = {}

        if 'location' in item:
            location_dict = item['location']

            location = {
                'name': location_dict['name'],
                }
            if ('lat' and 'lng') in location_dict:
                location['lat'] = location_dict['lat']
                location['lng'] = location_dict['lng']

            obj['location'] = location

        obj['created_at'] = item['taken_at']

        obj['like_count'] = item['like_count']
        obj['id'] = item['id']

        if item['media_type'] == MediaTypes.VIDEO:
            obj['type'] = MediaTypes.VIDEO
            obj['items'] = [video_item(item)]

        elif item['media_type'] == MediaTypes.CAROUSEL:
            obj['type'] = MediaTypes.CAROUSEL
            obj['items'] = carousel_item(item)

        elif item['media_type'] == MediaTypes.PHOTO:
            obj['type'] = MediaTypes.PHOTO
            obj['items'] = [photo_item(item)]

        objs.append(obj)

    return objs


def fetch_count_posts(username: str) -> int:
    return private_api.username_info(username)['user']['media_count']


def fetch_posts(username: str, max_id: str) -> List[Post]:
    posts = private_api.username_feed(username, max_id=max_id)
    return post_items_raw_to_object(posts['items'])
