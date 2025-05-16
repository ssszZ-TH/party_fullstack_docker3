import axios from 'axios';

// กำหนด BASE_URL สำหรับ API endpoint ของ authentication
const BASE_URL = 'http://localhost:8080/auth';

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

// ฟังก์ชันสำหรับสมัครสมาชิก
// รับ payload เป็น object ที่มี name, email, password
export async function register({ name, email, password }: { name: string; email: string; password: string }) {
  try {
    // เรียก API ด้วย axios เพื่อสมัครสมาชิก
    const res = await axios.post(`${BASE_URL}/register`, { name, email, password }, {
      headers: { 'Content-Type': 'application/json' },
    });

    // คืนข้อมูลจาก API (ถ้ามี)
    return res.data;
  } catch (error: any) {
    // เรียก logError เพื่อบันทึกข้อผิดพลาด
    logError('register', error);
    // โยน error ต่อให้ caller (เช่น Register.tsx) จัดการ
    throw new Error(error.response?.data?.message || 'Registration failed');
  }
}

// ฟังก์ชันสำหรับ login
// รับ payload เป็น object ที่มี email, password
export async function login({ email, password }: { email: string; password: string }) {
  try {
    // เรียก API ด้วย axios เพื่อ login
    const res = await axios.post(`${BASE_URL}/login`, { email, password }, {
      headers: { 'Content-Type': 'application/json' },
    });

    // คืน access_token จาก response
    return res.data.access_token;
  } catch (error: any) {
    // เรียก logError เพื่อบันทึกข้อผิดพลาด
    logError('login', error);
    // โยน error ต่อให้ caller (เช่น Login.tsx) จัดการ
    throw new Error(error.response?.data?.message || 'Login failed');
  }
}