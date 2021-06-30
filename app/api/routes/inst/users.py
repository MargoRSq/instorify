from fastapi import APIRouter
from fastapi_cache.decorator import cache

from plugins.instagram.users import (fetch_user_info)

from models.schemas.instagram import User
from core.config import ROUTES_CACHE_EXPIRES_TIME


router = APIRouter()


@router.get('/{username}/', response_model=User, summary='Get user profile info')
@cache(expire=ROUTES_CACHE_EXPIRES_TIME)
async def get_user_info(username: str):
    return fetch_user_info(username)
