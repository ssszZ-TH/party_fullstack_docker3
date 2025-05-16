from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import logging
from app.models.users.user import create_user, get_user, update_user, delete_user, get_all_users
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.config.settings import SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        logger.info(f"Decoded JWT payload: {payload}")
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role != "admin":
            logger.error(f"Invalid token: missing 'sub' or role is not 'admin' (role={role})")
            raise HTTPException(status_code=401, detail="Admin access required")
        logger.info(f"Authenticated user: id={user_id}, role={role}")
        return {"id": user_id, "role": role}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate, current_user: dict = Depends(get_current_user)):
    result = await create_user(user)
    if not result:
        logger.warning(f"Failed to create user: {user.email}")
        raise HTTPException(status_code=400, detail="Email already exists")
    logger.info(f"Created user: {user.email}, role={result.role}")
    return result

@router.get("/me", response_model=UserOut)
async def get_current_user_endpoint(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    result = await get_user(user_id)
    if not result:
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved current user: id={user_id}, role={result.role}")
    return result

@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_user(user_id)
    if not result:
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved user: id={user_id}, role={result.role}")
    return result

@router.get("/", response_model=List[UserOut])
async def get_all_users_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_users()
    logger.info(f"Retrieved {len(results)} users")
    return results

@router.put("/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: int, user: UserUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_user(user_id, user)
    if not result:
        logger.warning(f"User not found for update: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Updated user: id={user_id}, role={result.role}")
    return result

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_user(user_id)
    if not result:
        logger.warning(f"User not found for deletion: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted user: id={user_id}")
    return {"message": "User deleted"}