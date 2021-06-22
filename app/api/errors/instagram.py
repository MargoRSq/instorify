from fastapi import HTTPException, status
from starlette.requests import Request
from starlette.responses import JSONResponse


def username_error(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({'detail': 'User not found'}, status_code=404)


def story_not_found_exception() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={'detail': 'Story not found'})
