'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useUser, useAuth as useClerkAuth, useSignUp, useSignIn } from '@clerk/nextjs';

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
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { user: clerkUser, isLoaded } = useUser();
  const { signOut } = useClerkAuth();
  const { signUp, setActive: setActiveSignUp } = useSignUp();
  const { signIn, setActive: setActiveSignIn } = useSignIn();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (isLoaded && clerkUser) {
      // Map Clerk user to our User interface
      setUser({
        id: clerkUser.id,
        email: clerkUser.primaryEmailAddress?.emailAddress || '',
        full_name: clerkUser.fullName || clerkUser.firstName || 'User',
        role: clerkUser.publicMetadata?.role as string || undefined,
        institution: clerkUser.publicMetadata?.institution as string || undefined,
        research_interests: clerkUser.publicMetadata?.research_interests as string[] || undefined,
      });
    } else if (isLoaded && !clerkUser) {
      setUser(null);
    }
  }, [clerkUser, isLoaded]);

  const login = async (email: string, password: string) => {
    if (!signIn) {
      throw new Error('Sign in is not available');
    }

    try {
      const result = await signIn.create({
        identifier: email,
        password,
      });

      if (result.status === 'complete') {
        await setActiveSignIn({ session: result.createdSessionId });
      } else {
        throw new Error('Sign in incomplete. Please try again.');
      }
    } catch (error: any) {
      console.error('Login error:', error);
      throw new Error(error.errors?.[0]?.message || error.message || 'Login failed');
    }
  };

  const register = async (data: RegisterData) => {
    if (!signUp) {
      throw new Error('Sign up is not available');
    }

    try {
      // Split full name into first and last name
      const nameParts = data.full_name.trim().split(' ');
      const firstName = nameParts[0];
      const lastName = nameParts.slice(1).join(' ') || '';

      // Create the sign-up
      const result = await signUp.create({
        emailAddress: data.email,
        password: data.password,
        firstName,
        lastName,
      });

      // If email verification is not required, set the session active
      if (result.status === 'complete') {
        await setActiveSignUp({ session: result.createdSessionId });
      } else if (result.status === 'missing_requirements') {
        // Email verification required - prepare email verification
        await signUp.prepareEmailAddressVerification({ strategy: 'email_code' });
        // Return success - the UI should handle showing verification input
        return;
      } else {
        // Handle email verification if required
        throw new Error('Registration initiated. Please check your email for verification code.');
      }
    } catch (error: any) {
      console.error('Registration error:', error);
      throw new Error(error.errors?.[0]?.message || error.message || 'Registration failed');
    }
  };

  const logout = async () => {
    await signOut();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading: !isLoaded,
        logout,
        login,
        register,
        isAuthenticated: !!user,
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
