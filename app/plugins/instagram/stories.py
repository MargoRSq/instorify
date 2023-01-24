from typing import List, Dict

from instagram_private_api import MediaTypes
from api.errors.instagram import raise_not_found

from models.schemas.instagram import Story
from plugins.instagram.clients.private_api import private_api
from plugins.instagram.utils import username_to_pk


def stories_raw_to_object(story_dict: Dict) -> Story:
    obj = {}

    # optional params
    if 'audience' in story_dict:
        if obj['audience']:
            obj['audience'] = story_dict['audience']

    if 'imported_taken_at' in story_dict:
        obj['original_created_at'] = story_dict['imported_taken_at']

    mentions = []
    if 'reel_mentions' in story_dict:
        for mention in story_dict['reel_mentions']:
            mentions.append(mention['user']['pk'])
        obj['mentions'] = mentions

    if 'story_locations' in story_dict:
        locations = []
        for location in story_dict['story_locations']:
            location_dict = location['location']
            location = {'name': location_dict['name']}
            if 'lat' in location_dict and 'lng' in location_dict:
                location.update({'lat': location_dict['lat'],
                                 'lng': location_dict['lng']})
            locations.append(location)
        if locations:
            obj['location'] = locations

    obj['type'] = story_dict['media_type']

    if obj['type'] == MediaTypes.PHOTO:
        obj['content_url'] = story_dict['image_versions2']['candidates'][0]['url']

    elif obj['type'] == MediaTypes.VIDEO:
        obj['content_url'] = story_dict['video_versions'][0]['url']
        obj['duration'] = story_dict['video_duration']

    obj['height'] = story_dict['original_height']
    obj['width'] = story_dict['original_width']

    obj['id'] = story_dict['pk']

    obj['created_at'] = story_dict['taken_at']

    return obj


def fetch_stories_raw(username: str) -> List[dict]:
    user_pk = username_to_pk(username)

    stories = private_api.user_story_feed(user_pk)

    if stories['reel'] is None:
        return []

    return stories['reel']['items']


def fetch_stories(username: str) -> List[Story]:
    stories = fetch_stories_raw(username)

    list_of_stories = []
    for _, item in enumerate(stories):
        story_object = stories_raw_to_object(item)

        list_of_stories.append(story_object)

    return list_of_stories


def fetch_count_stories(username: str) -> int:
    return len(fetch_stories_raw(username))


def fetch_one_story_by_index(username: str, index: int) -> Story | None:
    if index < 0:
        raise_not_found('index')
    stories = fetch_stories_raw(username)

    if len(stories) < index:
        return None

    story_by_index = stories[index - 1]
    story_object = stories_raw_to_object(story_by_index)

    return story_object
