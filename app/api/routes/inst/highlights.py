from fastapi import APIRouter, Body, Depends, HTTPException

from plugins.instagram.highlights import (count_highlights,
                                          fetch_items_highlight_by_id,
                                          fetch_item_highlight_by_id,
                                          fetch_highlights,
                                          fetch_one_highlight,
                                          count_highlight_by_id)

router = APIRouter()


@router.get('/{username}/highlights')
def fetch_all_highlights(username: str):
    return {'data': fetch_highlights(username)}
    
@router.get('/{username}/highlights/count')
def cnt_highlights(username: str):
    return {'data': count_highlights(username)}

@router.get('/{username}/highlights/{highlight_index}')
def highlight_by_index(username :str, highlight_index: int):
    return {'data': fetch_one_highlight(username, highlight_index)}

@router.get('/{username}/highlights/items/{highlight_id}')
def highlight_by_id(highlight_id: int):
    return {'data': fetch_items_highlight_by_id(highlight_id)}

@router.get('/{username}/highlights/items/{highlight_id}/count')
def cnt_highlight_by_id(highlight_id: int):
    return {'data': count_highlight_by_id(highlight_id)}

@router.get('/{username}/highlights/items/{highlight_id}/{index_media}')
def highlight_item_by_id(highlight_id: int, index_media: int):
    return {'data': fetch_item_highlight_by_id(highlight_id, index_media)}

