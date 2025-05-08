from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.settings import SECRET_KEY, BCRYPT_SALT
from passlib.context import CryptContext
from pydantic import BaseModel
from app.config.database import database
import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

async def create_user(name: str, email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    query = """
        INSERT INTO users (name, email, password)
        VALUES (:name, :email, :password)
        RETURNING id, name, email
    """
    values = {"name": name, "email": email, "password": hashed_password}
    return await database.fetch_one(query=query, values=values)

async def get_user_by_email(email: str):
    query = "SELECT id, name, email, password FROM users WHERE email = :email"
    return await database.fetch_one(query=query, values={"email": email})

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register")
async def register(user: UserCreate):
    result = await create_user(user.name, user.email, user.password)
    if not result:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"message": "User created"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    if hashed_password != db_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user["id"])})
    return {"access_token": token, "token_type": "bearer"}