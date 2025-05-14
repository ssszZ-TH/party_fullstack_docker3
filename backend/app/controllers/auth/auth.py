# นำเข้าโมดูลที่จำเป็นสำหรับ FastAPI, JWT, การจัดการฐานข้อมูล และ logging
from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.settings import SECRET_KEY, BCRYPT_SALT
from app.config.database import database
import bcrypt
import logging
from app.schemas.user import UserCreate, UserLogin
from app.models.users.user import create_user, get_user_by_email  # อธิบาย: นำเข้าฟังก์ชันจาก model

# ตั้งค่า logging สำหรับบันทึกการทำงานและ debug
# อธิบาย: ใช้ logging เพื่อ track การสมัคร, login, และ error
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# สร้าง router สำหรับ endpoint ภายใต้ /auth
# อธิบาย: prefix="/auth" ทำให้ endpoint เริ่มด้วย /auth เช่น /auth/register
router = APIRouter(prefix="/auth", tags=["auth"])

# กำหนด algorithm สำหรับ JWT
# อธิบาย: HS256 เป็น standard algorithm สำหรับ JWT ใช้ HMAC-SHA256
ALGORITHM = "HS256"

# ฟังก์ชันสร้าง JWT access token
def create_access_token(data: dict):
    # อธิบาย: สร้าง JWT จากข้อมูล (user_id ใน sub และ role)
    # เพิ่ม expiration time และ encode ด้วย SECRET_KEY
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)  # กำหนดเวลา expiration เป็น 1 วัน
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Created JWT for user: id={data.get('sub')}, role={data.get('role')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create token")

# Endpoint สำหรับสมัครสมาชิก
@router.post("/register")
async def register(user: UserCreate):
    # อธิบาย: รับ UserCreate schema (name, email, password, role)
    # ใช้ create_user จาก model ซึ่งตรวจสอบ email ซ้ำและตั้ง role='admin' โดย default
    try:
        result = await create_user(user)
        if not result:
            logger.warning(f"Registration failed: Email {user.email} already exists")
            raise HTTPException(status_code=400, detail="Email already exists")
        logger.info(f"User registered: {user.email}, role={result.role}")
        return {"message": "User created"}
    except ValueError as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")

# Endpoint สำหรับ login
@router.post("/login")
async def login(user: UserLogin):
    # อธิบาย: รับ UserLogin schema (email, password)
    # ใช้ get_user_by_email จาก model เพื่อตรวจสอบผู้ใช้
    db_user = await get_user_by_email(user.email)
    if not db_user:
        logger.warning(f"Login attempt with invalid email: {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info(f"Found user: id={db_user['id']}, email={db_user['email']}, role={db_user['role']}")
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        if hashed_password != db_user["password"]:
            logger.warning(f"Invalid password for email: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except ValueError as e:
        logger.error(f"Error verifying password for {user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")
    token = create_access_token({"sub": str(db_user["id"]), "role": db_user["role"]})
    logger.info(f"User logged in: {user.email}, token sub={db_user['id']}, role={db_user['role']}")
    return {"access_token": token, "token_type": "bearer"}