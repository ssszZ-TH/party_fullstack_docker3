// ไฟล์นี้เป็น service สำหรับจัดการ API calls สำหรับ classifybyindustry
import axios from "axios";
import Cookies from "js-cookie";

// Base URL สำหรับ API
const BASE_URL = "http://localhost:8080/v1/classifybyindustry";

// ฟังก์ชัน log error เพื่อ debug
const logError = (method: string, error: any) => {
  console.error(`Error in ${method} request to ${BASE_URL}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    stack: error.stack,
  });
};

// สร้าง Axios instance พร้อมตั้งค่า default
const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

// เพิ่ม interceptor เพื่อแนบ token ในทุก request
api.interceptors.request.use((config) => {
  const token = Cookies.get("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ดึงรายการทั้งหมด
export async function list() {
  try {
    const res = await api.get("/");
    return res.data;
  } catch (error: any) {
    logError("list", error);
    throw error;
  }
}

// ดึงข้อมูลตาม ID
export async function get({ id }: { id: number }) {
  try {
    const res = await api.get(`/${id}`);
    return res.data;
  } catch (error: any) {
    logError("get", error);
    throw error;
  }
}

// สร้างข้อมูลใหม่
export async function create({
  fromdate,
  thrudate,
  party_id,
  industry_type_id,
}: {
  fromdate: string;
  thrudate: string;
  party_id: number;
  industry_type_id: number;
}) {
  try {
    const res = await api.post("/", {
      fromdate,
      thrudate,
      party_id,
      industry_type_id,
    });
    return res.data;
  } catch (error: any) {
    logError("create", error);
    throw error;
  }
}

// อัพเดทข้อมูล
export async function update({
  id,
  fromdate,
  thrudate,
  party_id,
  industry_type_id,
}: {
  id: number;
  fromdate: string;
  thrudate: string;
  party_id: number;
  industry_type_id: number;
}) {
  try {
    const res = await api.put(`/${id}`, {
      fromdate,
      thrudate,
      party_id,
      industry_type_id,
    });
    return res.data;
  } catch (error: any) {
    logError("update", error);
    throw error;
  }
}

// ลบข้อมูล
export async function deleteById({ id }: { id: number }) {
  try {
    const res = await api.delete(`/${id}`);
    return res.data;
  } catch (error: any) {
    logError("deleteById", error);
    throw error;
  }
}