Full-Stack Development Based on Reference Data Model
โปรเจกต์จบสำหรับการพัฒนาระบบ Full-Stack โดยใช้ FastAPI (Python), React + TypeScript, และ PostgreSQL รองรับการจัดการข้อมูลผู้ใช้ด้วย role-based authentication (เฉพาะ admin) และ deploy ด้วย Docker Compose โปรเจกต์นี้เน้น data integrity, performance optimization และ scalability สำหรับ dataset ขนาดใหญ่ (>100,000 records).
ผู้พัฒนา: สิทธิพงษ์ จำรัสฤทธิรงค์ (รหัสนักศึกษา 6410301019)
คุณสมบัติหลัก

การจัดการผู้ใช้:
CRUD operations (POST /users, GET /users/{id}, PUT /users/{id}, DELETE /users/{id})
Role-based access (role="admin") ด้วย JWT authentication


Data Integrity:
ใช้ schema validation ด้วย Pydantic (UserCreate, UserUpdate, UserOut)
ตรวจสอบ email ซ้ำและ hash รหัสผ่านด้วย bcrypt


Performance Optimization:
Backend response time <200ms ด้วย FastAPI
PostgreSQL partitioning และ index optimization สำหรับ dataset ขนาดใหญ่


Dashboard:
Admin dashboard สำหรับจัดการผู้ใช้


Deployment:
ใช้ Docker Compose สำหรับ PostgreSQL, FastAPI, React, และ Nginx


Testing:
Test-Driven Development (TDD) ด้วย Postman
Automated testing สำหรับ API (GET, POST, PUT, DELETE)



เทคโนโลยีที่ใช้



ส่วนประกอบ
เทคโนโลยี



Backend
FastAPI (Python), MVC Pattern


Frontend
Vite, React, TypeScript


Database
PostgreSQL, pgAdmin


Authentication
JWT, bcrypt


Deployment
Docker Compose, Nginx


Testing
Postman, Supertest (Node.js)


ขั้นตอนการติดตั้งและรันโปรเจกต์
ความต้องการ

Docker และ Docker Compose
Python 3.13+
Node.js 18+
PostgreSQL 15+

ขั้นตอน

Clone repository:
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>


ตั้งค่า environment:

สร้างไฟล์ .env ใน /backend:SECRET_KEY=8c2f7a9b3d6e1f0c4a8b2d5e7f9a1c3b6d8e0f2a4b7c9d1e3f5a8b0c2d4e6f
BCRYPT_SALT=$2b$12$abcdefghijklmnopqrstuv
DATABASE_URL=postgresql://spa:password@db:5432/myapp




รัน Docker Compose:
docker-compose up --build


Backend: http://localhost:8080
Frontend: http://localhost:3000
pgAdmin: http://localhost:5050


ตั้งค่า database:

เข้า pgAdmin (http://localhost:5050)
เพิ่ม server ด้วย DATABASE_URL จาก .env
สร้างตาราง users:CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'admin'
);




รัน frontend (ถ้าต้องการรันแยก):
cd frontend
npm install
npm run dev



ตัวอย่างการใช้งาน API
สมัครผู้ใช้
curl -X POST "http://localhost:8080/auth/register" \
-H "Content-Type: application/json" \
-d '{"name":"Jane Doe","email":"jane@example.com","password":"securepassword"}'

ผลลัพธ์:
{"message":"User created"}

Login
curl -X POST "http://localhost:8080/auth/login" \
-H "Content-Type: application/json" \
-d '{"email":"jane@example.com","password":"securepassword"}'

ผลลัพธ์:
{"access_token":"eyJhbG...","token_type":"bearer"}

ดึงข้อมูลผู้ใช้ (ต้องใช้ JWT)
curl -X GET "http://localhost:8080/users/1" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <JWT_TOKEN>"

ผลลัพธ์:
{
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": null,
    "role": "admin"
}

การทดสอบ

Postman:
นำเข้า collection จาก /tests/postman_collection.json
ทดสอบ API (GET, POST, PUT, DELETE) และตรวจสอบ role="admin"


Supertest (ถ้ามี):
รัน automated tests:cd backend
npm install supertest
npm test





การปรับปรุงในอนาคต

เพิ่ม dark theme และปรับ font ใน frontend
Migrate backend ไป Express.js หรือปรับปรุง FastAPI เพื่อ response time <200ms
เพิ่ม Multi-Factor Authentication (MFA)
ใช้ Supertest สำหรับ automated testing
ปรับปรุง PostgreSQL ด้วย partitioning และ index optimization สำหรับ dataset ขนาดใหญ่

ผู้พัฒนา

ชื่อ: สิทธิพงษ์ จำรัสฤทธิรงค์
รหัสนักศึกษา: 6410301019
อีเมล: sitthipong@example.com
GitHub: https://github.com/

ที่มา
โปรเจกต์นี้พัฒนาเป็นส่วนหนึ่งของโปรเจกต์จบ วิทยาการคอมพิวเตอร์ โดยอ้างอิง The Data Model Resource Book สำหรับการออกแบบ schema และเน้น data integrity และ performance optimization.
