from fastapi import APIRouter

from plugins.instagram.posts import fetch_posts, fetch_count_posts
from models.schemas.instagram import Post

router = APIRouter()


@router.get('/{username}/posts', response_model=list[Post], summary='Get user posts')
def get_posts(username: str, max_id: str = None):
    return fetch_posts(username, max_id)


@router.get('/{username}/posts/count', response_model=int, summary='Get count of user posts')
def get_count_posts(username: str):
    return fetch_count_posts(username)
