from fastapi import APIRouter

from app.models.schemas.instagram import Post
from app.plugins.instagram.posts import fetch_posts, fetch_count_posts


router = APIRouter()


@router.get('/{username}/posts', response_model=list[Post], summary='Get user posts')
async def get_posts(username: str, last_id: str = None):
    return fetch_posts(username, last_id)


@router.get('/{username}/posts/count', response_model=int, summary='Get count of user posts')
async def get_count_posts(username: str):
    return fetch_count_posts(username)
