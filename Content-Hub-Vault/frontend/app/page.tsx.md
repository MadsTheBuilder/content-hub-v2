---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/page.tsx"
category: "Content Hub Source Code"
---

# page.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/dashboard");
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-[#C9A96E] mb-2">Content Hub</h1>
        <p className="text-gray-400">Loading...</p>
      </div>
    </div>
  );
}

```
