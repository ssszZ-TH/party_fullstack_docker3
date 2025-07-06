import axios from "axios";
import Cookies from "js-cookie";

const BASE_URL = "http://localhost:8080/v1/partyrelationshipstatustype";

const logError = (method: string, error: any) => {
  console.error(`Error in ${method} request to ${BASE_URL}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    stack: error.stack,
  });
};

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = Cookies.get("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function list() {
  try {
    const res = await api.get("/");
    return res.data;
  } catch (error: any) {
    logError("list", error);
    throw error;
  }
}

export async function get({ id }: { id: number }) {
  try {
    const res = await api.get(`/${id}`);
    return res.data;
  } catch (error: any) {
    logError("get", error);
    throw error;
  }
}

export async function create({ description }: { description: string }) {
  try {
    const res = await api.post("/", { description });
    return res.data;
  } catch (error: any) {
    logError("create", error);
    throw error;
  }
}

export async function update({
  id,
  description,
}: {
  id: number;
  description: string;
}) {
  try {
    const res = await api.put(`/${id}`, { description });
    return res.data;
  } catch (error: any) {
    logError("update", error);
    throw error;
  }
}

export async function deleteById({ id }: { id: number }) {
  try {
    const res = await api.delete(`/${id}`);
    return res.data;
  } catch (error: any) {
    logError("deleteById", error);
    throw error;
  }
}