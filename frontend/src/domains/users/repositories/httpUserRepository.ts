import { api } from "@/shared/lib/api";
import type { User, Settings } from "@/shared/types";
import type { UserRepository, LoginResponse } from "./userRepository";

export class HttpUserRepository implements UserRepository {
  async getCurrentUser(token?: string | null): Promise<User | null> {
    try {
      return await api.get<User>("/users/me", token);
    } catch {
      return null;
    }
  }

  async login(username: string, password: string): Promise<LoginResponse> {
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);
    return await api.postForm<LoginResponse>("/auth/login", null, body);
  }

  async logout(token?: string | null): Promise<void> {
    try {
      await api.post<void>("/auth/logout", token ?? null, undefined);
    } catch (err) {
      console.warn("Logout failed", err);
    }
  }

  async refresh(): Promise<LoginResponse> {
    return await api.post<LoginResponse>("/auth/refresh", null, null as unknown as undefined);
  }

  async register(email: string, username: string, password: string): Promise<void> {
    await api.post<void>("/auth/register", null, { email, username, password });
  }

  async getSettings(token?: string | null): Promise<Settings | null> {
    try {
      return await api.get<Settings>("/users/settings", token);
    } catch {
      return null;
    }
  }

  async updateSettings(token?: string | null, data?: unknown): Promise<void> {
    await api.put("/users/settings", token ?? null, data);
  }
}

export default HttpUserRepository;
