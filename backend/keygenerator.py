import secrets
print(secrets.token_hex(16))  # สร้าง 32 ตัวอักษร

import bcrypt
print(bcrypt.gensalt().decode('utf-8'))