from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.models.schemas.instagram import Post
from app.plugins.instagram.posts import fetch_posts, fetch_count_posts
from app.core.config import ROUTES_CACHE_EXPIRES_TIME


router = APIRouter()


@router.get('/{username}/posts', response_model=list[Post], summary='Get user posts')
@cache(expire=ROUTES_CACHE_EXPIRES_TIME)
async def get_posts(username: str, last_id: str = None):
    return fetch_posts(username, last_id)


@router.get('/{username}/posts/count', response_model=int, summary='Get count of user posts')
@cache(expire=ROUTES_CACHE_EXPIRES_TIME)
async def get_count_posts(username: str):
    return fetch_count_posts(username)
