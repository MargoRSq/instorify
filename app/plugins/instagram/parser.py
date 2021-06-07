import instagram_private_api


def username_to_pk(api: instagram_private_api.client.Client, username: str) -> int: # getting pk(id) of instagram account from username
    search_results = api.search_users(username)
    search_id = search_results['users'][0]['pk']
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


def fetch_stories(api: instagram_private_api.client.Client, user_pk:int) -> list[dict]: # fetching list of user's stories

    list_of_stories = []
    stories = api.user_story_feed(user_pk)
    if stories['reel']:
        list_stories_full = stories['reel']['items']

        for i in range(len(list_stories_full)):
            
            story_dict = list_stories_full[i]

            story_object = {}

            if 'audience' in story_dict:
                story_object['audience'] = story_dict['audience']
    
            story_object['type'] = story_dict['media_type'] 

            story_object['height'] = story_dict['original_height']
            story_object['width'] = story_dict['original_width']
                
            story_object['image_url'] = story_dict['image_versions2']['candidates'][0]['url']
            story_object['preview_url'] = story_dict['image_versions2']['candidates'][1]['url']

            story_object['id'] = story_dict['pk']
            
            story_object['created_at'] = story_dict['taken_at']
            
            if 'imported_taken_at' in story_dict:
                story_object['original_created_at'] = story_dict['imported_taken_at']

            list_of_stories.append(story_object)

    return list_of_stories
