from typing import Union

from instagram_private_api import MediaTypes

from app.models.schemas.instagram import Story
from app.plugins.instagram.clients.private_api import private_api
from app.plugins.instagram.utils import username_to_pk


def stories_raw_to_object(story_dict: dict) -> Story:
    object = {}

    # optional params
    if 'audience' in story_dict:
        object['audience'] = story_dict['audience']

    if 'imported_taken_at' in story_dict:
        object['original_created_at'] = story_dict['imported_taken_at']

    mentions = []
    if 'reel_mentions' in story_dict:

        for mention in story_dict['reel_mentions']:
            mentions.append(mention['user']['pk'])
    object['mentions'] = mentions

    if 'story_locations' in story_dict:
        locations = []
        for location in story_dict['story_locations']:
            location_dict = location['location']
            location = {
                'name': location_dict['name'],
                'lat': location_dict['lat'],
                'lng': location_dict['lng']}
            locations.append(location)

        object['location'] = locations

    object['type'] = story_dict['media_type']

    if object['type'] == MediaTypes.PHOTO:
        object['content_url'] = story_dict['image_versions2']['candidates'][0]['url']

    elif object['type'] == MediaTypes.VIDEO:
        object['content_url'] = story_dict['video_versions'][0]['url']
        object['duration'] = story_dict['video_duration']

    object['height'] = story_dict['original_height']
    object['width'] = story_dict['original_width']

    object['id'] = story_dict['pk']

    object['created_at'] = story_dict['taken_at']

    return object


def fetch_stories_raw(username: str) -> list[dict]:
    user_pk = username_to_pk(username)

    stories = private_api.user_story_feed(user_pk)

    if stories['reel'] is None:
        return []

    return stories['reel']['items']


def fetch_stories(username: str) -> list[Story]:
    stories = fetch_stories_raw(username)

    list_of_stories = []
    for i in range(len(stories)):
        story_object = stories_raw_to_object(stories[i])

        list_of_stories.append(story_object)

    return list_of_stories


def fetch_count_stories(username: str) -> int:
    return len(fetch_stories_raw(username))


def fetch_one_story_by_index(username: str, index: int) -> Union[Story, None]:
    stories = fetch_stories_raw(username)

    if len(stories) < index:
        return None

    story_by_index = stories[index - 1]
    story_object = stories_raw_to_object(story_by_index)

    return story_object
