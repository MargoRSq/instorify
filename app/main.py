import uvicorn
import aioredis

from fastapi import FastAPI
from fastapi.exception_handlers import (http_exception_handler,
                                        request_validation_exception_handler)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from instagram_private_api.errors import ClientError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.api.routes.api import router as api_router
from app.core.config import DOCS_URL, PROJECT_NAME, REDIS_URL, REDOC_URL, VERSION

origins_regex = r'http(s?)://localhost:3000'


def application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME,
                          version=VERSION, docs_url=DOCS_URL, redoc_url=REDOC_URL)

    application.add_middleware(
        CORSMiddleware,
        allow_origin_regex=origins_regex,
        allow_credentials=True,
        allow_methods=["*"],
        )

    application.include_router(api_router)

    @application.on_event("startup")
    async def startup():
        redis = await aioredis.create_redis_pool(REDIS_URL, encoding="utf8")
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    @application.exception_handler(ClientError)
    async def custom_http_exception_handler(request, exc):
        if exc.msg == 'Not Found: user_not_found':
            return JSONResponse({'detail': 'user not found'}, status_code=404)

    @application.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, exc):
        return await http_exception_handler(request, exc)

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return await request_validation_exception_handler(request, exc)

    return application


application = application()


def start():
    uvicorn.run("app.main:application", debug=False, reload=True)
