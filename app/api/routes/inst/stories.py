from typing import List

from fastapi import APIRouter

from app.api.errors.instagram import raise_not_found
from app.models.schemas.instagram import Story
from app.plugins.instagram.stories import (fetch_count_stories,
                                           fetch_one_story_by_index,
                                           fetch_stories)


router = APIRouter()


@router.get('/{username}/stories',
            summary='Get all user stories',
            response_model=List[Story],
            response_model_exclude_none=True)
async def get_all_stories(username: str):
    return fetch_stories(username)


@router.get('/{username}/stories/count',
            summary='Get count of user stories',
            response_model=int)
async def get_count_stories(username: str):
    return fetch_count_stories(username)


@router.get('/{username}/stories/{index_story}',
            summary='Get user story by index',
            response_model=Story,
            response_model_exclude_none=True)
async def get_one_story(username: str, index_story: int):
    story = fetch_one_story_by_index(username, index_story)

    if story is None:
        raise_not_found('story')

    return story
