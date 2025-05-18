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
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    const token = Cookies.get('access_token');
    console.log('AuthContext: Initial token check:', token ? 'Token exists' : 'No token');
    return !!token;
  });

  useEffect(() => {
    console.log('AuthContext: Running useEffect');
    const token = Cookies.get('access_token');
    setIsAuthenticated(!!token);
  }, []);

  const login = (token: string) => {
    try {
      Cookies.set('access_token', token, { expires: 1, secure: true, sameSite: 'strict' });
      setIsAuthenticated(true);
      console.log('AuthContext: Login successful, token set');
    } catch (error) {
      console.error('AuthContext: Error when setting cookie:', error);
      setIsAuthenticated(false);
    }
  };

  const logout = () => {
    try {
      Cookies.remove('access_token');
      setIsAuthenticated(false);
      console.log('AuthContext: Logout successful, token removed');
    } catch (error) {
      console.error('AuthContext: Error when removing cookie:', error);
      setIsAuthenticated(false);
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};