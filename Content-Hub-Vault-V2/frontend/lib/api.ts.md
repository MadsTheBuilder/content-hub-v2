---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/lib/api.ts"
category: "Content Hub Source Code"
---

# api.ts

**Description:** Frontend shared utilities, API clients, or TypeScript type definitions.

---

```typescript
const API_BASE = "/api/v1";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

async function fetchAPI(path: string, options: RequestInit = {}) {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  // Auth wall disabled for MVP — single-user mode
  // if (res.status === 401) {
  //   localStorage.removeItem("access_token");
  //   window.location.href = "/login";
  //   throw new Error("Unauthorized");
  // }
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }
  return res.json();
}

// Auth
export const auth = {
  signup: (email: string, password: string, display_name: string) =>
    fetchAPI("/auth/signup", { method: "POST", body: JSON.stringify({ email, password, display_name }) }),
  login: async (email: string, password: string) => {
    const data = await fetchAPI("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
    if (data.session?.access_token) {
      localStorage.setItem("access_token", data.session.access_token);
    }
    return data;
  },
  logout: () => {
    localStorage.removeItem("access_token");
    return fetchAPI("/auth/logout", { method: "POST" });
  },
  me: () => fetchAPI("/auth/me"),
};

// Workflows
export const workflows = {
  list: () => fetchAPI("/workflows"),
  get: (id: string) => fetchAPI(`/workflows/${id}`),
  create: (data: Record<string, unknown>) => fetchAPI("/workflows", { method: "POST", body: JSON.stringify(data) }),
  update: (id: string, data: Record<string, unknown>) => fetchAPI(`/workflows/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id: string) => fetchAPI(`/workflows/${id}`, { method: "DELETE" }),
  templates: () => fetchAPI("/workflows/templates"),
  scrape: (id: string) => fetchAPI(`/workflows/${id}/scrape`, { method: "POST" }),
  trending: (id: string) => fetchAPI(`/workflows/${id}/trending`),
  suggestions: (id: string) => fetchAPI(`/workflows/${id}/suggestions`),
  recordSelections: (id: string, post_ids: string[]) =>
    fetchAPI(`/workflows/${id}/selections`, { method: "POST", body: JSON.stringify({ selected_post_ids: post_ids }) }),
};

// Content
export const content = {
  generate: (data: { workflow_id: string; content_type: string; platform: string; topic: string }) =>
    fetchAPI("/content/generate", { method: "POST", body: JSON.stringify(data) }),
  status: (id: string) => fetchAPI(`/content/status/${id}`),
  get: (id: string) => fetchAPI(`/content/${id}`),
  library: (params?: { workflow_id?: string; content_type?: string; platform?: string }) => {
    const query = new URLSearchParams();
    if (params?.workflow_id) query.set("workflow_id", params.workflow_id);
    if (params?.content_type) query.set("content_type", params.content_type);
    if (params?.platform) query.set("platform", params.platform);
    return fetchAPI(`/content/library?${query}`);
  },
  calendar: () => fetchAPI("/content/calendar"),
  download: (id: string) => fetchAPI(`/content/${id}/download`),
  edit: (id: string, edited_script: string) =>
    fetchAPI(`/content/${id}/edit`, { method: "PUT", body: JSON.stringify({ edited_script }) }),
  publish: (id: string) => fetchAPI(`/content/${id}/publish`, { method: "PUT" }),
  delete: (id: string) => fetchAPI(`/content/${id}`, { method: "DELETE" }),
  editHistory: (id: string) => fetchAPI(`/content/${id}/edit-history`),
  synthesize: (data: { workflow_id: string; selected_post_ids: string[]; platform: string }) =>
    fetchAPI("/content/synthesize", { method: "POST", body: JSON.stringify(data) }),
  generateFromStrategy: (data: { workflow_id: string; strategy: Record<string, unknown>; original_strategy?: Record<string, unknown>; user_notes?: string; content_type?: string }) =>
    fetchAPI("/content/generate-from-strategy", { method: "POST", body: JSON.stringify(data) }),
};

// Brand
export const brand = {
  get: (workflowId: string) => fetchAPI(`/brand/${workflowId}`),
  update: (workflowId: string, data: Record<string, unknown>) =>
    fetchAPI(`/brand/${workflowId}`, { method: "PUT", body: JSON.stringify(data) }),
};

```
