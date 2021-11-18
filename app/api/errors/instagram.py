from fastapi import HTTPException

def raise_not_found(entity):
    raise HTTPException(status_code=404, detail=f"{entity} not found")
