from fastapi import APIRouter

from app.api.routes.inst import stories, highlights, users, posts

router = APIRouter()

router.include_router(users.router, tags=["instagram_profile"], prefix="/inst")
router.include_router(stories.router, tags=["instagram_stories"], prefix="/inst")
router.include_router(highlights.router, tags=["instagram_highlights"], prefix="/inst")
router.include_router(posts.router, tags=["instagram_posts"], prefix="/inst")
