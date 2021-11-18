from fastapi import APIRouter

from app.plugins.instagram.users import (fetch_user_info)
from app.models.schemas.instagram import User


router = APIRouter()

@router.get('/{username}/', response_model=User, summary='Get user profile info')
async def get_user_info(username: str):
    return fetch_user_info(username)
