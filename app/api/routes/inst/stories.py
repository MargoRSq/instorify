from fastapi import APIRouter, Body, Depends, HTTPException

from plugins.instagram.stories import (fetch_one_story_by_index, fetch_stories,
                                       fetch_count_stories)

from models.schemas.instagram import StoryItem
from typing import List

router = APIRouter()


@router.get('/{username}/stories', response_model=List[StoryItem], summary='Get all user stories')
def get_all_stories(username: str):
    return fetch_stories(username)

@router.get('/{username}/stories/count', response_model=int, summary='Get count of user stories')
def get_count_stories(username: str):
    return fetch_count_stories(username)

@router.get('/{username}/stories/{index_story}', response_model=StoryItem, summary='Get user story by index')
def get_one_story(username: str, index_story: int):
    story = fetch_one_story_by_index(username, index_story)

    if (story == None):
        return HTTPException(404)
    else:
        return story
