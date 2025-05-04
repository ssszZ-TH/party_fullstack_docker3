# ใช้ Python 3.13-slim เป็นฐาน
FROM python:3.13-slim

# ติดตั้ง dependencies สำหรับ psycopg2 และ FastAPI
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# กำหนด working directory
WORKDIR /app

# คัดลอก requirements.txt ก่อนเพื่อใช้ cache
COPY requirements.txt .

# ติดตั้ง dependencies และล้าง cache
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# # สร้าง non-root user
# RUN useradd -m appuser
# USER appuser

# # เปิดพอร์ต
# EXPOSE 8080

# คำสั่งเริ่มต้น (จะถูกแทนที่ใน docker-compose.yml)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]