import instagram_private_api

def stories_raw_to_object(stories: dict) -> dict:
    story_object = {}

    # optional params
    if 'audience' in story_dict:
        story_object['audience'] = story_dict['audience']

    if 'imported_taken_at' in story_dict:
        story_object['original_created_at'] = story_dict['imported_taken_at']

    story_object['type'] = story_dict['media_type']

    story_object['height'] = story_dict['original_height']
    story_object['width'] = story_dict['original_width']

    story_object['image_url'] = story_dict['image_versions2']['candidates'][0]['url']
    story_object['preview_url'] = story_dict['image_versions2']['candidates'][1]['url']

    story_object['id'] = story_dict['pk']

    story_object['created_at'] = story_dict['taken_at']

    return story_object


def username_to_pk(api: instagram_private_api.client.Client, username: str) -> int: # getting pk(id) of instagram account from username
    search_results = api.username_info(username)
    search_id = search_results['user']['pk']
    return search_id


def pk_to_username(api: instagram_private_api.client.Client, pk: int) -> str: # instagram id(pk) to instagram username
    search_results = api.user_info(pk)
    username = search_results['user']['username']

    return username


def fetch_following_pk(api: instagram_private_api.client.Client, pk: int) -> list[int]: # fetching "following" accounts

    uuid = api.generate_uuid()
    results = api.user_following(pk, uuid)
    followers = results['users']

    list_acconts_pk = []
    for human in followers:
        list_acconts_pk.append(human['pk'])

    return list_acconts_pk


def get_stories_raw(api: instagram_private_api.client.Client, username: str) -> list[dict]:
    user_pk = username_to_pk(api, username)

    stories = api.user_story_feed(user_pk)

    if stories['reel'] == None:
        return []

    return stories['reel']['items']


def fetch_stories(api: instagram_private_api.client.Client, username: str) -> list[dict] | None:

    stories = get_stories_raw(api, username)

    for i in range(len(stories)):
        story_object = stories_raw_to_object(stories[i])

        list_of_stories.append(story_object)

    return list_of_stories


def fetch_stories_count(api: instagram_private_api.client.Client, username: str) -> int:
    return len(get_stories_raw(api, username))


def fetch_one_story_by_index(api: instagram_private_api.client.Client, username: str, index: int) -> list[dict]:
    stories = get_stories_raw(api, username)

    story_by_index = list_stories_full[index - 1]

    if (story_by_index == None):
        return None

    story_object = stories_raw_to_object(stories[i])

    return story_object
