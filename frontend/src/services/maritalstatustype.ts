import axios from "axios";
import Cookies from "js-cookie";
const BASE_URL = "http://localhost:8080/v1/maritalstatustype";

// ฟังก์ชันสำหรับ log error (สามารถปรับแต่งได้)
const logError = (method: string, error: any) => {
  console.error(`Error in ${method} request to ${BASE_URL}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
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

export async function list() {
  try {
    const res = await axios.get(BASE_URL, { headers: getAuthHeaders() });
    return res.data;
  } catch (error: any) {
    logError("list", error);
    throw error; // โยน error ต่อไปให้ caller จัดการ
  }
}

export async function get({ id }: { id: number }) {
  try {
    const res = await axios.get(`${BASE_URL}/${id}`, { headers: getAuthHeaders() });
    return res.data;
  } catch (error: any) {
    logError("get", error);
    throw error;
  }
}

export async function create(data: any) {
  try {
    const res = await axios.post(BASE_URL, data, {headers: getAuthHeaders()});
    return res.data;
  } catch (error: any) {
    logError("create", error);
    throw error;
  }
}

export async function update(data: any) {
  try {
    const res = await axios.put(`${BASE_URL}/${data.id}`, data, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error: any) {
    logError("update", error);
    throw error;
  }
}

export async function deleteById({ id }: { id: number }) {
  try {
    const res = await axios.delete(`${BASE_URL}/${id}`, { headers: getAuthHeaders() });
    return res.data;
  } catch (error: any) {
    logError("deleteById", error);
    throw error;
  }
}