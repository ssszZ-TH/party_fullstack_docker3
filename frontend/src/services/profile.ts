import axios from 'axios';
import Cookies from 'js-cookie';

// กำหนด BASE_URL สำหรับ API endpoint ของ users
const BASE_URL = 'http://localhost:8080/users';

// ฟังก์ชันสำหรับ log error เพื่อแสดงรายละเอียดข้อผิดพลาดใน console
const logError = (method: string, error: any, token?: string) => {
  console.error(`Error in ${method} request to ${BASE_URL}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    token: token ? `Bearer ${token}` : 'No token provided',
    stack: error.stack,
  });
};

// ฟังก์ชันดึง access_token จาก cookie
const getAuthHeaders = () => {
  const token = Cookies.get('access_token');
  if (!token) {
    throw new Error('No access token found');
  }
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

// ฟังก์ชันสำหรับดึงข้อมูลโปรไฟล์ผู้ใช้ปัจจุบัน
// ไม่ต้องรับ payload เพราะใช้ Bearer Token จาก cookie เพื่อระบุผู้ใช้
export async function getProfile({}: {}) {
  try {
    const res = await axios.get(`${BASE_URL}/me`, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error: any) {
    logError('getProfile', error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}