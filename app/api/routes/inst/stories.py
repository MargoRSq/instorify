from typing import List

from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from models.schemas.instagram import NotFoundMessage, Story
from api.errors.instagram import not_found_error
from plugins.instagram.stories import (fetch_count_stories,
                                       fetch_one_story_by_index, fetch_stories)
from core.config import ROUTES_CACHE_EXPIRES_TIME


router = APIRouter()


@router.get('/{username}/stories', response_model=List[Story], summary='Get all user stories')
@cache(expire=ROUTES_CACHE_EXPIRES_TIME)
async def get_all_stories(username: str):
    return fetch_stories(username)


@router.get('/{username}/stories/count', response_model=int, summary='Get count of user stories')
@cache(expire=ROUTES_CACHE_EXPIRES_TIME)
async def get_count_stories(username: str):
    return fetch_count_stories(username)


@router.get('/{username}/stories/{index_story}',
            response_model=Story,
            summary='Get user story by index',
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFoundMessage}})
@cache(expire=ROUTES_CACHE_EXPIRES_TIME)
async def get_one_story(username: str, index_story: int):
    story = fetch_one_story_by_index(username, index_story)

    if story is None:
        return not_found_error('Story')

    return story
