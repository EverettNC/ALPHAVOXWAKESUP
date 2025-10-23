from fastapi import APIRouter

router = APIRouter(prefix="/main", tags=["main"])

@router.get("/test")
async def test():
    return {"msg": "Test router operational!"}

