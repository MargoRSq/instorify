from typing import NoReturn
from fastapi import HTTPException

def raise_not_found(entity) -> NoReturn:
    raise HTTPException(status_code=404, detail=f"{entity} not found")
