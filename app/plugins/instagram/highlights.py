from plugins.instagram.instagram_client import private_api, web_api
from plugins.instagram.utils import MediaType, username_to_pk


def highlight_raw_to_object(items: dict) -> dict:
    
    highlight_items = []
    for item in items:
        highlight_item = {}
        highlight_item['height'] = item['dimensions']['height']
        highlight_item['width'] = item['dimensions']['width']
        highlight_item['taken_at'] = item['taken_at_timestamp']
        highlight_item['id'] = int(item['id'])

        if item['is_video']:
            highlight_item['content_url'] = item['video_resources'][0]['src']
            highlight_item['type'] = MediaType.VIDEO.value
            highlight_item['duration'] = item['video_duration']
        
        else:
            for image in item['display_resources']:
                if highlight_item['height'] == image['config_height'] and highlight_item['width'] == image['config_width']:
                    highlight_item['content_url'] = image['src']
                    highlight_item['type'] = MediaType.PHOTO.value

        highlight_items.append(highlight_item)

    return highlight_items

def fetch_highlights(username: str) -> list:
    
    user_pk = username_to_pk(username)
    all_highlights = private_api.highlights_user_feed(user_pk)

    highlight_objects = []
    highlight_id_arr = []
    for highlight_raw in all_highlights['tray']:
        highlight_id = highlight_raw['id'].split(':')[1]
        highlight_id_arr.append(highlight_id)
        
        content_info = {'id': int(highlight_id),
                        'title': highlight_raw['title'], 
                        'created_at': highlight_raw['created_at'],
                        'media_count': highlight_raw['media_count']}
        highlight_objects.append(content_info)

    highlight_reel_media = web_api.highlight_reel_media(highlight_id_arr)
    for i, highlight in enumerate(highlight_reel_media['data']['reels_media']):
        items = {'items': highlight_raw_to_object(highlight['items'])}
        
        highlight_objects[i].update(items)

    return highlight_objects
