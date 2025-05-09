import secrets
import bcrypt

st = secrets.token_hex(16)  # สร้าง 32 ตัวอักษร
bg = bcrypt.gensalt().decode('utf-8')

print(f"secret token: {st} length: {len(st)}")
print(f"bcrypt: {bg} length: {len(bg)}")
