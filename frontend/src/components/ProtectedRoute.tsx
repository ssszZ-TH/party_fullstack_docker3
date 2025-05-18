import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

// ProtectedRoute component เพื่อป้องกันการเข้าถึง route สำหรับผู้ใช้ที่ไม่ได้ login
// ถ้า isAuthenticated เป็น true จะแสดง children ถ้าไม่ใช่จะ redirect ไป /login
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;