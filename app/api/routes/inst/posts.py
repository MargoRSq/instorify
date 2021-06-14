from fastapi import APIRouter, Body, Depends, HTTPException

from plugins.instagram.posts import *

router = APIRouter()


@router.get('/{username}/posts')
def get_all_posts(username: str):
    pass

@router.get('/{username}/posts/{index_post}')
def get_one_post(username: str, index_story: int):
    pass
