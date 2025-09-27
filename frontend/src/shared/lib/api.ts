import { ApiError } from "@/shared/types";

const API_PREFIX = import.meta.env.VITE_API_PREFIX || "/api/v1";

function buildUrl(path: string) {
  if (path.startsWith("/")) return `${API_PREFIX}${path}`;
  return `${API_PREFIX}/${path}`;
}

async function parseJsonSafe(res: Response): Promise<unknown> {
  const text = await res.text();
  try {
    return text ? JSON.parse(text) : null;
  } catch (_err) {
    return text;
  }
}

export async function apiFetch<T = unknown>(
  path: string,
  token?: string | null,
  options: {
    method?: string;
    json?: unknown;
    form?: URLSearchParams;
    headers?: Record<string, string>;
    credentials?: RequestCredentials;
  } = {},
): Promise<T> {
  const url = buildUrl(path);
  const headers: Record<string, string> = options.headers ? { ...options.headers } : {};

  let body: BodyInit | undefined;
  if (options.json !== undefined) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(options.json);
  } else if (options.form) {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    body = options.form.toString();
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(url, { method: options.method ?? "GET", headers, body, credentials: options.credentials ?? "include" });
  const data = await parseJsonSafe(res);
  if (!res.ok) {
    const message = (data && (typeof data === "object" ? (data as ApiError).detail : data)) || res.statusText || "Request failed";
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }
  return data as T;
}

export const api = {
  get: <T = unknown>(path: string, token?: string | null) => apiFetch<T>(path, token, {}),
  post: <T = unknown>(path: string, token?: string | null, json?: unknown) => apiFetch<T>(path, token, { method: "POST", json }),
  put: <T = unknown>(path: string, token?: string | null, json?: unknown) => apiFetch<T>(path, token, { method: "PUT", json }),
  postForm: <T = unknown>(path: string, token: string | null, form: URLSearchParams) => apiFetch<T>(path, token, { method: "POST", form }),
};

export default api;
