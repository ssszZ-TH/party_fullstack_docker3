from fastapi import APIRouter, HTTPException
from app.models.users.user import create_user, get_user, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate):
    result = await create_user(user.name, user.email, user.password)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create user")
    return result

@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int):
    result = await get_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.put("/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: int, user: UserUpdate):
    result = await update_user(user_id, user.name, user.email, user.password)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int):
    result = await delete_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}