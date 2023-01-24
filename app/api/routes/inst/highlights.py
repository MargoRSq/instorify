from typing import List
from fastapi import APIRouter

from api.errors.instagram import raise_not_found
from models.schemas.instagram import HighlightItemPreview, Story
from plugins.instagram.highlights import (fetch_count_highlight_by_id,
                                              fetch_count_highlights,
                                              fetch_highlight_item_by_id,
                                              fetch_highlights,
                                              fetch_items_highlight_by_id,
                                              fetch_one_highlight)

router = APIRouter()


@router.get('/{username}/highlights',
            summary='Get all user highlights',
            response_model=List[HighlightItemPreview])
async def get_all_highlights(username: str):
    return fetch_highlights(username)


@router.get('/{username}/highlights/count',
            summary='Get count of user highlights',
            response_model=int)
async def get_count_highlights(username: str):
    return fetch_count_highlights(username)


@router.get('/{username}/highlights/{highlight_index}',
            summary='Get user highlight by index',
            response_model=HighlightItemPreview)
async def get_highlight_by_index(username: str, highlight_index: int):
    if highlight_index < 0:
        raise_not_found('index')
    highlight = fetch_one_highlight(username, highlight_index)

    if highlight is None:
        raise_not_found('highlight')

    return highlight


@router.get('/{username}/highlights/items/{highlight_id}',
            summary='Get user highlight by id',
            response_model=List[Story])
async def get_highlight_by_id(highlight_id: int):
    highlight = fetch_items_highlight_by_id(highlight_id)

    if highlight is None:
        raise_not_found('highlight')

    return highlight


@router.get('/{username}/highlights/items/{highlight_id}/count',
            summary='Get count of user highlight by id',
            response_model=int)
async def get_count_highlight_by_id(highlight_id: int):
    highlight = fetch_count_highlight_by_id(highlight_id)

    if highlight is None:
        raise_not_found('highlight')

    return fetch_count_highlight_by_id(highlight_id)


@router.get('/{username}/highlights/items/{highlight_id}/{index_media}',
            summary='Get story by index from highlight',
            response_model=Story)
async def get_highlight_item_by_id(highlight_id: int, index_media: int):
    highlight = fetch_highlight_item_by_id(highlight_id, index_media)

    if highlight is None:
        raise_not_found('highlight')

    return highlight
