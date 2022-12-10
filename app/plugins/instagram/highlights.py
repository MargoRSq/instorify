from typing import List, Dict
from instagram_private_api import MediaTypes
from instagram_web_api.errors import ClientError

from app.models.schemas.instagram import Story, HighlightItemPreview
from app.plugins.instagram.clients.private_api import private_api
from app.plugins.instagram.clients.web_api import web_api
from app.plugins.instagram.utils import username_to_pk


def highlight_items_raw_to_object(items: List) -> List[Story]:
    objects = []
    for item in items:
        obj = {}

        heigh = item['dimensions']['height']
        width = item['dimensions']['width']
        obj['height'] = heigh
        obj['width'] = width
        obj['created_at'] = item['taken_at_timestamp']
        obj['id'] = int(item['id'])

        if item['is_video']:
            obj['content_url'] = item['video_resources'][0]['src']
            obj['type'] = MediaTypes.VIDEO
            obj['duration'] = item['video_duration']

        else:
            for image in item['display_resources']:
                if heigh == image['config_height'] and width == image['config_width']:
                    obj['content_url'] = image['src']
                    obj['type'] = MediaTypes.PHOTO

        objects.append(obj)

    return objects


def highlight_raw_to_object(raw: Dict) -> HighlightItemPreview:
    return {'id': int(raw['id'].split(':')[1]),
            'title': raw['title'],
            'created_at': raw['created_at'],
            'media_count': raw['media_count'],
            'preview_url': raw['cover_media']['cropped_image_version']['url']}


def fetch_highlights(username: str) -> List[Story]:
    user_pk = username_to_pk(username)
    all_highlights = private_api.highlights_user_feed(user_pk)['tray']

    objects = []
    for raw in all_highlights:
        content_info = highlight_raw_to_object(raw)
        objects.append(content_info)

    return objects


def fetch_count_highlights(username: str) -> int:
    user_pk = username_to_pk(username)
    all_highlights = private_api.highlights_user_feed(user_pk)['tray']

    return len(all_highlights)


def fetch_one_highlight(username: str, index: int) -> Story | None:
    user_pk = username_to_pk(username)
    all_highlights = private_api.highlights_user_feed(user_pk)['tray']

    if len(all_highlights) < index or not all_highlights:
        return None

    raw = all_highlights[index - 1]
    content_info = highlight_raw_to_object(raw)

    return content_info


# highlights by id

def fetch_items_highlight_by_id(hl_id: int) -> list[Story] | None:
    try:
        highlight_reel_media = web_api.highlight_reel_media([hl_id])

        for highlight in highlight_reel_media['data']['reels_media']:
            items = highlight_items_raw_to_object(highlight['items'])

        return items[::-1]
    except ClientError:
        return None


def fetch_highlight_item_by_id(hl_id: int, index: int) -> Story | None:
    stories = fetch_items_highlight_by_id(hl_id)

    if not stories or len(stories) < index:
        return None

    return stories[index - 1]


def fetch_count_highlight_by_id(hl_id: int) -> int | None:
    try:
        highlight_reel_media = web_api.highlight_reel_media([hl_id])
        return len(highlight_reel_media['data']['reels_media'][0]['items'])
    except ClientError:
        return None
