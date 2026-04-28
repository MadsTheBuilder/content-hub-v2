---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/layout.tsx"
category: "Content Hub Source Code"
---

# layout.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Content Hub",
  description: "Personal brand content operating system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} antialiased bg-[#0F172A] text-white min-h-screen`}
      >
        <Sidebar />
        {/* Main content pushed right to clear sidebar */}
        <main className="ml-64 min-h-screen p-8">
          {children}
        </main>
      </body>
    </html>
  );
}

```
