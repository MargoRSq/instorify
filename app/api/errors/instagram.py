from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

async def username_error(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({'detail':'User not found'} , status_code=404)
