from fastapi import FastAPI
from fastapi.exception_handlers import (http_exception_handler,
                                        request_validation_exception_handler)
from fastapi.exceptions import RequestValidationError
from instagram_private_api.errors import ClientError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse


def subscribe_exception_handlers(application: FastAPI):
    @application.exception_handler(ClientError)
    async def user_not_found_error(exc):
        if exc.msg == 'Not Found: user_not_found':
            return JSONResponse({'detail': 'user not found'}, status_code=404)

    @application.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, exc):
        return await http_exception_handler(request, exc)

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return await request_validation_exception_handler(request, exc)
