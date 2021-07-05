from fastapi import APIRouter

from app.api.routes.inst import stories, highlights, users, posts

router = APIRouter()

router.include_router(users.router, tags=["inst_profile"], prefix="/inst")
router.include_router(stories.router, tags=["inst_stories"], prefix="/inst")
router.include_router(highlights.router, tags=[
                      "inst_highlights"], prefix="/inst")
router.include_router(posts.router, tags=[
                      "inst_posts"], prefix="/inst")
