import re
import logging

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# กำหนดตัวแปร configuration
DATABASE_URL = "postgresql://spa:spa@db:5432/myapp"
API_HOST = "0.0.0.0"
API_PORT = 8080
SECRET_KEY = "fd9d468016a797a38a517230f987399f"
BCRYPT_SALT = "$2b$12$gcH3dT2MwA6z.z1MESIzge"

# ตรวจสอบ BCRYPT_SALT
logger.info(f"Loaded BCRYPT_SALT: {BCRYPT_SALT}")
if not BCRYPT_SALT:
    raise ValueError("BCRYPT_SALT is not set")
if not re.match(r'^\$2b\$\d{2}\$[A-Za-z0-9./]{22}$', BCRYPT_SALT):
    raise ValueError(f"BCRYPT_SALT is invalid: {BCRYPT_SALT}. It must be in the format $2b$<cost>$<22-char-base64>")