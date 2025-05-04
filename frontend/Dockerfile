# ใช้ Node.js image เป็นฐาน
FROM node:23-alpine

# กำหนด working directory
WORKDIR /app

# คัดลอก package.json และ package-lock.json
COPY package*.json ./

# ติดตั้ง dependencies
RUN npm install

# คัดลอกโค้ดทั้งหมด
COPY . .

# เปิดพอร์ต (เพื่อเอกสาร)
EXPOSE 5173

# คำสั่งเริ่มต้น (จะถูกแทนที่ด้วย command ใน docker-compose.yml)
# CMD ["npm", "run", "dev"]