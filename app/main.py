import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.api import router
from core.config import API_DOCS_URL, API_PROJECT_NAME,  API_REDOC_URL, API_VERSION
from api.errors.exceptions_handlers import subscribe_exception_handlers

ORIGIN_REGEX = r'http(s?)://localhost:3000'


def get_application() -> FastAPI:
    application = FastAPI(title=API_PROJECT_NAME,
                          version=API_VERSION, docs_url=API_DOCS_URL, redoc_url=API_REDOC_URL)

    application.add_middleware(
        CORSMiddleware,
        allow_origin_regex=ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        )

    application.include_router(router)

    subscribe_exception_handlers(application)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
               