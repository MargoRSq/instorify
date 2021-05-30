import io

import requests
import instagram_private_api

from .schemas import Story

def username_to_pk(api: instagram_private_api.client.Client, username: str)->int:
    """getting pk(id) of instagram account from username

    Args:
        api (instagram_private_api.client.Client): api instance
        username (str): insagram username

    Returns:
        int: personal pk(id) of instagram account
    """

    search_results = api.search_users(username)
    search_id = search_results['users'][0]['pk']
    return search_id


def fetch_following_pk(api: instagram_private_api.client.Client, pk: int)->list[int]:
    """getting pk's of following accounts

    Args:
        api (instagram_private_api.client.Client): api instance
        pk (int): pk of account, that you need to get following accounts from

    Returns:
        list[int]: list of following pks
    """
    uuid = api.generate_uuid()
    results = api.user_following(pk, uuid)
    followers = results['users']
    
    list_acconts_pk = []
    for human in followers:
        list_acconts_pk.append(human['pk'])

    return list_acconts_pk


def fetch_stories(api: instagram_private_api.client.Client, user_pk:int)->list[Story]:
    """getting stories for list of users instagram accounts

    Args:
        api (instagram_private_api.client.Client): api instance
        users (int): account pk

    Returns:
        list[Story]: list of stories dictionaries
    """

    list_of_stories = []
    stories = api.user_story_feed(user_pk)
    if stories['reel']:
        list_stories_full = stories['reel']['items']

        for i in range(len(list_stories_full)):

            if list_stories_full[i]['media_type'] == 1:
                
                image_url = list_stories_full[i]['image_versions2']['candidates'][0]['url']
                image = requests.get(image_url)
                image_bytes = io.BytesIO(image.content)
                
                image_stories_object = {'type': 'image', 'url': image_url, 'file_obj': image_bytes.read()}
                list_of_stories.append(image_stories_object)
                # with open(f'stories/{user_pk}-{i}.png', 'wb+') as f: for local save
                #     f.write(image_bytes.read())

            if list_stories_full[i]['media_type'] == 2:
                
                video_url = list_stories_full[i]['video_versions'][0]['url']
                
                # with open(f'stories/{user_pk}-{i}.mp4','wb') as f: for local save
                r = requests.get(video_url, stream=True)
                video_bytes = io.BytesIO()
                for chunk in r.iter_content(chunk_size = 1024*1024): 
                    if chunk:
                        video_bytes.write(chunk)
                            # f.write(chunk) 
                video_stories_object = {'type': 'video', 'url': video_url, 'file_obj': video_bytes.read()}
                list_of_stories.append(video_stories_object)

    return list_of_stories
