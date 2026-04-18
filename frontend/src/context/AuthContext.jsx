import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { api } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for stored token on mount
    const token = localStorage.getItem('token');
    if (token) {
      validateToken(token);
    } else {
      setLoading(false);
    }
  }, []);

  const validateToken = async (token) => {
    try {
      const response = await axios.get('/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
      // Ensure future requests use this token
      const authHeader = `Bearer ${token}`;
      axios.defaults.headers.common['Authorization'] = authHeader;
      api.defaults.headers.common['Authorization'] = authHeader;
    } catch (error) {
      console.error('Session expired');
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    const response = await axios.post('/api/v1/auth/login', { email, password });
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    const authHeader = `Bearer ${access_token}`;
    axios.defaults.headers.common['Authorization'] = authHeader;
    api.defaults.headers.common['Authorization'] = authHeader;
    await validateToken(access_token);
  };

  const register = async (email, password, fullName) => {
    await axios.post('/api/v1/auth/register', { email, password, full_name: fullName });
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
