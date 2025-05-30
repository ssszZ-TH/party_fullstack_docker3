import axios from 'axios';
import Cookies from 'js-cookie';

const BASE_URL = 'http://localhost:8080/v1/person';

const logError = (method: string, error: any, token?: string) => {
  console.error(`Error in ${method} request to ${BASE_URL}:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data,
    token: token ? `Bearer ${token}` : 'No token provided',
    stack: error.stack,
  });
};

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

export async function create(data: { socialsecuritynumber: string; birthdate: string; mothermaidenname: string; totalyearworkexperience: number; comment: string; gender_id?: number }) {
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

export async function update(data: { id: number; socialsecuritynumber: string; birthdate: string; mothermaidenname: string; totalyearworkexperience: number; comment: string; gender_id?: number }) {
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