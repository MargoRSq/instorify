from fastapi import APIRouter

from api.errors.instagram import not_found_error
from plugins.instagram.posts import fetch_posts_by_max_id, fetch_one_post, fetch_count_posts

router = APIRouter()


@router.get('/{username}/posts')
def get_posts(username: str, max_id: str = None):
    return fetch_posts_by_max_id(username, max_id)


@router.get('/{username}/posts/count')
def get_count_posts(username: str):
    return fetch_count_posts(username)


@router.get('/{username}/posts/{index_post}')
def get_one_post(username: str, index_post: int):
    from time import time
    start = time()
    post = fetch_one_post(username, index_post)
    end = time()
    print(end - start)
    if post is None:
        return not_found_error('Post')

    return post
