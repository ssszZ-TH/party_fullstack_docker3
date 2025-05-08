-- สร้างตาราง users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- สร้าง index สำหรับฟิลด์ email เพื่อ optimize การ query
CREATE INDEX idx_users_email ON users (email);