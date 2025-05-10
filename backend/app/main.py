from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import database
from app.controllers.users.user import router as user_router
from app.controllers.auth.auth import router as auth_router
from app.controllers.marital_status_type import router as marital_status_type_router
from app.controllers.minority_type import router as minority_type_router

# โหลด .env ก่อน import อื่นๆ
load_dotenv()

app = FastAPI()

# CORS สำหรับ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# รวม routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(marital_status_type_router)
app.include_router(minority_type_router)

# รวม routers อื่นๆ ที่มีใน controllers

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "FastAPI Backend"}