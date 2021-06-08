from fastapi import APIRouter

from api.routes.inst import stories, posts, users

router = APIRouter()

router.include_router(stories.router, tags=["insta_stories"], prefix="/inst/stories")
