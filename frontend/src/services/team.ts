// ไฟล์นี้เป็น service สำหรับจัดการ API calls สำหรับ team
// สามารถปรับใช้กับ family และ other_informal_organization ได้โดยเปลี่ยน BASE_URL เป็น /v1/family หรือ /v1/other_informal_organization
import axios from "axios";
import Cookies from "js-cookie";

// Base URL สำหรับ API
const BASE_URL = "http://localhost:8080/v1/team";

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
export async function create({ name_en, name_th }: { name_en: string; name_th: string }) {
  try {
    const res = await api.post("/", { name_en, name_th });
    return res.data;
  } catch (error: any) {
    logError("create", error);
    throw error;
  }
}

// อัพเดทข้อมูล
export async function update({
  id,
  name_en,
  name_th,
}: {
  id: number;
  name_en: string;
  name_th: string;
}) {
  try {
    const res = await api.put(`/${id}`, { name_en, name_th });
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