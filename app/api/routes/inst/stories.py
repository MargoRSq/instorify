from fastapi import APIRouter, Body, Depends, HTTPException
from plugins.instagram.stories import (fetch_one_story_by_index, fetch_stories,
                                       fetch_stories_count)

router = APIRouter()


@router.get('/{username}')
def fetch_all_stories(username: str):
    return {'data': fetch_stories(username)}

@router.get('/{username}/count')
def count_stories(username: str):
    return {'data': fetch_stories_count(username)}

@router.get('/{username}/{index_story}')
def fetch_one_story(username: str, index_story: int):
    story = fetch_one_story_by_index(username, index_story)

    if (story == None):
        return HTTPException(404)
    else:
        return {'data': story}
