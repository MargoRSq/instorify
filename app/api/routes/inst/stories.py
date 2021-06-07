from fastapi import APIRouter, Body, Depends, HTTPException

from plugins.instagram.instagram_client import api as instagram_api
from plugins.instagram.parser import (username_to_pk, pk_to_username, fetch_following_pk, fetch_stories)

router = APIRouter()


@router.get('/{username}')
def fetch_all_stories(username: str):
    user_pk = username_to_pk(instagram_api, username)
    return {'data': fetch_stories(instagram_api, user_pk)}


@router.get('/{username}/{index_story}')
def fetch_one_story(username: str, index_story: int):
    user_pk = username_to_pk(instagram_api, username)

    stories = fetch_stories(instagram_api, user_pk)
    stories_count = len(stories)
    if stories_count < index_story:
        return HTTPException(404)
    else:
        return {'data': stories[index_story - 1]}
