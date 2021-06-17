from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import IntEnum, Enum
from instagram_private_api import MediaTypes


class MediaTypes(IntEnum):
    PHOTO = 1       #: Photo type
    VIDEO = 2       #: Video type
    CAROUSEL = 8


class Audience(Enum):
    BESTIE = 'besties'


class StoryItem(BaseModel):
    id: int
    type: MediaTypes
    audience: Optional[Audience]
    content_url: str
    created_at: int
    duration: Optional[float]
    original_created_at: Optional[int]
    height: int
    width: int


class HighlightItemPreview(BaseModel):
    id: int
    preview_url: str
    title: str
    created_at: str
    media_count: int


class User(BaseModel):
    id: int
    username: str
    full_name: str
    profile_img: str
    profile_info: str
    is_private: bool
    is_verified: bool
    follower_count: int
    following_count: int
    media_count: int
