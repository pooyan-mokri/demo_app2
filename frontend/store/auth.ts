"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { apiFetch } from "@/lib/api";

interface AuthState {
  user: { email: string; fullName: string } | null;
  tokens: { accessToken: string; refreshToken: string } | null;
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      tokens: null,
      login: async (credentials) => {
        const formData = new URLSearchParams();
        formData.append("username", credentials.email);
        formData.append("password", credentials.password);

        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData
        });
        if (!response.ok) {
          throw new Error("Login failed");
        }
        const data = await response.json();
        set({
          tokens: { accessToken: data.access_token, refreshToken: data.refresh_token },
          user: { email: credentials.email, fullName: credentials.email.split("@")[0] }
        });
      },
      logout: () => set({ user: null, tokens: null })
    }),
    {
      name: "themoak-auth"
    }
  )
);

function normalizeHeaders(headers?: HeadersInit): Record<string, string> {
  if (!headers) {
    return {};
  }
  if (headers instanceof Headers) {
    return Object.fromEntries(headers.entries());
  }
  if (Array.isArray(headers)) {
    return Object.fromEntries(headers);
  }
  return { ...headers };
}

export async function authenticatedFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const { tokens } = useAuthStore.getState();
  const headers = normalizeHeaders(options?.headers);
  if (tokens?.accessToken) {
    headers["Authorization"] = `Bearer ${tokens.accessToken}`;
  }
  return apiFetch<T>(endpoint, { ...options, headers });
}
