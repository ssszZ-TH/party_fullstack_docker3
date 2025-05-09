# นำเข้าโมดูลที่จำเป็นสำหรับการตั้งค่าและ logging
import re
import logging

# ตั้งค่า logging สำหรับ debug และบันทึก error
# อธิบาย: ใช้ logging เพื่อบันทึกการโหลด BCRYPT_SALT และ error
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# กำหนดตัวแปร configuration สำหรับ FastAPI
# อธิบาย: ค่าต่างๆ ใช้ในการเชื่อมต่อฐานข้อมูล, API, และ JWT
DATABASE_URL = "postgresql://spa:spa@db:5432/myapp"
API_HOST = "0.0.0.0"
API_PORT = 8080
SECRET_KEY = "8c2f7a9b3d6e1f0c4a8b2d5e7f9a1c3b6d8e0f2a4b7c9d1e3f5a8b0c2d4e6f"
BCRYPT_SALT = "$2b$12$zDZMoHsxUdSvpuNJjEzsve"

# ตรวจสอบ BCRYPT_SALT
# อธิบาย: ตรวจสอบว่า BCRYPT_SALT ถูกตั้งค่าและอยู่ในรูปแบบที่ถูกต้อง
logger.info(f"Loaded BCRYPT_SALT: {BCRYPT_SALT}")
if not BCRYPT_SALT:
    # ถ้า BCRYPT_SALT ไม่ถูกตั้ง raise error
    raise ValueError("BCRYPT_SALT is not set")
if not re.match(r'^\$2b\$\d{2}\$[A-Za-z0-9./]{22}$', BCRYPT_SALT):
    # ถ้า BCRYPT_SALT ไม่ถูกต้องตาม regex raise error
    raise ValueError(f"BCRYPT_SALT is invalid: {BCRYPT_SALT}. It must be in the format $2b$<cost>$<22-char-base64>")