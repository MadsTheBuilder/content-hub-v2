---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/tailwind.config.ts"
category: "Content Hub Source Code"
---

# tailwind.config.ts

**Description:** TypeScript module or React implementation logic.

---

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
};
export default config;

```
