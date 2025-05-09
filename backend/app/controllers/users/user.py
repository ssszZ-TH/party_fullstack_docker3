# นำเข้าโมดูลที่จำเป็นสำหรับ FastAPI, authentication, และ schema
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import logging
from app.models.users.user import create_user, get_user, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.config.settings import SECRET_KEY

# ตั้งค่า logging สำหรับบันทึกการทำงานและ debug
# อธิบาย: ใช้ logging เพื่อ track การ decode JWT และ error
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# สร้าง router สำหรับ endpoint ภายใต้ /users
# อธิบาย: ใช้ APIRouter เพื่อกำหนด prefix และ tags สำหรับ grouping endpoint
# FastAPI จัดการ trailing slashes อัตโนมัติ (เช่น /users และ /users/ ถือว่าเหมือนกัน)
router = APIRouter(prefix="/users", tags=["users"])

# กำหนด OAuth2 scheme สำหรับรับ access_token จาก header Authorization
# อธิบาย: tokenUrl="/auth/login" ชี้ไปที่ endpoint login เพื่อให้ Swagger UI รู้
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ฟังก์ชันตรวจสอบและ decode JWT เพื่อดึง user_id จาก token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # อธิบาย: รับ token จาก header Authorization (Bearer <token>)
    # Decode เพื่อดึง payload (เช่น sub ซึ่งเป็น user_id)
    try:
        # Decode token ด้วย SECRET_KEY และ algorithm HS256
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Log payload เพื่อ debug
        logger.info(f"Decoded JWT payload: {payload}")
        # ดึง user_id จาก field sub ใน payload
        user_id: str = payload.get("sub")
        # ถ้าไม่มี sub หรือ token ไม่ถูกต้อง raise error
        if user_id is None:
            logger.error("JWT payload missing 'sub' field")
            raise HTTPException(status_code=401, detail="Invalid token")
        # คืน user_id เพื่อยืนยันว่า token ถูกต้อง
        logger.info(f"Authenticated user_id: {user_id}")
        return user_id
    except JWTError as e:
        # ถ้า decode ล้มเหลว (เช่น token หมดอายุหรือ SECRET_KEY ผิด) raise error
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

# Endpoint สำหรับสร้างผู้ใช้ใหม่
@router.post("/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate):
    # อธิบาย: ไม่ต้อง auth เพราะเป็นการสมัครสมาชิก
    # รับข้อมูลจาก UserCreate schema (name, email, password) และบันทึกผู้ใช้
    result = await create_user(user.name, user.email, user.password)
    if not result:
        # ถ้าสร้างไม่สำเร็จ (เช่น email ซ้ำ) raise error 400
        logger.warning(f"Failed to create user: {user.email}")
        raise HTTPException(status_code=400, detail="Failed to create user")
    # คืนข้อมูลผู้ใช้ที่สร้างใหม่
    logger.info(f"Created user: {user.email}")
    return result

# Endpoint สำหรับดึงข้อมูลผู้ใช้ตาม user_id
@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int, current_user: str = Depends(get_current_user)):
    # อธิบาย: ต้อง auth ด้วย Depends(get_current_user) เพื่อตรวจสอบ JWT
    # ไม่ตรวจสอบว่า user_id ตรงกับ current_user เพราะต้องการให้ผู้ใช้ที่ login สามารถดูข้อมูลทุกคนได้
    # เหมาะสำหรับโปรเจกต์จบที่ไม่ต้องการจำกัดการเข้าถึง
    result = await get_user(user_id)
    if not result:
        # ถ้าไม่พบผู้ใช้ raise error 404
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    # คืนข้อมูลผู้ใช้
    logger.info(f"Retrieved user: id={user_id}")
    return result

# Endpoint สำหรับอัปเดตข้อมูลผู้ใช้
@router.put("/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: int, user: UserUpdate, current_user: str = Depends(get_current_user)):
    # อธิบาย: ต้อง auth ด้วย Depends(get_current_user) เพื่อตรวจสอบ JWT
    # อนุญาตให้อัปเดตข้อมูลผู้ใช้ทุกคน ไม่จำกัดเฉพาะข้อมูลของตัวเอง
    result = await update_user(user_id, user.name, user.email, user.password)
    if not result:
        # ถ้าไม่พบผู้ใช้ raise error 404
        logger.warning(f"User not found for update: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    # คืนข้อมูลผู้ใช้ที่อัปเดต
    logger.info(f"Updated user: id={user_id}")
    return result

# Endpoint สำหรับลบผู้ใช้
@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: str = Depends(get_current_user)):
    # อธิบาย: ต้อง auth ด้วย Depends(get_current_user) เพื่อตรวจสอบ JWT
    # อนุญาตให้ลบผู้ใช้ทุกคน ไม่จำกัดเฉพาะตัวเอง
    result = await delete_user(user_id)
    if not result:
        # ถ้าไม่พบผู้ใช้ raise error 404
        logger.warning(f"User not found for deletion: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    # คืน message ว่าลบสำเร็จ
    logger.info(f"Deleted user: id={user_id}")
    return {"message": "User deleted"}