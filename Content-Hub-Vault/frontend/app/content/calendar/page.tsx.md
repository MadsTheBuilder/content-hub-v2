---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/content/calendar/page.tsx"
category: "Content Hub Source Code"
---

# page.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { CalendarDays, PlusCircle, ChevronRight } from "lucide-react";
import { content as contentApi } from "@/lib/api";
import type { ContentItem } from "@/lib/types";

const STATUS_COLORS: Record<string, string> = {
  generating: "bg-blue-400/20 text-blue-400",
  scripting: "bg-purple-400/20 text-purple-400",
  rendering: "bg-yellow-400/20 text-yellow-400",
  ready: "bg-green-400/20 text-green-400",
  failed: "bg-red-400/20 text-red-400",
  posted: "bg-[#C9A96E]/20 text-[#C9A96E]",
};

export default function CalendarPage() {
  const router = useRouter();
  const [items, setItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    contentApi.calendar().then((d) => {
      setItems(d.items);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [router]);

  const grouped = items.reduce((acc: Record<string, ContentItem[]>, item) => {
    const date = new Date(item.created_at).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    if (!acc[date]) acc[date] = [];
    acc[date].push(item);
    return acc;
  }, {});

  return (
    <div
      className="min-h-screen"
      style={{ background: "#0F172A" }}
    >
      <div className="max-w-4xl mx-auto p-8 space-y-8">

        {/* Header */}
        <div className="pb-6 border-b border-[#1E293B]">
          <Link href="/dashboard" className="text-gray-500 text-sm hover:text-[#C9A96E] transition-colors">
            &larr; Dashboard
          </Link>
          <h1 className="text-4xl font-black text-white tracking-tight mt-2">
            Content Calendar
          </h1>
          <p className="text-gray-400 mt-1">
            {loading ? (
              <span className="animate-pulse">Loading schedule...</span>
            ) : (
              <>
                <span className="text-[#C9A96E] font-bold">{Object.keys(grouped).length}</span> active day{Object.keys(grouped).length !== 1 ? "s" : ""}
              </>
            )}
          </p>
        </div>

        {/* Content */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 grayscale opacity-40">
            <div className="w-12 h-12 rounded-full border-2 border-t-[#C9A96E] border-[#1E293B] animate-spin mb-4" />
            <p className="text-sm font-medium text-gray-400 animate-pulse">Loading calendar...</p>
          </div>
        ) : Object.entries(grouped).length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative overflow-hidden group py-24 bg-[#0F172A] rounded-3xl border border-[#334155] border-dashed text-center"
          >
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-[#C9A96E]/5 to-transparent pointer-events-none" />
            <div className="relative z-10 space-y-4">
              <div className="w-16 h-16 bg-[#1E293B] rounded-2xl flex items-center justify-center mx-auto mb-6 transform group-hover:rotate-12 transition-transform duration-500">
                <CalendarDays className="w-8 h-8 text-[#C9A96E]" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">No scheduled content yet</h2>
              <p className="text-gray-500 max-w-sm mx-auto mb-8">
                Your calendar is empty. Generate content and schedule it to see it here.
              </p>
              <Link
                href="/content/new"
                className="inline-flex items-center gap-2 px-8 py-3 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-bold hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] transition-all active:scale-95"
              >
                <PlusCircle className="w-5 h-5" />
                Generate Content
              </Link>
            </div>
          </motion.div>
        ) : (
          <div className="space-y-8">
            <AnimatePresence mode="popLayout">
              {Object.entries(grouped).map(([date, dateItems], groupIdx) => (
                <motion.div
                  key={date}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: groupIdx * 0.05 }}
                >
                  {/* Date group header with gold left border */}
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-1 h-6 rounded-full bg-[#C9A96E]" />
                    <h2 className="text-sm font-black uppercase tracking-widest text-[#C9A96E]">
                      {date}
                    </h2>
                    <span className="text-[10px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full bg-[#C9A96E]/10 text-[#C9A96E] border border-[#C9A96E]/20">
                      {dateItems.length} item{dateItems.length !== 1 ? "s" : ""}
                    </span>
                  </div>

                  {/* Cards for this date */}
                  <div className="space-y-2 pl-4 border-l border-[#1E293B]">
                    {dateItems.map((item, idx) => (
                      <motion.div
                        key={item.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: groupIdx * 0.05 + idx * 0.04 }}
                        className="group relative"
                      >
                        <div className="absolute -inset-0.5 bg-gradient-to-br from-[#C9A96E]/20 to-transparent rounded-xl blur transition-opacity opacity-0 group-hover:opacity-100" />
                        <Link
                          href={`/content/${item.id}`}
                          className="relative flex items-center justify-between p-4 rounded-xl bg-[#1E293B]/40 border border-[#334155] hover:border-[#C9A96E]/50 transition-all duration-300"
                        >
                          {/* Left: title */}
                          <div className="flex-1 min-w-0 mr-4">
                            <span className="text-white text-sm font-semibold group-hover:text-[#C9A96E] transition-colors line-clamp-1">
                              {item.title}
                            </span>
                          </div>

                          {/* Right: badges + chevron */}
                          <div className="flex items-center gap-2 flex-shrink-0">
                            <span className="text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-full bg-[#0F172A] border border-[#1E293B] text-gray-400 capitalize hidden sm:inline-block">
                              {item.platform}
                            </span>
                            <span className="text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-full bg-[#0F172A] border border-[#1E293B] text-gray-400 capitalize hidden md:inline-block">
                              {item.content_type.replace("_", " ")}
                            </span>
                            <span
                              className={`text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-full ${STATUS_COLORS[item.status] ?? "bg-gray-500/20 text-gray-400"}`}
                            >
                              {item.status}
                            </span>
                            <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
                          </div>
                        </Link>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}

```
