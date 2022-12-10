from fastapi import APIRouter

from app.api.routes.inst import api as instagram

router = APIRouter()

router.include_router(instagram.router, prefix="/api", tags=["instagram"])
