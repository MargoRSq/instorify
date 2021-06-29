from enum import Enum, IntEnum
from typing import List, Optional, TypedDict, Union

from instagram_private_api import MediaTypes
from pydantic import BaseModel


class NotFoundMessage(BaseModel):
    detail: str


class InstMediaTypes(IntEnum):
    PHOTO = MediaTypes.PHOTO
    VIDEO = MediaTypes.VIDEO
    CAROUSEL = MediaTypes.CAROUSEL


class Audience(Enum):
    BESTIE = 'besties'


class Location(BaseModel):
    name: str
    lat: float
    lng: float


# Plugin functions schemas


HighlightItemsObject = TypedDict('HighlightObjectPlugin', {
    'id': int,
    'type': InstMediaTypes,
    'height': str,
    'width': int,
    'created_at': int,
    'duration': Optional[float],
    'content_url': str
    })

HighlightObject = TypedDict('HighlightObject', {
    'id': int,
    'title': str,
    'created_at': int,
    'media_count': int,
    'preview_url': str
    })

UserInfoObject = TypedDict('UserInfoObject', {
    'id': int,
    'username': str,
    'full_name': str,
    'profile_img': str,
    'profile_info': str,
    'is_private': bool,
    'is_verified': bool,
    'follower_count': int,
    'following_count': int,
    'media_count': int
    })

StoryObject = TypedDict('StoryObject', {
    'id': int,
    'audience': Optional[Audience],
    'original_created_at': Optional[int],
    'type': InstMediaTypes,
    'height': int,
    'width': int,
    'created_at': int,
    'duration': Optional[float],
    'content_url': str,
    'location': Optional[List[Location]],
    'mentions': Optional[List[int]]
    })


# Response models

class StoryItem(BaseModel):
    id: int
    type: InstMediaTypes
    audience: Optional[Audience]
    content_url: str
    created_at: int
    duration: Optional[float]
    original_created_at: Optional[int]
    height: int
    width: int
    location: Optional[List[Location]]
    mentions: Optional[List[int]]


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


class PostPhotoObject(BaseModel):
    height: Optional[int]
    width: Optional[int]
    content_url: str
    mentions: Optional[List[int]]


class PostVideoObject(BaseModel):
    duration: Optional[float]
    content_url: Optional[str]
    mentions: Optional[List[int]]


PostCarouselList = list[Union[PostPhotoObject, PostVideoObject]]


class PostObject(BaseModel):
    id: str
    type: InstMediaTypes
    created_at: int
    location: Optional[List[Location]]
    view_count: Optional[int]
    like_count: int
    items: Union[PostCarouselList, PostVideoObject, PostPhotoObject]


class Post(BaseModel):
    id: str
    type: InstMediaTypes
    created_at: int
    location: Optional[Location]
    like_count: int
    items: Union[PostCarouselList, PostVideoObject, PostPhotoObject]
