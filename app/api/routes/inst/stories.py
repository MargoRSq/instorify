from fastapi import APIRouter, Body, Depends, HTTPException

from plugins.instagram.instagram_client import api as instagram_api
from plugins.instagram.parser import (fetch_stories, stories_count)

router = APIRouter()


@router.get('/{username}')
def fetch_all_stories(username: str):
    return {'data': fetch_stories(instagram_api, username)}

@router.get('/{username}/count')
def count_stories(username: str):
    return {'data': stories_count(instagram_api, username)}

@router.get('/{username}/{index_story}')
def fetch_one_story(username: str, index_story: int):

    stories = fetch_stories(instagram_api, username)
    stories_count = len(stories)
    if stories_count < index_story:
        return HTTPException(404)
    else:
        return {'data': stories[index_story - 1]}
