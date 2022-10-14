from typing import Any
from fastapi import APIRouter

from fastapi_rss import RSSResponse

from app.models.schemas.instagram import Post
from app.plugins.instagram.posts import fetch_posts, fetch_count_posts
from app.plugins.instagram.rss import posts_to_rss

import locale
locale.setlocale(locale.LC_ALL, '')

router = APIRouter()


@router.get('/{username}/posts', response_model=Any, summary='Get user posts')
async def get_posts(username: str, last_id: str = None):
    posts = fetch_posts(username, last_id)
    rss = posts_to_rss(posts, username)
    return RSSResponse(rss)


@router.get('/{username}/posts/count', response_model=int, summary='Get count of user posts')
async def get_count_posts(username: str):
    return fetch_count_posts(username)
