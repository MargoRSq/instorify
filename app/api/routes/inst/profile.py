from fastapi import APIRouter, Body, Depends, HTTPException
from plugins.instagram.profile import (fetch_user_info)

router = APIRouter()


@router.get('/{username}/')
def get_user_info(username: str):
    return {'data': fetch_user_info(username)}