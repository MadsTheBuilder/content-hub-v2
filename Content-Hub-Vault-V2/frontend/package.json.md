---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/package.json"
category: "Content Hub Source Code"
---

# package.json

**Description:** Configuration, structured mapping, or static configuration file.

---

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --port 3003",
    "build": "next build",
    "start": "next start --port 3003",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18",
    "react-dom": "^18",
    "next": "14.2.35",
    "lucide-react": "^0.446.0",
    "framer-motion": "^11.5.4"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "eslint": "^8",
    "eslint-config-next": "14.2.35"
  }
}

```
