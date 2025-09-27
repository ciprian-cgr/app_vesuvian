import type { User, Settings } from "@/shared/types";

export type LoginResponse = { access_token?: string } | null;

export interface UserRepository {
  getCurrentUser(token?: string | null): Promise<User | null>;
  login(username: string, password: string): Promise<LoginResponse>;
  logout(token?: string | null): Promise<void>;
  refresh(): Promise<LoginResponse>;
  register?(email: string, username: string, password: string): Promise<void>;

  // Settings
  getSettings(token?: string | null): Promise<Settings | null>;
  updateSettings(token?: string | null, data?: unknown): Promise<void>;
}

// NOTE: intentionally no default export; consumers should import the named interface
