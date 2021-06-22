from fastapi import HTTPException, status
from starlette.requests import Request
from starlette.responses import JSONResponse


def username_error(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({'detail': 'User not found'}, status_code=404)
