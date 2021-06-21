from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.api import router as api_router

origins_regex = r'http(s?)://localhost:3000'

def get_application() -> FastAPI:
    application = FastAPI(title='api')

    application.add_middleware(
        CORSMiddleware,
        allow_origin_regex=origins_regex,
        allow_credentials=True,
        allow_methods=["*"],
    )

    application.include_router(api_router)

    return application


app = get_application()
