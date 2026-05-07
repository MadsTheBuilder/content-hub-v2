---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/globals.css"
category: "Content Hub Source Code"
---

# globals.css

**Description:** Next.js frontend page component defining routing and page layout.

---

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: Arial, Helvetica, sans-serif;
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}

```
