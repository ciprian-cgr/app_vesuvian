// Shared frontend types
export type ISODateString = string;

export interface User {
  id: number;
  email: string;
  username: string;
  created_at?: ISODateString;
}

export interface Settings {
  // extend with concrete fields as your backend exposes them
  locale?: string;
  theme?: "light" | "dark";
  [key: string]: unknown;
}

export interface ApiError {
  detail?: string | Record<string, unknown> | string[];
  [key: string]: unknown;
}
