---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/next.config.mjs"
category: "Content Hub Source Code"
---

# next.config.mjs

**Description:** Implementation asset: next.config.mjs

---

```mjs
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      { source: '/api/:path*', destination: 'http://127.0.0.1:8000/api/:path*' },
    ];
  },
};

export default nextConfig;

```
