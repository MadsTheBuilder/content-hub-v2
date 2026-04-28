---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/components/Sidebar.tsx"
category: "Content Hub Source Code"
---

# Sidebar.tsx

**Description:** React UI component for the frontend dashboard and user workflows.

---

```typescript
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  Library,
  CalendarDays,
  PlusCircle,
  Cpu,
  Zap,
  ChevronRight,
  AlertTriangle,
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  {
    href: "/content/new",
    label: "Generate Content",
    icon: PlusCircle,
    accent: true,
  },
  { href: "/content/library", label: "Content Library", icon: Library },
  { href: "/content/calendar", label: "Calendar", icon: CalendarDays },
];

export function Sidebar() {
  const pathname = usePathname();
  const [mockMode, setMockMode] = useState(false);

  useEffect(() => {
    fetch("/api/v1/status")
      .then((r) => r.json())
      .then((d) => setMockMode(d.mock_mode ?? false))
      .catch(() => {});
  }, []);

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-[#080F1A] border-r border-[#1E293B] flex flex-col z-40">
      {/* Brand */}
      <div className="px-6 py-6 border-b border-[#1E293B]">
        <Link href="/dashboard" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#C9A96E] to-[#8E744A] flex items-center justify-center shadow-[0_0_20px_rgba(201,169,110,0.3)]">
            <Cpu className="w-5 h-5 text-[#0F172A]" />
          </div>
          <div>
            <span className="text-white font-black text-base tracking-tight">
              Content Hub
            </span>
            <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-[#C9A96E]/60">
              Intelligence Engine
            </p>
          </div>
        </Link>
      </div>

      {/* Mock mode warning */}
      {mockMode && (
        <div className="mx-3 mt-3 p-3 rounded-xl bg-amber-500/5 border border-amber-500/20 flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <p className="text-[10px] font-black uppercase tracking-widest text-amber-400">
              Mock Mode
            </p>
            <p className="text-[10px] text-amber-400/60 mt-0.5 leading-relaxed">
              No Supabase connected. Data won&apos;t persist.
            </p>
          </div>
        </div>
      )}

      {/* Nav links */}
      <nav className="flex-1 px-3 py-5 space-y-1 overflow-y-auto">
        <p className="text-[9px] font-black uppercase tracking-[0.2em] text-gray-600 px-3 mb-3">
          Navigation
        </p>

        {NAV_ITEMS.map(({ href, label, icon: Icon, accent }) => {
          const isActive =
            pathname === href ||
            (href !== "/dashboard" &&
              href !== "/content/new" &&
              pathname?.startsWith(href));
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center justify-between gap-3 px-3 py-2.5 rounded-xl text-sm font-bold transition-all group ${
                accent
                  ? "bg-gradient-to-r from-[#C9A96E]/10 to-transparent border border-[#C9A96E]/20 text-[#C9A96E] hover:from-[#C9A96E]/20 hover:border-[#C9A96E]/40"
                  : isActive
                  ? "bg-[#1E293B] text-white border border-[#334155]"
                  : "text-gray-500 hover:text-white hover:bg-[#1E293B]/50"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon
                  className={`w-4 h-4 ${
                    accent
                      ? "text-[#C9A96E]"
                      : isActive
                      ? "text-[#C9A96E]"
                      : "text-gray-600 group-hover:text-gray-400"
                  }`}
                />
                {label}
              </div>
              {isActive && !accent && (
                <ChevronRight className="w-3 h-3 text-[#C9A96E]" />
              )}
            </Link>
          );
        })}

        <div className="pt-4">
          <p className="text-[9px] font-black uppercase tracking-[0.2em] text-gray-600 px-3 mb-3">
            Workflows
          </p>
          <Link
            href="/workflows/new"
            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-bold transition-all group ${
              pathname === "/workflows/new"
                ? "bg-[#1E293B] text-white border border-[#334155]"
                : "text-gray-500 hover:text-white hover:bg-[#1E293B]/50"
            }`}
          >
            <Zap
              className={`w-4 h-4 ${
                pathname === "/workflows/new"
                  ? "text-[#C9A96E]"
                  : "text-gray-600 group-hover:text-gray-400"
              }`}
            />
            New Workflow
          </Link>
        </div>
      </nav>

      {/* Footer */}
      <div className="px-5 py-4 border-t border-[#1E293B]">
        <div className="flex items-center gap-3 px-2 py-2.5 rounded-xl bg-[#1E293B]/50 border border-[#334155]">
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#C9A96E]/30 to-[#C9A96E]/10 border border-[#C9A96E]/30 flex items-center justify-center text-[10px] font-black text-[#C9A96E]">
            M
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-bold text-white truncate">Local User</p>
            <p className="text-[9px] font-bold uppercase tracking-widest text-gray-600 truncate">
              {mockMode ? "Mock Mode" : "Connected"}
            </p>
          </div>
        </div>
        <p className="text-[9px] font-bold text-gray-700 mt-3 px-2">
          v2.0 · MVP Build
        </p>
      </div>
    </aside>
  );
}

```
