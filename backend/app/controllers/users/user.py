# นำเข้าโมดูลที่จำเป็นสำหรับ FastAPI, authentication, และ schema
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import logging
from app.models.users.user import create_user, get_user, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.config.settings import SECRET_KEY

# ตั้งค่า logging สำหรับบันทึกการทำงานและ debug
# อธิบาย: ใช้ logging เพื่อ track การ decode JWT, การทำงานของ endpoint, และ error
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# สร้าง router สำหรับ endpoint ภายใต้ /users
# อธิบาย: prefix="/users" ทำให้ endpoint เริ่มด้วย /users เช่น /users/{user_id}
router = APIRouter(prefix="/users", tags=["users"])

# กำหนด OAuth2 scheme สำหรับรับ access_token
# อธิบาย: tokenUrl="/auth/login" ชี้ไปที่ endpoint login สำหรับ Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ฟังก์ชันตรวจสอบและ decode JWT
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # อธิบาย: รับ token จาก header Authorization (Bearer <token>)
    # Decode เพื่อดึง user_id และ role ตรวจสอบว่าเป็น admin
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

# Endpoint สำหรับสร้างผู้ใช้ใหม่
# @router.post("/", response_model=UserOut)
# async def create_user_endpoint(user: UserCreate):
#     # อธิบาย: รับ UserCreate schema (name, email, password, role)
#     # ใช้ create_user จาก model ซึ่งตรวจสอบ email ซ้ำและตั้ง role='admin' โดย default
#     result = await create_user(user)
#     if not result:
#         logger.warning(f"Failed to create user: {user.email}")
#         raise HTTPException(status_code=400, detail="Email already exists")
#     logger.info(f"Created user: {user.email}, role={result.role}")
#     return result

# Endpoint สำหรับดึงข้อมูลผู้ใช้
@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    # อธิบาย: ต้อง auth และเป็น admin
    # อนุญาตให้ดูข้อมูลทุกคน เหมาะสำหรับระบบที่ให้ admin จัดการทุกอย่าง
    result = await get_user(user_id)
    if not result:
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved user: id={user_id}, role={result.role}")
    return result

# Endpoint สำหรับอัปเดตผู้ใช้
@router.put("/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: int, user: UserUpdate, current_user: dict = Depends(get_current_user)):
    # อธิบาย: ต้อง auth และเป็น admin
    # ส่ง UserUpdate รวม role ไปยัง update_user ซึ่งตั้ง role='admin' ถ้าไม่ระบุ
    result = await update_user(user_id, user)
    if not result:
        logger.warning(f"User not found for update: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Updated user: id={user_id}, role={result.role}")
    return result

# Endpoint สำหรับลบผู้ใช้
@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    # อธิบาย: ต้อง auth และเป็น admin
    # อนุญาตให้ลบทุกคน
    result = await delete_user(user_id)
    if not result:
        logger.warning(f"User not found for deletion: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted user: id={user_id}")
    return {"message": "User deleted"}