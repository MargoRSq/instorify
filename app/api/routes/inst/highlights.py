from typing import List

from fastapi import APIRouter, status

from api.errors.instagram import not_found_error
from models.schemas.instagram import (HighlightItemPreview, NotFoundMessage,
                                      Story)
from plugins.instagram.highlights import (fetch_count_highlight_by_id,
                                          fetch_count_highlights,
                                          fetch_highlight_item_by_id,
                                          fetch_highlights,
                                          fetch_items_highlight_by_id,
                                          fetch_one_highlight)

router = APIRouter()


@router.get('/{username}/highlights',
            response_model=List[HighlightItemPreview],
            summary='Get all user highlights')
def get_all_highlights(username: str):
    return fetch_highlights(username)


@router.get('/{username}/highlights/count',
            response_model=int,
            summary='Get count of user highlights')
def get_count_highlights(username: str):
    return fetch_count_highlights(username)


@router.get('/{username}/highlights/{highlight_index}',
            response_model=HighlightItemPreview,
            summary='Get user highlight by index',
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFoundMessage}})
def get_highlight_by_index(username: str, highlight_index: int):
    highlight = fetch_one_highlight(username, highlight_index)

    if highlight is None:
        return not_found_error('Highlight')

    return highlight


@router.get('/{username}/highlights/items/{highlight_id}',
            response_model=List[Story],
            summary='Get user highlight by id')
def get_highlight_by_id(highlight_id: int):
    return fetch_items_highlight_by_id(highlight_id)


@router.get('/{username}/highlights/items/{highlight_id}/count',
            response_model=int,
            summary='Get count of user highlight by id')
def get_count_highlight_by_id(highlight_id: int):
    return fetch_count_highlight_by_id(highlight_id)


@router.get('/{username}/highlights/items/{highlight_id}/{index_media}',
            response_model=Story,
            summary='Get story by index from highlight',
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFoundMessage}})
def get_highlight_item_by_id(highlight_id: int, index_media: int):
    highlight = fetch_highlight_item_by_id(highlight_id, index_media)

    if highlight is None:
        return not_found_error('Story from highlight')

    return highlight
