---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/content/library/page.tsx"
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
import { Library, PlusCircle, ChevronRight } from "lucide-react";
import { content as contentApi, workflows as workflowsApi } from "@/lib/api";
import type { ContentItem, Workflow } from "@/lib/types";

const STATUS_COLORS: Record<string, string> = {
  generating: "bg-blue-400/20 text-blue-400",
  scripting: "bg-purple-400/20 text-purple-400",
  rendering: "bg-yellow-400/20 text-yellow-400",
  ready: "bg-green-400/20 text-green-400",
  failed: "bg-red-400/20 text-red-400",
  posted: "bg-[#C9A96E]/20 text-[#C9A96E]",
};

export default function LibraryPage() {
  const router = useRouter();
  const [items, setItems] = useState<ContentItem[]>([]);
  const [workflowList, setWorkflowList] = useState<Workflow[]>([]);
  const [filterWorkflow, setFilterWorkflow] = useState("");
  const [filterType, setFilterType] = useState("");
  const [filterPlatform, setFilterPlatform] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    workflowsApi.list().then((d) => setWorkflowList(d.workflows));
    loadContent();
  }, [router]);

  async function loadContent() {
    setLoading(true);
    const params: Record<string, string> = {};
    if (filterWorkflow) params.workflow_id = filterWorkflow;
    if (filterType) params.content_type = filterType;
    if (filterPlatform) params.platform = filterPlatform;
    const data = await contentApi.library(params);
    setItems(data.items);
    setLoading(false);
  }

  useEffect(() => { loadContent(); }, [filterWorkflow, filterType, filterPlatform]);

  return (
    <div
      className="min-h-screen"
      style={{ background: "#0F172A" }}
    >
      <div className="max-w-6xl mx-auto p-8 space-y-8">

        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-[#1E293B]">
          <div>
            <Link href="/dashboard" className="text-gray-500 text-sm hover:text-[#C9A96E] transition-colors">
              &larr; Dashboard
            </Link>
            <h1 className="text-4xl font-black text-white tracking-tight mt-2">
              Content Library
            </h1>
            <p className="text-gray-400 mt-1">
              {loading ? (
                <span className="animate-pulse">Loading items...</span>
              ) : (
                <>
                  <span className="text-[#C9A96E] font-bold">{items.length}</span> pieces generated
                </>
              )}
            </p>
          </div>

          <Link
            href="/content/new"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-bold hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] transition-all active:scale-95 self-start md:self-auto"
          >
            <PlusCircle className="w-4 h-4" />
            Generate
          </Link>
        </div>

        {/* Filter Bar */}
        <div className="flex flex-wrap gap-3">
          <select
            value={filterWorkflow}
            onChange={(e) => setFilterWorkflow(e.target.value)}
            className="px-4 py-2.5 rounded-xl bg-[#1E293B]/40 border border-[#334155] text-gray-300 text-sm focus:outline-none focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 transition-all"
          >
            <option value="">All Workflows</option>
            {workflowList.map((w) => (
              <option key={w.id} value={w.id}>{w.name}</option>
            ))}
          </select>

          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2.5 rounded-xl bg-[#1E293B]/40 border border-[#334155] text-gray-300 text-sm focus:outline-none focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 transition-all"
          >
            <option value="">All Types</option>
            <option value="slides">Slides</option>
            <option value="topic">Topic Content</option>
            <option value="short_form">Short-form Video</option>
            <option value="talking_head">Talking Head</option>
          </select>

          <select
            value={filterPlatform}
            onChange={(e) => setFilterPlatform(e.target.value)}
            className="px-4 py-2.5 rounded-xl bg-[#1E293B]/40 border border-[#334155] text-gray-300 text-sm focus:outline-none focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 transition-all"
          >
            <option value="">All Platforms</option>
            <option value="tiktok">TikTok</option>
            <option value="instagram">Instagram</option>
            <option value="youtube">YouTube</option>
            <option value="linkedin">LinkedIn</option>
            <option value="twitter">Twitter</option>
          </select>
        </div>

        {/* Content */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 grayscale opacity-40">
            <div className="w-12 h-12 rounded-full border-2 border-t-[#C9A96E] border-[#1E293B] animate-spin mb-4" />
            <p className="text-sm font-medium text-gray-400 animate-pulse">Loading library...</p>
          </div>
        ) : items.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative overflow-hidden group py-24 bg-[#0F172A] rounded-3xl border border-[#334155] border-dashed text-center"
          >
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-[#C9A96E]/5 to-transparent pointer-events-none" />
            <div className="relative z-10 space-y-4">
              <div className="w-16 h-16 bg-[#1E293B] rounded-2xl flex items-center justify-center mx-auto mb-6 transform group-hover:rotate-12 transition-transform duration-500">
                <Library className="w-8 h-8 text-[#C9A96E]" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">No content generated yet</h2>
              <p className="text-gray-500 max-w-sm mx-auto mb-8">
                Your library is empty. Generate your first piece of content to get started.
              </p>
              <Link
                href="/content/new"
                className="inline-flex items-center gap-2 px-8 py-3 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-bold hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] transition-all active:scale-95"
              >
                <PlusCircle className="w-5 h-5" />
                Generate First Piece
              </Link>
            </div>
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <AnimatePresence mode="popLayout">
              {items.map((item, idx) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className="group relative"
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-br from-[#C9A96E]/20 to-transparent rounded-2xl blur transition-opacity opacity-0 group-hover:opacity-100" />
                  <Link
                    href={`/content/${item.id}`}
                    className="relative block h-full overflow-hidden p-5 rounded-xl bg-[#1E293B]/40 border border-[#334155] hover:border-[#C9A96E]/50 transition-all duration-300"
                  >
                    {/* Top row: status + platform */}
                    <div className="flex items-center justify-between mb-3">
                      <span
                        className={`text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-full ${STATUS_COLORS[item.status] ?? "bg-gray-500/20 text-gray-400"}`}
                      >
                        {item.status}
                      </span>
                      <span className="text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-full bg-[#0F172A] border border-[#1E293B] text-gray-400 capitalize group-hover:border-[#C9A96E]/20 transition-colors">
                        {item.platform}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="text-white text-sm font-semibold mb-3 line-clamp-2 group-hover:text-[#C9A96E] transition-colors leading-snug">
                      {item.title}
                    </h3>

                    {/* Bottom row: content_type + date + chevron */}
                    <div className="flex items-center justify-between pt-3 border-t border-[#334155]/50">
                      <span className="text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-full bg-[#0F172A] border border-[#1E293B] text-gray-500 capitalize">
                        {item.content_type.replace("_", " ")}
                      </span>
                      <div className="flex items-center gap-1.5 text-gray-500 text-xs">
                        <span>{new Date(item.created_at).toLocaleDateString()}</span>
                        <ChevronRight className="w-3.5 h-3.5 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
                      </div>
                    </div>
                  </Link>
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
