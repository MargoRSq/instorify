from fastapi import APIRouter
from plugins.instagram.users import (fetch_user_info)

from models.schemas.instagram import User

router = APIRouter()


@router.get('/{username}/', response_model=User, summary='Get user profile info')
def get_user_info(username: str):
    return fetch_user_info(username)
