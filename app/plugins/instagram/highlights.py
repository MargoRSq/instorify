from instagram_private_api import MediaTypes
from plugins.instagram.instagram_client import private_api, web_api
from plugins.instagram.utils import username_to_pk


def highlight_raw_to_object(items: dict) -> dict:
    
    hl_items = []
    for item in items:
        heigh = item['dimensions']['height']
        width = item['dimensions']['width']
        hl_item = {}
        hl_item['height'] = heigh
        hl_item['width'] = width
        hl_item['taken_at'] = item['taken_at_timestamp']
        hl_item['id'] = int(item['id'])

        if item['is_video']:
            hl_item['content_url'] = item['video_resources'][0]['src']
            hl_item['type'] = MediaTypes.VIDEO.value
            hl_item['duration'] = item['video_duration']
        
        else:
            for image in item['display_resources']:
                if heigh == image['config_height'] and width == image['config_width']:
                    hl_item['content_url'] = image['src']
                    hl_item['type'] = MediaTypes.PHOTO.value

        hl_items.append(hl_item)

    return hl_items

def fetch_highlights(username: str) -> list:
    
    user_pk = username_to_pk(username)
    all_highlights = private_api.highlights_user_feed(user_pk)

    hl_objects = []
    hl_id_arr = []
    for hl_raw in all_highlights['tray']:
        hl_id = hl_raw['id'].split(':')[1]
        hl_id_arr.append(hl_id)
        
        content_info = {'id': int(hl_id),
                        'title': hl_raw['title'], 
                        'created_at': hl_raw['created_at'],
                        'media_count': hl_raw['media_count']}
        hl_objects.append(content_info)

    hl_reel_media = web_api.highlight_reel_media(hl_id_arr)
    for i, hl in enumerate(hl_reel_media['data']['reels_media']):
        items = {'items': highlight_raw_to_object(hl['items'])}
        
        hl_objects[i].update(items)

    return hl_objects
