from fastapi import APIRouter

from models.schemas.instagram import Post
from plugins.instagram.posts import fetch_posts, fetch_count_posts


router = APIRouter()


@router.get('/{username}/posts',
            summary='Get user posts',
            response_model=list[Post])
async def get_posts(username: str, offset: str = None):
    return fetch_posts(username, offset)


@router.get('/{username}/posts/count',
            summary='Get count of user posts',
            response_model=int)
async def get_count_posts(username: str):
    return fetch_count_posts(username)
