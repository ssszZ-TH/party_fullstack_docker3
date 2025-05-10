from app.config.database import database
from app.config.settings import BCRYPT_SALT
from app.schemas.user import UserCreate, UserUpdate, UserOut
import bcrypt
import logging
from typing import Optional

# ตั้งค่า logging สำหรับ debug
# อธิบาย: ใช้ logging แทน print เพื่อบันทึกการทำงานและ error
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ฟังก์ชันตรวจสอบว่า email มีอยู่แล้วหรือไม่
# อธิบาย: ใช้ใน create_user เพื่อป้องกัน email ซ้ำ
async def get_user_by_email(email: str) -> Optional[dict]:
    query = "SELECT id, name, email, password, role FROM users WHERE email = :email"
    result = await database.fetch_one(query=query, values={"email": email})
    logger.info(f"Queried user with email {email}: {result}")
    return result

# ฟังก์ชันสร้างผู้ใช้ใหม่
async def create_user(user: UserCreate) -> Optional[UserOut]:
    # อธิบาย: รับ UserCreate schema และสร้างผู้ใช้ใหม่ด้วย role default เป็น 'admin'
    try:
        # ตรวจสอบว่า email ซ้ำหรือไม่
        existing_user = await get_user_by_email(user.email)
        if existing_user:
            logger.warning(f"Attempt to create user with existing email: {user.email}")
            return None
        # Hash รหัสผ่านด้วย BCRYPT_SALT
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        logger.info(f"Hashed password for {user.email}: {hashed_password}")
        # สร้าง query สำหรับ insert ผู้ใช้ใหม่
        query = """
            INSERT INTO users (name, email, password, role)
            VALUES (:name, :email, :password, :role)
            RETURNING id, name, email, role
        """
        values = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "role": user.role
        }
        result = await database.fetch_one(query=query, values=values)
        logger.info(f"Created user: {user.email}, role: {user.role}")
        return UserOut(**result._mapping) if result else None
    except ValueError as e:
        logger.error(f"Error hashing password for {user.email}: {str(e)}")
        raise

# ฟังก์ชันดึงข้อมูลผู้ใช้
async def get_user(user_id: int) -> Optional[UserOut]:
    # อธิบาย: คืนข้อมูลผู้ใช้เป็น UserOut หรือ None ถ้าไม่พบ
    query = "SELECT id, name, email, role FROM users WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    logger.info(f"Retrieved user: id={user_id}")
    return UserOut(**result._mapping) if result else None

# ฟังก์ชันอัปเดตผู้ใช้
async def update_user(user_id: int, user: UserUpdate) -> Optional[UserOut]:
    # อธิบาย: รับ UserUpdate schema และอัปเดตเฉพาะฟิลด์ที่ส่งมา
    values = {"id": user_id}
    query_parts = []
    
    if user.name is not None:
        query_parts.append("name = :name")
        values["name"] = user.name
    if user.email is not None:
        query_parts.append("email = :email")
        values["email"] = user.email
    if user.password is not None:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        query_parts.append("password = :password")
        values["password"] = hashed_password
    if user.role is not None:
        query_parts.append("role = :role")
        values["role"] = user.role
    else:
        # อธิบาย: ถ้าไม่ระบุ role ตั้งเป็น 'admin' เพื่อให้ทุกคนเป็น admin
        query_parts.append("role = :role")
        values["role"] = "admin"

    if not query_parts:
        logger.info(f"No fields to update for user id={user_id}")
        return None

    query = f"""
        UPDATE users
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, name, email, role
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated user: id={user_id}")
    return UserOut(**result._mapping) if result else None

# ฟังก์ชันลบผู้ใช้
async def delete_user(user_id: int) -> Optional[int]:
    # อธิบาย: ลบผู้ใช้และคืน id หรือ None ถ้าไม่พบ
    query = "DELETE FROM users WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    logger.info(f"Deleted user: id={user_id}")
    return result["id"] if result else None

# ฟังก์ชันตรวจสอบรหัสผ่าน
async def verify_user_password(user_id: int, password: str) -> bool:
    # อธิบาย: ตรวจสอบว่ารหัสผ่านตรงกับในฐานข้อมูลหรือไม่
    query = "SELECT password FROM users WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    if not result:
        logger.warning(f"User not found for password verification: id={user_id}")
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    logger.info(f"Verified password for user id={user_id}")
    return hashed_password == result["password"]