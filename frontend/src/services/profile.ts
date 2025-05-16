import axios from 'axios';
import Cookies from 'js-cookie';

// กำหนด BASE_URL สำหรับ API endpoint ของ users
const BASE_URL = 'http://localhost:8080/users';

// ฟังก์ชันสำหรับ log error เพื่อแสดงรายละเอียดข้อผิดพลาดใน console
// ใช้เพื่อ debug และบันทึกข้อมูล error เช่น status code และ response data
const logError = (method: string, error: any) => {
  console.error(`Error in ${method} request to ${BASE_URL}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    stack: error.stack,
  });
};

// ฟังก์ชันสำหรับดึงข้อมูลโปรไฟล์ผู้ใช้ปัจจุบัน
// ไม่ต้องรับ payload เพราะใช้ Bearer Token จาก cookie เพื่อระบุผู้ใช้
export async function getProfile({}: {}) {
  try {
    // ดึง access_token จาก cookie
    const token = Cookies.get('access_token');
    
    // ตรวจสอบว่า token มีอยู่หรือไม่
    if (!token) {
      throw new Error('No access token found');
    }

    // เรียก API ด้วย axios เพื่อดึงข้อมูลผู้ใช้จาก endpoint /users/me
    // ส่ง Bearer Token ใน header Authorization
    const res = await axios.get(`${BASE_URL}/me`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    // คืนข้อมูลผู้ใช้ที่ได้จาก API
    return res.data;
  } catch (error: any) {
    // เรียก logError เพื่อบันทึกข้อผิดพลาด
    logError('getProfile', error);
    // โยน error ต่อให้ caller (เช่น Profile.tsx) จัดการ
    throw error;
  }
}