from fastapi import FastAPI

from api.routes.api import router as api_router

def get_application() -> FastAPI:
    application = FastAPI(title='api')

    application.include_router(api_router)

    return application


app = get_application()
