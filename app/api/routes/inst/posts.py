from fastapi import APIRouter, Body, Depends, HTTPException

from plugins.instagram.posts import fetch_posts, fetch_one_post

router = APIRouter()


@router.get('/{username}/posts')
def get_all_posts(username: str):
    return {'data': fetch_posts(username)}

@router.get('/{username}/posts/{index_post}')
def get_one_post(username: str, index_post: int):
    post = fetch_one_post(username, index_post)

    if post == None:
        return HTTPException(404)
    else:
        return {'data': post}
