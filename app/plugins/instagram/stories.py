from plugins.instagram.instagram_client import private_api
from plugins.instagram.utils import MediaType, username_to_pk, pk_to_username, fetch_following_pk


def stories_raw_to_object(story_dict: dict) -> dict:
    story_object = {}

    # optional params
    if 'audience' in story_dict:
        story_object['audience'] = story_dict['audience']

    if 'imported_taken_at' in story_dict:
        story_object['original_created_at'] = story_dict['imported_taken_at']

    story_object['type'] = story_dict['media_type']
    
    if story_object['type'] == MediaType.PHOTO.value: 
        story_object['content_url'] = story_dict['image_versions2']['candidates'][0]['url']
    
    elif story_object['type'] == MediaType.VIDEO.value:
        story_object['content_url'] = story_dict['video_versions'][0]['url']


    story_object['height'] = story_dict['original_height']
    story_object['width'] = story_dict['original_width']

    story_object['id'] = story_dict['pk']

    story_object['created_at'] = story_dict['taken_at']

    return story_object

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

    story_by_index = stories[index - 1]
    if (story_by_index == None):
        return None

    story_object = stories_raw_to_object(story_by_index)

    return story_object
