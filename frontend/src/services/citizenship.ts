import axios from 'axios';
import Cookies from 'js-cookie';

// กำหนด BASE_URL สำหรับ API endpoint ของ citizenship
const BASE_URL = 'http://localhost:8080/v1/citizenship';

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

// ดึงรายการทั้งหมด
export async function list() {
  try {
    const res = await axios.get(BASE_URL, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error: any) {
    logError('list', error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}

// ดึงข้อมูลตาม ID
export async function get({ id }: { id: number }) {
  try {
    const res = await axios.get(`${BASE_URL}/${id}`, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error: any) {
    logError('get', error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}

// สร้างข้อมูลใหม่
export async function create(data: any) {
  // ป้องกัน error จากวันที่เป็น string ว่าง
  data.thrudate = data.thrudate?.trim() || null;
  try {
    const res = await axios.post(BASE_URL, data, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error: any) {
    logError('create', error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}

// อัพเดทข้อมูล
export async function update(data: any) {
  // ป้องกัน error จากวันที่เป็น string ว่าง
  data.thrudate = data.thrudate?.trim() || null;
  try {
    const res = await axios.put(`${BASE_URL}/${data.id}`, data, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error: any) {
    logError('update', error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}

// ลบข้อมูลตาม ID
export async function deleteById({ id }: { id: number }) {
  try {
    const res = await axios.delete(`${BASE_URL}/${id}`, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error: any) {
    logError('deleteById', error, Cookies.get('access_token'));
    if (error.response?.status === 401) {
      throw new Error('Unauthorized: Invalid or expired token');
    }
    throw error;
  }
}