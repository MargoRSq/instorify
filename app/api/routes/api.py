from fastapi import APIRouter

from api.routes.inst import api as instagram

router = APIRouter()

router.include_router(instagram.router, prefix="/api", tags=["instagram"])
