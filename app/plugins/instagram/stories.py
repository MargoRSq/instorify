from plugins.instagram.clients.private_api import private_api
from plugins.instagram.utils import username_to_pk

from instagram_private_api import MediaTypes


def stories_raw_to_object(story_dict: dict) -> dict:
    object = {}

    # optional params
    if 'audience' in story_dict:
        object['audience'] = story_dict['audience']

    if 'imported_taken_at' in story_dict:
        object['original_created_at'] = story_dict['imported_taken_at']

    object['type'] = story_dict['media_type']
    
    if object['type'] == MediaTypes.PHOTO: 
        object['content_url'] = story_dict['image_versions2']['candidates'][0]['url']
    
    elif object['type'] == MediaTypes.VIDEO:
        object['content_url'] = story_dict['video_versions'][0]['url']


    object['height'] = story_dict['original_height']
    object['width'] = story_dict['original_width']

    object['id'] = story_dict['pk']

    object['created_at'] = story_dict['taken_at']

    return object

def get_stories_raw(username: str) -> list[dict]:
    user_pk = username_to_pk(username)

    stories = private_api.user_story_feed(user_pk)

    if stories['reel'] == None:
        return []

    return stories['reel']['items']

def fetch_stories(username: str) -> list[dict]:

    stories = get_stories_raw(username)

    list_of_stories = []
    for i in range(len(stories)):
        story_object = stories_raw_to_object(stories[i])

        list_of_stories.append(story_object)

    return list_of_stories

def fetch_stories_count(username: str) -> int:
    return len(get_stories_raw(username))

def fetch_one_story_by_index(username: str, index: int) -> dict or None:
    stories = get_stories_raw(username)
    
    if len(stories) < index:
        return None
    else:
        story_by_index = stories[index - 1]

    story_object = stories_raw_to_object(story_by_index)

    return story_object
