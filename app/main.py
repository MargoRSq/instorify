from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from instagram_private_api.errors import ClientError

from api.errors.instagram import username_error
from api.routes.api import router as api_router

origins_regex = r'http(s?)://localhost:3000'


def get_application() -> FastAPI:
    application = FastAPI(title='instorify-api',
                          version='1.0.0', docs_url="/__docs", redoc_url=None)

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
