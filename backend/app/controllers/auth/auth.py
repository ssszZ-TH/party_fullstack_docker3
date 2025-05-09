# นำเข้าโมดูลที่จำเป็นสำหรับ FastAPI, JWT, การจัดการฐานข้อมูล และ logging
from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.settings import SECRET_KEY, BCRYPT_SALT
from app.config.database import database
import bcrypt
import logging
from app.schemas.user import UserCreate, UserLogin

# ตั้งค่า logging สำหรับบันทึกการทำงานและ debug error
# อธิบาย: ใช้ logging เพื่อ track การสมัคร, login, และ error
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# สร้าง router สำหรับ endpoint ภายใต้ /auth
# อธิบาย: prefix="/auth" ทำให้ endpoint เริ่มด้วย /auth เช่น /auth/register
router = APIRouter(prefix="/auth", tags=["auth"])

# กำหนด algorithm สำหรับ JWT
# อธิบาย: HS256 เป็น standard algorithm สำหรับ JWT ใช้ HMAC-SHA256
ALGORITHM = "HS256"

# ฟังก์ชันสร้างผู้ใช้ใหม่ในฐานข้อมูล
async def create_user(name: str, email: str, password: str):
    # อธิบาย: รับ name, email, password และ hash รหัสผ่านด้วย BCRYPT_SALT
    # ตรวจสอบ email ซ้ำก่อนบันทึกเพื่อป้องกัน error
    try:
        # ตรวจสอบว่า email มีอยู่ในฐานข้อมูลหรือไม่
        existing_user = await get_user_by_email(email)
        if existing_user:
            # ถ้า email ซ้ำ log warning และคืน None
            logger.warning(f"Attempt to create user with existing email: {email}")
            return None
        # Hash รหัสผ่านด้วย bcrypt และ BCRYPT_SALT
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        # บันทึก hashed password ใน log เพื่อ debug
        logger.info(f"Hashed password for {email}: {hashed_password}")
        # สร้าง query สำหรับ insert ผู้ใช้ใหม่
        query = """
            INSERT INTO users (name, email, password)
            VALUES (:name, :email, :password)
            RETURNING id, name, email
        """
        values = {"name": name, "email": email, "password": hashed_password}
        # รัน query และคืนผลลัพธ์
        return await database.fetch_one(query=query, values=values)
    except ValueError as e:
        # จับ error จาก bcrypt (เช่น BCRYPT_SALT ไม่ถูกต้อง)
        logger.error(f"Error hashing password for {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")

# ฟังก์ชันดึงข้อมูลผู้ใช้ตาม email
async def get_user_by_email(email: str):
    # อธิบาย: ค้นหาผู้ใช้ในฐานข้อมูลด้วย email
    # คืน dictionary ที่มี id, name, email, password หรือ None ถ้าไม่พบ
    query = "SELECT id, name, email, password FROM users WHERE email = :email"
    result = await database.fetch_one(query=query, values={"email": email})
    # Log ผลลัพธ์เพื่อ debug
    logger.info(f"Queried user with email {email}: {result}")
    return result

# ฟังก์ชันสร้าง JWT access token
def create_access_token(data: dict):
    # อธิบาย: สร้าง JWT จากข้อมูล (เช่น user_id ใน sub)
    # เพิ่ม expiration time และ encode ด้วย SECRET_KEY
    try:
        # คัดลอกข้อมูลเพื่อไม่แก้ไขต้นฉบับ
        to_encode = data.copy()
        # กำหนดเวลาหมดอายุของ token (30 นาที)
        expire = datetime.utcnow() + timedelta(minutes=30)
        # เพิ่ม exp ใน payload
        to_encode.update({"exp": expire})
        # Encode token ด้วย SECRET_KEY และ ALGORITHM
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        # Log การสร้าง token
        logger.info(f"Created JWT for user: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        # จับ error จากการ encode (เช่น SECRET_KEY ไม่ถูกต้อง)
        logger.error(f"Error creating JWT: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create token")

# Endpoint สำหรับสมัครสมาชิก
@router.post("/register")
async def register(user: UserCreate):
    # อธิบาย: รับข้อมูลจาก UserCreate schema (name, email, password)
    # เรียก create_user เพื่อสร้างผู้ใช้ใหม่
    result = await create_user(user.name, user.email, user.password)
    if not result:
        # ถ้า email ซ้ำ raise error 400
        logger.warning(f"Registration failed: Email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    # Log การสมัครสำเร็จ
    logger.info(f"User registered: {user.email}")
    return {"message": "User created"}

# Endpoint สำหรับ login
@router.post("/login")
async def login(user: UserLogin):
    # อธิบาย: รับข้อมูลจาก UserLogin schema (email, password)
    # ตรวจสอบ email และ password แล้วคืน access_token
    # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
    db_user = await get_user_by_email(user.email)
    if not db_user:
        # ถ้าไม่พบ email raise error 401
        logger.warning(f"Login attempt with invalid email: {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Log ข้อมูลผู้ใช้ที่พบ
    logger.info(f"Found user: id={db_user['id']}, email={db_user['email']}")
    try:
        # Hash รหัสผ่านที่ส่งมาและเปรียบเทียบกับในฐานข้อมูล
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        if hashed_password != db_user["password"]:
            # ถ้ารหัสผ่านไม่ตรง raise error 401
            logger.warning(f"Invalid password for email: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except ValueError as e:
        # จับ error จาก bcrypt (เช่น BCRYPT_SALT ไม่ถูกต้อง)
        logger.error(f"Error verifying password for {user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")
    # สร้าง access_token ด้วย user_id
    token = create_access_token({"sub": str(db_user["id"])})
    # Log การ login สำเร็จ
    logger.info(f"User logged in: {user.email}, token sub={db_user['id']}")
    return {"access_token": token, "token_type": "bearer"}