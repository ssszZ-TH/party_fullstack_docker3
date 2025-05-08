เข้าใจแล้ว! คุณต้องการคงการใช้ `python-dotenv` สำหรับจัดการ `.env` file (ไม่ใช้ `pydantic-settings`) และยืนยันว่า database จะใช้ **PostgreSQL** พร้อมเพิ่มระบบ authentication (auth) ใน `requirements.txt` สำหรับโปรเจกต์ FastAPI ที่มีโครงสร้าง MVC (ไม่มี View) และกำลัง scale up เพื่อรองรับ 10+ services โดยใช้ native SQL queries และ Dockerized environment

ด้านล่างนี้เป็นการอัปเดต `requirements.txt` โดย:
- คง `python-dotenv` แทน `pydantic-settings`
- เพิ่ม libraries สำหรับระบบ auth ที่เหมาะสมและเข้ากันได้
- ใช้เวอร์ชันล่าสุดที่ stable (ณ วันที่ 8 พฤษภาคม 2025)
- รองรับ PostgreSQL และ native queries
- เข้ากันได้กับ FastAPI และ dependencies อื่นๆ

### ข้อควรพิจารณา
- **ระบบ Auth**:
  - ใช้ **JWT** สำหรับ stateless authentication
  - ใช้ **password hashing** สำหรับรหัสผ่าน
  - รองรับ **CORS** สำหรับ frontend React
  - อาจเพิ่ม **session management** หรือ **rate limiting** สำหรับ scale up
- **PostgreSQL**:
  - ใช้ `psycopg2-binary` และ `databases[postgresql]` สำหรับ native queries
  - รองรับ connection pool
- **.env**:
  - ใช้ `python-dotenv` สำหรับโหลด environment variables
- **Scale Up**:
  - รองรับ high traffic ด้วย JWT และ connection pool
  - อาจเพิ่ม Redis สำหรับ session หรือ rate limiting

### อัปเดต `requirements.txt`
จาก `requirements.txt` เดิม:


fastapi==0.115.2
uvicorn==0.32.0
psycopg2-binary==2.9.10
python-dotenv==1.0.1
databases[postgresql]==0.9.0
pydantic==2.9.2


#### Libraries ที่ควรเพิ่มสำหรับ Auth
1. **python-jose[cryptography]**:
   - ใช้สำหรับสร้างและ verify JWT tokens
   - เหตุผล: FastAPI รองรับ OAuth2 และ JWT ผ่าน library นี้
   - เข้ากันได้กับ: FastAPI, Pydantic
   - เวอร์ชันล่าสุด: `3.3.0`
2. **passlib[bcrypt]**:
   - ใช้สำหรับ hash รหัสผ่านอย่างปลอดภัย
   - เหตุผล: เก็บรหัสผ่านใน PostgreSQL ด้วย `bcrypt`
   - เข้ากันได้กับ: FastAPI, `psycopg2`
   - เวอร์ชันล่าสุด: `1.7.4`
3. **python-multipart**:
   - ใช้สำหรับ endpoints ที่รับ `multipart/form-data` เช่น file upload ใน auth (เช่น profile pictures)
   - เหตุผล: รองรับ form data ใน login หรือ register
   - เข้ากันได้กับ: FastAPI
   - เวอร์ชันล่าสุด: `0.0.12`
4. **aioredis** (optional):
   - ใช้สำหรับ session management หรือ rate limiting เพื่อ scale up
   - เหตุผล: เก็บ session หรือจำกัด rate ใน Redis
   - เข้ากันได้กับ: FastAPI, async operations
   - เวอร์ชันล่าสุด: `2.0.1`

#### `requirements.txt` ที่อัปเดต

fastapi==0.115.2
uvicorn==0.32.0
psycopg2-binary==2.9.10
python-dotenv==1.0.1
databases[postgresql]==0.9.0
pydantic==2.9.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
aioredis==2.0.1


**หมายเหตุ**:
- คง `python-dotenv==1.0.1` ตามที่ต้องการ
- `aioredis` เป็น optional ถ้ายังไม่ต้องการ Redis สามารถลบได้
- ทุก library เข้ากันได้กับ `fastapi==0.115.2`, `pydantic==2.9.2`, และ `psycopg2-binary==2.9.10`
- ไม่รวม `fastapi-users` เพราะคุณอาจต้องการเขียน auth logic เองเพื่อควบคุม native queries และโครงสร้าง MVC

### การใช้งาน Libraries ในโปรเจกต์
เพื่อให้เข้าใจว่า libraries เหล่านี้ใช้อย่างไรในโครงสร้าง MVC ของคุณ:

#### 1. `python-dotenv`
- ใช้ใน `app/config/settings.py` เพื่อโหลด `.env`
- ตัวอย่าง:
  ```python
  from dotenv import load_dotenv
  import os

  load_dotenv()

  DATABASE_URL = os.getenv("DATABASE_URL")
  API_HOST = os.getenv("API_HOST")
  API_PORT = int(os.getenv("API_PORT"))
  SECRET_KEY = os.getenv("SECRET_KEY")
  ```

#### 2. `python-jose[cryptography]`
- ใช้ใน `/app/controllers/auth/auth.py` สำหรับจัดการ JWT
- ตัวอย่าง:
  ```python
  from fastapi import APIRouter, HTTPException
  from jose import jwt, JWTError
  from datetime import datetime, timedelta
  from app.config.settings import SECRET_KEY
  from passlib.context import CryptContext
  from pydantic import BaseModel
  from app.config.database import database

  router = APIRouter(prefix="/auth", tags=["auth"])

  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  ALGORITHM = "HS256"

  class UserLogin(BaseModel):
      email: str
      password: str

  class UserCreate(BaseModel):
      name: str
      email: str
      password: str

  async def create_user(name: str, email: str, password: str):
      hashed_password = pwd_context.hash(password)
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
      if not db_user or not pwd_context.verify(user.password, db_user["password"]):
          raise HTTPException(status_code=401, detail="Invalid credentials")
      token = create_access_token({"sub": str(db_user["id"])})
      return {"access_token": token, "token_type": "bearer"}
  ```

#### 3. `passlib[bcrypt]`
- ใช้ใน `auth.py` (ด้านบน) สำหรับ hash รหัสผ่าน
- ตัวอย่างการ hash และ verify:
  ```python
  hashed_password = pwd_context.hash(password)
  is_valid = pwd_context.verify(plain_password, hashed_password)
  ```

#### 4. `python-multipart`
- ใช้ถ้ามี endpoints ที่รับ file upload เช่น profile pictures
- ตัวอย่าง:
  ```python
  from fastapi import UploadFile

  @router.post("/upload-profile")
  async def upload_profile(file: UploadFile):
      content = await file.read()
      # บันทึกไฟล์หรือประมวลผล
      return {"filename": file.filename}
  ```

#### 5. `aioredis` (ถ้าใช้)
- ใช้สำหรับ session หรือ rate limiting
- ต้องเพิ่ม Redis service ใน `docker-compose.yml`:
  ```yaml
  version: '3.8'

  services:
    backend:
      build: ./backend
      command: sh -c "uvicorn app.main:app --host 0.0.0.0 --reload --port 8080"
      ports:
        - "8080:8080"
      volumes:
        - ./backend:/app
        - ./backend/.env:/app/.env
      networks:
        - partymodelnet3

    db:
      image: postgres:16
      volumes:
        - ./db-data:/var/lib/postgresql/data
        - ./staticData:/staticData
      environment:
        POSTGRES_DB: myapp
        POSTGRES_USER: spa
        POSTGRES_PASSWORD: spa
      networks:
        - partymodelnet3
      ports:
        - "5432:5432"

    redis:
      image: redis:7
      networks:
        - partymodelnet3

    frontend:
      build: ./frontend
      command: npm run dev -- --host 0.0.0.0 --port 5173
      ports:
        - "5173:5173"
      volumes:
        - ./frontend:/app
        - /app/node_modules
      environment:
        - CHOKIDAR_USEPOLLING=true
      depends_on:
        - backend
      networks:
        - partymodelnet3

  networks:
    partymodelnet3:
      driver: bridge
  ```
- ตัวอย่างการใช้ `aioredis`:
  ```python
  import aioredis

  redis = aioredis.from_url("redis://redis:6379", decode_responses=True)

  async def store_session(user_id: int, token: str):
      await redis.set(f"session:{user_id}", token, ex=1800)
  ```

### อัปเดต `.env`
เพิ่ม `SECRET_KEY` สำหรับ JWT:


DATABASE_URL=postgresql://spa:spa@db:5432/myapp
API_HOST=0.0.0.0
API_PORT=8080
SECRET_KEY=your-secure-secret-key-here


### การ Scale Up
เพื่อรองรับการ scale up:
1. **JWT**:
   - ใช้ `python-jose` สำหรับ stateless auth เพื่อลด load บน database
   - เก็บ token ใน client-side (React) และ verify ใน backend
2. **Redis** (ถ้าใช้ `aioredis`):
   - เก็บ session หรือ rate limit เพื่อลดการ query PostgreSQL
   - Scale Redis ด้วย replication ใน production
3. **PostgreSQL**:
   - ใช้ connection pool ใน `databases`:
     ```python
     database = Database(settings.DATABASE_URL, min_size=5, max_size=20)
     ```
   - เพิ่ม indexes สำหรับตาราง `users`:
     ```sql
     CREATE INDEX idx_users_email ON users (email);
     ```
4. **Rate Limiting** (ถ้าต้องการ):
   - เพิ่ม `slowapi`:
     ```bash
     pip install slowapi
     ```
     อัปเดต `requirements.txt`:
     ```
     slowapi==0.1.9
     ```
     ตัวอย่าง:
     ```python
     from slowapi import Limiter
     from slowapi.util import get_remote_address

     limiter = Limiter(key_func=get_remote_address)
     app.state.limiter = limiter
     ```

### การตรวจสอบความเข้ากันได้
- **FastAPI 0.115.2**: เข้ากันได้กับ `python-jose`, `passlib`, `python-multipart`, และ `aioredis`
- **Pydantic 2.9.2**: เข้ากันได้กับทุก library
- **psycopg2-binary 2.9.10**: เข้ากันได้กับ `databases[postgresql]` และ PostgreSQL 16
- **python-dotenv 1.0.1**: ทำงานได้ดีกับการโหลด `.env`
- ทดสอบด้วย:
  ```bash
  pip install -r requirements.txt
  docker-compose up --build
  ```

### การรวม Auth เข้ากับ MVC
- **Model** (`/app/models/users/user.py`):
  - เพิ่มฟังก์ชันสำหรับ auth เช่น `get_user_by_email`
  - ตัวอย่าง:
    ```python
    async def get_user_by_email(email: str):
        query = "SELECT id, name, email, password FROM users WHERE email = :email"
        return await database.fetch_one(query=query, values={"email": email})
    ```
- **Controller** (`/app/controllers/auth/auth.py`):
  - รวม endpoints สำหรับ `/auth/register` และ `/auth/login` (ดูตัวอย่างด้านบน)
- **Schema** (`/app/schemas/user.py`):
  - คง schema เดิมจาก artifact ก่อนหน้า
- **Main** (`/app/main.py`):
  - รวม `auth_router` และตั้งค่า CORS:
    ```python
    app.include_router(auth_router)
    ```

### วิธีทดสอบ
1. **อัปเดตไฟล์**:
   - ใช้ `requirements.txt`, `.env`, และ `auth.py` จากด้านบน
   - ตรวจสอบ `docker-compose.yml` มี Redis ถ้าใช้ `aioredis`
2. **สร้างตาราง users**:
   - อัปเดต `/projfolder/db/init.sql`:
     ```sql
     CREATE TABLE users (
         id SERIAL PRIMARY KEY,
         name VARCHAR(255) NOT NULL,
         email VARCHAR(255) UNIQUE NOT NULL,
         password VARCHAR(255) NOT NULL
     );
     CREATE INDEX idx_users_email ON users (email);
     ```
3. **รัน**:
   ```bash
   cd /projfolder
   docker-compose up --build
   ```
4. **ทดสอบ API**:
   - ใช้ Swagger UI (`http://localhost:8080/docs`):
     - `POST /auth/register`: สร้างผู้ใช้
     - `POST /auth/login`: ได้รับ JWT token
   - ตัวอย่าง request:
     ```json
     {
         "name": "John Doe",
         "email": "john@example.com",
         "password": "securepassword"
     }
     ```

### สรุป
- **Libraries ที่เพิ่ม**:
  - `python-jose[cryptography]==3.3.0`: สำหรับ JWT
  - `passlib[bcrypt]==1.7.4`: สำหรับ password hashing
  - `python-multipart==0.0.12`: สำหรับ form data
  - `aioredis==2.0.1`: สำหรับ session/rate limiting (optional)
- **คงไว้**:
  - `python-dotenv==1.0.1` สำหรับ `.env`
  - PostgreSQL ด้วย `psycopg2-binary` และ `databases[postgresql]`
- **เข้ากันได้**: ทุก library ทำงานได้ดีกับ FastAPI 0.115.2 และ Pydantic 2.9.2
- **Scale Up**:
  - ใช้ JWT สำหรับ stateless auth
  - เพิ่ม Redis ถ้าต้องการ session/rate limiting
  - Optimize PostgreSQL ด้วย indexes และ connection pool

ถ้าต้องการตัวอย่างเพิ่ม เช่น การ verify JWT ใน endpoints อื่น, การเชื่อมต่อจาก React, หรือการตั้งค่า Redis ให้สมบูรณ์ บอกมาได้เลย!