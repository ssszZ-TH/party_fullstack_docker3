# ใช้ Python 3.13-alpine เป็นฐาน
FROM python:3.13-alpine

# ติดตั้ง dependencies สำหรับ psycopg2 และ FastAPI
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    && rm -rf /var/cache/apk/*

# กำหนด working directory
WORKDIR /app

# คัดลอก requirements.txt
COPY requirements.txt .

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ด
COPY ./app .

# สร้าง non-root user
RUN adduser -D appuser
USER appuser

# เปิดพอร์ต
EXPOSE 8080

# คำสั่งเริ่มต้น (จะถูกแทนที่ใน docker-compose.yml)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]