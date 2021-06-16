from fastapi import APIRouter

from api.routes.inst import stories, highlights, profile

router = APIRouter()

router.include_router(profile.router, tags=["inst_profile"], prefix="/inst")
router.include_router(stories.router, tags=["inst_stories"], prefix="/inst")
router.include_router(highlights.router, tags=["inst_highlights"], prefix="/inst")
