from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema สำหรับสร้างผู้ใช้ใหม่
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "admin"  # อธิบาย: Default เป็น 'admin' เพราะระบบให้เฉพาะ admin ใช้งาน

# Schema สำหรับอัปเดตผู้ใช้
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None  # อธิบาย: อนุญาตให้อัปเดต role แต่ default เป็น None

# Schema สำหรับ response
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: Optional[str] = None
    role: str  # อธิบาย: รวม role ใน response เพื่อให้ frontend ทราบว่าเป็น admin

    class Config:
        # อธิบาย: อนุญาตให้แปลงจาก Row object (จาก databases) เป็น UserOut
        from_attributes = True

# Schema สำหรับ login
class UserLogin(BaseModel):
    email: EmailStr  # อธิบาย: ใช้ EmailStr เพื่อ validate รูปแบบ email
    password: str