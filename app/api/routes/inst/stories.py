from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from models.schemas.instagram import NotFoundMessage, StoryItem
from plugins.instagram.stories import (fetch_count_stories,
                                       fetch_one_story_by_index, fetch_stories)

router = APIRouter()


@router.get('/{username}/stories', response_model=List[StoryItem], summary='Get all user stories')
def get_all_stories(username: str):
    return fetch_stories(username)


@router.get('/{username}/stories/count', response_model=int, summary='Get count of user stories')
def get_count_stories(username: str):
    return fetch_count_stories(username)


@router.get('/{username}/stories/{index_story}',
            response_model=StoryItem,
            summary='Get user story by index',
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFoundMessage}})
def get_one_story(username: str, index_story: int):
    story = fetch_one_story_by_index(username, index_story)

    if story is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'detail': 'Story not found'})

    return story
