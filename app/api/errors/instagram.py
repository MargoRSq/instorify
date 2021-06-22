from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


def not_found_error(entity: str) -> JSONResponse:
    return JSONResponse({'detail': entity + ' Not Found'}, status_code=404)


def username_error(_: Request, exc: HTTPException) -> JSONResponse:
    return not_found_error('User')
