import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from instagram_private_api.errors import ClientError

from api.errors.instagram import username_error
from api.routes.api import router as api_router
from core.config import PROJECT_NAME, VERSION, DOCS_URL, REDOC_URL, REDIS_URL

origins_regex = r'http(s?)://localhost:3000'


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME,
                          version=VERSION, docs_url=DOCS_URL, redoc_url=REDOC_URL)

    application.add_middleware(
        CORSMiddleware,
        allow_origin_regex=origins_regex,
        allow_credentials=True,
        allow_methods=["*"],
        )

    application.include_router(api_router)

    application.add_exception_handler(ClientError, username_error)

    return application


app = get_application()


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(REDIS_URL, encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
