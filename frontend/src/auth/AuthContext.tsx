"use client";
import React, { createContext, useContext, useEffect, useState } from "react";
import { useLocalStorage } from "../hooks/useLocalStorage";
import { api } from "../lib/api";
import type { User } from "../types";

type AuthContextType = {
  token: string | null;
  currentUser: User | null | undefined; // undefined = loading
  loading: boolean;
  signIn: (username: string, password: string) => Promise<void>;
  signOut: () => void;
  register?: (email: string, username: string, password: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [storedToken, setStoredToken] = useLocalStorage<string | null>("auth_token", null);
  const [token, setToken] = useState<string | null>(storedToken);
  const [currentUser, setCurrentUser] = useState<User | null | undefined>(undefined);

  useEffect(() => {
    setStoredToken(token);
  }, [token, setStoredToken]);

  useEffect(() => {
    // When token changes, fetch current user or clear and schedule expiry handling
    let mounted = true;
    let expiryTimer: number | undefined;

    const scheduleExpiry = (jwt: string) => {
      // Decode JWT payload to get exp claim (in seconds)
      try {
        const parts = jwt.split(".");
        if (parts.length < 2) return undefined;
        const payload = JSON.parse(atob(parts[1].replace(/-/g, "+").replace(/_/g, "/")));
        const exp = payload.exp as number | undefined;
        if (!exp) return undefined;
        const msUntil = exp * 1000 - Date.now();
        if (msUntil <= 0) {
          // Already expired
          signOut();
          return undefined;
        }

        // Schedule a refresh a bit before expiry (e.g., 60 seconds before)
        const refreshBeforeMs = Math.min(60000, Math.floor(msUntil / 2));
        const refreshIn = msUntil - refreshBeforeMs;

        return window.setTimeout(async () => {
          // Attempt token refresh
          try {
            // Call refresh endpoint; refresh token is sent/validated via HttpOnly cookie
            const data = await api.post<{ access_token?: string }>("/auth/refresh", null, undefined);
            if (data?.access_token) {
              setToken(data.access_token);
            } else {
              signOut();
            }
          } catch (err) {
            console.error("Refresh failed:", err);
            signOut();
          }
        }, refreshIn);
      } catch (err) {
        console.warn("Failed to schedule token expiry", err);
        return undefined;
      }
    };

    const fetchCurrentUser = async () => {
      if (!token) {
        setCurrentUser(null);
        return;
      }
      setCurrentUser(undefined);
      try {
        const data = await api.get<User>("/users/me", token);
        if (!mounted) return;
        setCurrentUser(data);
      } catch (err) {
        console.error("Failed fetching current user:", err);
        if (mounted) setCurrentUser(null);
        setToken(null);
      }
    };

    if (token) {
      expiryTimer = scheduleExpiry(token);
      void fetchCurrentUser();
    } else {
      setCurrentUser(null);
    }

    return () => {
      mounted = false;
      if (expiryTimer) window.clearTimeout(expiryTimer);
    };
  }, [token]);

  const signIn = async (username: string, password: string): Promise<void> => {
    // Backend expects OAuth2 form data: username, password
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);
    // Include credentials so the browser accepts HttpOnly refresh cookie from the server
    const data = await api.postForm<{ access_token?: string }>("/auth/login", null, body);
    if (!data?.access_token) throw new Error("No access token returned");
    setToken(data.access_token);
  };

  const register = async (email: string, username: string, password: string): Promise<void> => {
    await api.post<void>("/auth/register", null, { email, username, password });
    // Optionally auto-login after register
    return;
  };

  const signOut = (): void => {
    // attempt to inform server to clear refresh cookie and revoke tokens
    // call and explicitly handle errors to avoid unhandled promise rejections
    void api
      .post<void>("/auth/logout", token ?? null, undefined)
      .catch((err: unknown) => console.warn("Logout request failed", err));
    setToken(null);
    setCurrentUser(null);
  };

  const value: AuthContextType = {
    token,
    currentUser,
    loading: currentUser === undefined,
    signIn,
    signOut,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

export function useAuthActions() {
  const { signIn, signOut, register } = useAuth();
  return { signIn, signOut, register };
}

export default AuthContext;
