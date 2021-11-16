from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend

from app.api.routes.api import router as api_router
from app.core.config import API_DOCS_URL, API_PROJECT_NAME, REDIS_URL, API_REDOC_URL, API_VERSION, API_DEBUG, API_RELOAD
from app.api.errors.exceptions_handlers import subscribe_exception_handlers

origins_regex = r'http(s?)://localhost:3000'


def get_application() -> FastAPI:
    application = FastAPI(title=API_PROJECT_NAME,
                          version=API_VERSION, docs_url=API_DOCS_URL, redoc_url=API_REDOC_URL)

    application.add_middleware(
        CORSMiddleware,
        allow_origin_regex=origins_regex,
        allow_credentials=True,
        allow_methods=["*"],
        )

    application.include_router(api_router)

    # @application.on_event("startup")
    # async def startup():
    #     redis = await aioredis.create_redis_pool(REDIS_URL, encoding="utf8")
    #     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    subscribe_exception_handlers(application)

    return application


app = get_application()
