from fastapi import APIRouter

from app.plugins.instagram.users import fetch_user_info
from app.models.schemas.instagram import User


router = APIRouter()


@router.get('/{username}',
            summary='Get user profile info',
            response_model=User,
            response_model_exclude_none=True)
async def get_user_info(username: str):
    return fetch_user_info(username)
