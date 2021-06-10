from instagram_private_api import MediaTypes
from plugins.instagram.instagram_client import private_api, web_api
from plugins.instagram.utils import username_to_pk


def highlight_raw_to_object(items: dict) -> dict:
    
    items = []
    for item in items:
        heigh = item['dimensions']['height']
        width = item['dimensions']['width']
        item = {}
        item['height'] = heigh
        item['width'] = width
        item['taken_at'] = item['taken_at_timestamp']
        item['id'] = int(item['id'])

        if item['is_video']:
            item['content_url'] = item['video_resources'][0]['src']
            item['type'] = MediaTypes.VIDEO.value
            item['duration'] = item['video_duration']
        
        else:
            for image in item['display_resources']:
                if heigh == image['config_height'] and width == image['config_width']:
                    item['content_url'] = image['src']
                    item['type'] = MediaTypes.PHOTO.value

        items.append(item)

    return items

def fetch_highlights(username: str) -> list:
    
    user_pk = username_to_pk(username)
    all_highlights = private_api.highlights_user_feed(user_pk)

    objects = []
    ids = []
    for raw in all_highlights['tray']:
        id = raw['id'].split(':')[1]
        ids.append(id)
        
        content_info = {'id': int(id),
                        'title': raw['title'], 
                        'created_at': raw['created_at'],
                        'media_count': raw['media_count']}
        objects.append(content_info)

    reel_media = web_api.highlight_reel_media(ids)
    for i, highlight in enumerate(reel_media['data']['reels_media']):
        items = {'items': highlight_raw_to_object(highlight['items'])}
        
        objects[i].update(items)

    return objects


def fetch_highlight_by_id(id: int) -> list:

    highlight_reel_media = web_api.highlight_reel_media([id])
    username = highlight_reel_media['data']['reels_media'][0]['owner']['username']

    
    user_pk = username_to_pk(username)
    all_highlights = private_api.highlights_user_feed(user_pk)

    highlight_objects = []
    highlight_id_arr = []
    for highlight_raw in all_highlights['tray']:
        highlight_id = highlight_raw['id'].split(':')[1]
        highlight_id_arr.append(highlight_id)
        
        if id == int(highlight_id):
            content_info = {'id': int(highlight_id),
                            'title': highlight_raw['title'], 
                            'created_at': highlight_raw['created_at'],
                            'media_count': highlight_raw['media_count']}
            highlight_objects.append(content_info)

    
    for i, highlight in enumerate(highlight_reel_media['data']['reels_media']):
        items = {'items': highlight_raw_to_object(highlight['items'])}
        
        highlight_objects[i].update(items)

    return highlight_objects
