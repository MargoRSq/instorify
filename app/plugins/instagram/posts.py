from instagram_private_api import MediaTypes
from plugins.instagram.clients.private_api import private_api
from models.schemas.instagram import PostObject, PostPhotoObject, PostVideoObject, PostCarouselList


def carousel_item(item: dict) -> PostCarouselList:
    items = []
    for media in item['carousel_media']:
        object = {}
        if 'video_duration' in media:
            object.update(video_item(media))
        else:
            object.update(photo_item(media))
        items.append(object)

    return items


def video_item(item: dict) -> PostVideoObject:
    object = {}
    object['content_url'] = item['video_versions'][0]['url']
    object['duration'] = item['video_duration']
    object['view_count'] = item['view_count']

    if 'location' in item:
        location_dict = item['location']
        location = {
            'name': location_dict['name'],
            'lat': location_dict['lat'],
            'lng': location_dict['lng']}
        object['location'] = location

    if 'usertags' in item:
        mentions = []
        for tag in item['usertags']['in']:
            mentions.append(tag['user']['pk'])
        if not mentions:
            mentions = None
        object['mentions'] = mentions

    return object


def photo_item(item: dict) -> PostPhotoObject:
    object = {}

    height = None
    width = None
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

    if 'usertags' in item:
        mentions = []
        for tag in item['usertags']['in']:
            mentions.append(tag['user']['pk'])
        if not mentions:
            mentions = None
        object['mentions'] = mentions

    return object


def post_items_raw_to_object(items: list) -> list[PostObject]:
    objects = []

    for item in items:
        object = {}

        if 'location' in item:
            location_dict = item['location']
            location = {
                'name': location_dict['name'],
                'lat': location_dict['lat'],
                'lng': location_dict['lng']}
            object['location'] = location

        object['created_at'] = item['taken_at']

        object['like_count'] = item['like_count']
        object['id'] = item['id']

        if item['media_type'] == MediaTypes.VIDEO:
            object['type'] = MediaTypes.VIDEO
            object['items'] = video_item(item)

        elif item['media_type'] == MediaTypes.CAROUSEL:
            object['type'] = MediaTypes.CAROUSEL
            object['items'] = carousel_item(item)

        elif item['media_type'] == MediaTypes.PHOTO:
            object['type'] = MediaTypes.PHOTO
            object['items'] = photo_item(item)

        objects.append(object)

    return objects


def fetch_count_posts(username: str) -> int:
    return private_api.username_info(username)['user']['media_count']


def fetch_posts(username: str, max_id: str) -> list[PostObject]:
    posts = private_api.username_feed(username, max_id=max_id)
    return post_items_raw_to_object(posts['items'])
