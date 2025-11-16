'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from './api-client';

interface User {
  id: string;
  email: string;
  full_name: string;
  role?: string;
  institution?: string;
  research_interests?: string[];
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  logout: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  isAuthenticated: boolean;
  token: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);

  // Load user from localStorage on mount
  useEffect(() => {
    const loadUser = async () => {
      try {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          apiClient.setToken(storedToken);
        }
      } catch (error) {
        console.error('Failed to load user from localStorage:', error);
        // Clear invalid data
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch(`${apiClient.getBaseURL()}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      const data = await response.json();

      // Store token and user
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      setToken(data.access_token);
      setUser(data.user);
      apiClient.setToken(data.access_token);
    } catch (error: any) {
      console.error('Login error:', error);
      throw new Error(error.message || 'Login failed');
    }
  };

  const register = async (data: RegisterData) => {
    try {
      const response = await fetch(`${apiClient.getBaseURL()}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }

      const result = await response.json();

      // Store token and user
      localStorage.setItem('token', result.access_token);
      localStorage.setItem('user', JSON.stringify(result.user));

      setToken(result.access_token);
      setUser(result.user);
      apiClient.setToken(result.access_token);
    } catch (error: any) {
      console.error('Registration error:', error);
      throw new Error(error.message || 'Registration failed');
    }
  };

  const logout = async () => {
    try {
      // Call logout endpoint (optional - just for logging)
      if (token) {
        await fetch(`${apiClient.getBaseURL()}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }).catch(() => {
          // Ignore errors - logout should always succeed client-side
        });
      }
    } finally {
      // Clear local state
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setToken(null);
      setUser(null);
      apiClient.clearToken();
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        logout,
        login,
        register,
        isAuthenticated: !!user && !!token,
        token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
