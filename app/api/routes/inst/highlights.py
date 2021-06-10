from fastapi import APIRouter, Body, Depends, HTTPException

from plugins.instagram.highlights import fetch_highlights, fetch_highlight_by_id

router = APIRouter()

@router.get('/{username}/highlights/{highlight_id}')
def fetch_all_stories(highlight_id: int):
    return {'data': fetch_highlight_by_id(highlight_id)}

@router.get('/{username}/highlights')
def fetch_all_stories(username: str):
    return {'data': fetch_highlights(username)}

