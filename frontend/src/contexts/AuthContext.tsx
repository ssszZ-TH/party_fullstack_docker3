import React, { createContext, useState, useEffect } from 'react';
import Cookies from 'js-cookie';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // ตรวจสอบ token จาก cookie ตอนโหลดหน้า
    try {
      const token = Cookies.get('access_token');
      if (token) {
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Error accessing cookies:', error);
    }
  }, []);

  const login = (token: string) => {
    try {
      Cookies.set('access_token', token, { expires: 7, secure: true, sameSite: 'strict' });
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Error setting cookie:', error);
    }
  };

  const logout = () => {
    try {
      Cookies.remove('access_token');
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Error removing cookie:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};