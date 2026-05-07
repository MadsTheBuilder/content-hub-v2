---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/lib/auth.ts"
category: "Content Hub Source Code"
---

# auth.ts

**Description:** Frontend shared utilities, API clients, or TypeScript type definitions.

---

```typescript
"use client";

// Auth wall disabled for MVP — single-user mode
export function isAuthenticated(): boolean {
  return true;
}

export function requireAuth(): boolean {
  return true;
}

```
