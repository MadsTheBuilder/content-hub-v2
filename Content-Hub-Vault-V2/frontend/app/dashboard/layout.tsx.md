---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/dashboard/layout.tsx"
category: "Content Hub Source Code"
---

# layout.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
import { Sidebar } from "@/components/Sidebar";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex bg-[#0F172A] min-h-screen">
      <Sidebar />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}

```
