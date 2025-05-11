# Full-Stack Development Based on Reference Data Model

โปรเจกต์จบสำหรับการพัฒนาระบบ Full-Stack โดยใช้ **FastAPI (Python)**, **React + TypeScript**, และ **PostgreSQL** รองรับการจัดการข้อมูลผู้ใช้ด้วย role-based authentication (เฉพาะ admin) และ deploy ด้วย **Docker Compose** โปรเจกต์นี้เน้น data integrity, performance optimization และ scalability สำหรับ dataset ขนาดใหญ่ (>100,000 records).

**ผู้พัฒนา**: Sithipong Chamratritthirong (รหัสนักศึกษา 64...19) สถาบันเทคโนโลยีจิตรลดา Chitralada Institute of Technology

## คุณสมบัติหลัก

- **การจัดการผู้ใช้**:
  - CRUD operations (`POST /users`, `GET /users/{id}`, `PUT /users/{id}`, `DELETE /users/{id}`)
  - Role-based access (`role="admin"`) ด้วย JWT authentication
- **Data Integrity**:
  - ใช้ schema validation ด้วย Pydantic (`UserCreate`, `UserUpdate`, `UserOut`)
  - ตรวจสอบ email ซ้ำและ hash รหัสผ่านด้วย bcrypt
- **Performance Optimization**:
  - Backend response time <200ms ด้วย FastAPI
  - PostgreSQL partitioning และ index optimization สำหรับ dataset ขนาดใหญ่
- **Dashboard**:
  - Admin dashboard สำหรับจัดการผู้ใช้
- **Deployment**:
  - ใช้ Docker Compose สำหรับ PostgreSQL, FastAPI, React, และ Nginx
- **Testing**:
  - Test-Driven Development (TDD) ด้วย Postman
  - Automated testing สำหรับ API (`GET`, `POST`, `PUT`, `DELETE`)

## เทคโนโลยีที่ใช้

| ส่วนประกอบ         | เทคโนโลยี                           |
| ------------------ | ----------------------------------- |
| **Backend**        | FastAPI (Python), MVC Pattern       |
| **Frontend**       | Vite, React, TypeScript             |
| **Database**       | PostgreSQL, pgAdmin                 |
| **Authentication** | JWT, bcrypt                         |
| **Deployment**     | Docker Compose, Nginx(comming soon) |
| **Testing**        | Postman, Supertest (Node.js)        |

## ขั้นตอนการติดตั้งและรันโปรเจกต์

### ความต้องการ

- git + hub
- Docker และ Docker Compose
- PG Admin ติดตั้งบนเครื่อง เอาไว้จัดการ database สามารถ load free ได้ที่ official pgadmin website มีใน window linux และ mac
- Postman เอาไว้ทดสอบ API

ที่เหลือไม่ต้องลงเพิ่มเพราะโปรเจกต์นี้เป็น cloud native application

### ขั้นตอน

1. **Clone repository**:

   ```bash
   git clone https://github.com/ssszZ-TH/party_fullstack_docker3.git
   ```

2. **ตั้งค่า environment**:

- /backend/app/config/setting ต้องเเก้ใขให้เป็นฉบับองคุณเอง เพื่อความปลอดภัยของระบบ (ถ้าเปลี่ยน key ก็จะต้องสร้าง user ใหม่ทั้งหมด เพราะ database มีการเก็บ password hashing + salt)

  ```python

   DATABASE_URL = "postgresql://spa:spa@db:5432/myapp"
   API_HOST = "0.0.0.0"
   API_PORT = 8080
   SECRET_KEY = "8c2f7a9b3d6e1f0c4a8b2d5e7f9a1c3b6d8e0f2a4b7c9d1e3f5a8b0c2d4e6f"
   BCRYPT_SALT = "$2b$12$zDZMoHsxUdSvpuNJjEzsve"

  ```

3. **รัน Docker Compose**:

   ```bash
   docker-compose up --build -d
   ```

   - Backend: `http://localhost:8080`
   - Frontend: `http://localhost:5173`
   - Postgres: `http://localhost:5432`

4. **ตั้งค่า pgadmin**:

   pg admin คือ program ที่มี GUI ไว้ใช้จัดการ database postgres เเบบง่าย เครื่องมือครบ

   - load pgadmin ใน มาติดตั้งใน computer ให้เรียบร้อย
   - เพิ่ม database server ตาม url ของ database ในที่นี้คือ localhost และ port 5432
   - เพิ่ม user ในที่นี้คือ spa และ password ในที่นี้คือ spa username password สามารถเปลี่ยนได้ที่ docker-compose.yml
   - ชื่อ database ใส่อะไรก็ได้ ไม่มีผล
   - คลิปสอนใช้ pgadmin https://youtu.be/WFT5MaZN6g4

5. **รัน frontend** (ถ้าต้องการรันแยก):
   ```bash
   cd frontend
   npm i
   npm run dev
   ```

## ตัวอย่างการใช้งาน API

### สมัครผู้ใช้

```bash
curl -X POST "http://localhost:8080/auth/register" \
-H "Content-Type: application/json" \
-d '{"name":"Jane Doe","email":"jane@example.com","password":"securepassword"}'
```

**ผลลัพธ์**:

```json
{ "message": "User created" }
```

### Login

```bash
curl -X POST "http://localhost:8080/auth/login" \
-H "Content-Type: application/json" \
-d '{"email":"jane@example.com","password":"securepassword"}'
```

**ผลลัพธ์**:

```json
{ "access_token": "eyJhbG...", "token_type": "bearer" }
```

**เพิ่มเติม**:
access_token จะเก็บ {sub: id ของ user, role: role ของ user} เเละเก็บ expire time ไว้ด้วย 30 นาที (now + 30 minutes)
ทั้งหมดจะถูกเข้ารหัสด้วย secret key ที่เรากําหนดไว้

### ดึงข้อมูลผู้ใช้ (ต้องใช้ JWT)
เอา access_token เมื่อกี้ไปวางใน header

```bash
curl -X GET "http://localhost:8080/users/1" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <JWT_TOKEN>"
```

**ผลลัพธ์**:

```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": null,
  "role": "admin"
}
```

## การทดสอบ

- **Postman**:
  - นำเข้า collection จาก `/tests/postman_collection.json`
  - ทดสอบ API (`GET`, `POST`, `PUT`, `DELETE`) และตรวจสอบ `role="admin"`
- **Supertest** (ถ้ามี):
  - รัน automated tests:
    ```bash
    cd backend
    npm install supertest
    npm test
    ```

## การปรับปรุงในอนาคต

- เพิ่ม **dark theme** และปรับ font ใน frontend
- Migrate backend ไป **Express.js** หรือปรับปรุง FastAPI เพื่อ response time <200ms
- เพิ่ม **Multi-Factor Authentication (MFA)**
- ใช้ **Supertest** สำหรับ automated testing
- ปรับปรุง PostgreSQL ด้วย partitioning และ index optimization สำหรับ dataset ขนาดใหญ่

## ผู้พัฒนา

- **ชื่อ**: Sitthipong Chamratritthirong
- **รหัสนักศึกษา**: 64...19
- **อีเมล**: sitthipong.cham@gmail.com
- **GitHub**: https://github.com/ssszZ-TH

## ที่มา

โปรเจกต์นี้พัฒนาเป็นส่วนหนึ่งของโปรเจกต์จบ วิศวกรรมคอมพิวเตอร์ โดยอ้างอิง **The Data Model Resource Book** สำหรับการออกแบบ schema และเน้น data integrity และ performance optimization.
