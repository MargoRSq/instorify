from fastapi import APIRouter, Body, Depends, HTTPException
from plugins.instagram.stories import (fetch_one_story_by_index, fetch_stories,
                                       fetch_count_stories)

router = APIRouter()


@router.get('/{username}/stories')
def get_all_stories(username: str):
    return {'data': fetch_stories(username)}

@router.get('/{username}/stories/count')
def get_count_stories(username: str):
    return {'data': fetch_count_stories(username)}

@router.get('/{username}/stories/{index_story}')
def get_one_story(username: str, index_story: int):
    story = fetch_one_story_by_index(username, index_story)

    if (story == None):
        return HTTPException(404)
    else:
        return {'data': story}
