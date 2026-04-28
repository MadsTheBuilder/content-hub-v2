---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/dashboard/page.tsx"
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
import { 
  PlusCircle, 
  Library, 
  TrendingUp, 
  Zap, 
  Search,
  ChevronRight,
  LayoutGrid,
  List,
  Filter
} from "lucide-react";
import { workflows as workflowsApi } from "@/lib/api";
import type { Workflow } from "@/lib/types";

export default function DashboardPage() {
  const router = useRouter();
  const [workflowList, setWorkflowList] = useState<Workflow[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<"grid" | "list">("grid");

  const filtered = workflowList.filter((wf) =>
    wf.name.toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    workflowsApi.list().then((data) => {
      setWorkflowList(data.workflows);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [router]);

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-1200">
      {/* Header section with stats/search */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-[#1E293B]">
        <div>
          <h1 className="text-4xl font-black text-white tracking-tight">Overview</h1>
          <p className="text-gray-400 mt-2 flex items-center gap-2">
            Managing <span className="text-[#C9A96E] font-bold">{workflowList.length}</span> active content engines
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-[#C9A96E] transition-colors" />
            <input
              type="text"
              placeholder="Search workflows..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-[#1E293B]/50 border border-[#334155] rounded-xl pl-10 pr-4 py-2 text-sm text-gray-200 focus:outline-none focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 transition-all w-64"
            />
          </div>
          <div className="flex bg-[#1E293B] rounded-xl p-1 border border-[#334155]">
            <button 
              onClick={() => setView("grid")}
              className={`p-2 rounded-lg transition-all ${view === "grid" ? "bg-[#C9A96E] text-[#0F172A]" : "text-gray-500 hover:text-white"}`}
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button 
               onClick={() => setView("list")}
               className={`p-2 rounded-lg transition-all ${view === "list" ? "bg-[#C9A96E] text-[#0F172A]" : "text-gray-500 hover:text-white"}`}
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 grayscale opacity-40">
          <div className="w-12 h-12 rounded-full border-2 border-t-[#C9A96E] border-[#1E293B] animate-spin mb-4" />
          <p className="text-sm font-medium animate-pulse">Synchronising flows...</p>
        </div>
      ) : workflowList.length === 0 ? (
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative overflow-hidden group py-24 bg-[#0F172A] rounded-3xl border border-[#334155] border-dashed text-center"
        >
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-[#C9A96E]/5 to-transparent pointer-events-none" />
          <div className="relative z-10 space-y-4">
            <div className="w-16 h-16 bg-[#1E293B] rounded-2xl flex items-center justify-center mx-auto mb-6 transform group-hover:rotate-12 transition-transform duration-500">
               <Zap className="w-8 h-8 text-[#C9A96E]" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Engines Standby</h2>
            <p className="text-gray-500 max-w-sm mx-auto mb-8">
              No active content pipelines detected. Initialise your first workflow to begin autonomous research and generation.
            </p>
            <Link
              href="/workflows/new"
              className="inline-flex items-center gap-2 px-8 py-3 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-bold hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] transition-all active:scale-95"
            >
              <PlusCircle className="w-5 h-5" />
              Initialise First Engine
            </Link>
          </div>
        </motion.div>
      ) : (
        <div className={view === "grid" ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" : "space-y-4"}>
          <AnimatePresence mode="popLayout">
            {filtered.map((wf, idx) => (
              <motion.div
                key={wf.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05 }}
                className="group relative"
              >
                <div className="absolute -inset-0.5 bg-gradient-to-br from-[#C9A96E]/20 to-transparent rounded-3xl blur transition-opacity opacity-0 group-hover:opacity-100" />
                <Link
                  href={`/workflows/${wf.id}`}
                  className={`relative block h-full overflow-hidden p-6 rounded-2xl border border-[#1E293B] bg-gradient-to-br from-[#1E293B] to-[#0F172A] hover:border-[#C9A96E]/50 transition-all duration-300 group`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 rounded-full bg-green-500/20 flex items-center justify-center">
                        <div className={`w-2 h-2 rounded-full ${wf.is_active ? "bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.5)]" : "bg-gray-500"}`} />
                      </div>
                      <span className="text-[10px] uppercase font-black tracking-widest text-gray-500">
                        {wf.template_type}
                      </span>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-white group-hover:translate-x-1 transition-all" />
                  </div>

                  <h3 className="text-xl font-bold text-white mb-4 group-hover:text-[#C9A96E] transition-colors leading-tight">
                    {wf.name}
                  </h3>

                  <div className="flex flex-wrap gap-2 mb-6">
                    {wf.platforms.map((p) => (
                      <span key={p} className="text-[10px] font-bold uppercase py-1 px-2 rounded-lg bg-[#0F172A] border border-[#1E293B] text-gray-400 group-hover:border-[#C9A96E]/20 transition-colors">
                        {p}
                      </span>
                    ))}
                  </div>

                  <div className="pt-4 border-t border-[#1E293B] flex items-center justify-between">
                    <div className="flex -space-x-2">
                       {wf.content_pillars.slice(0, 3).map((pillar, i) => (
                         <div 
                           key={pillar} 
                           className="w-6 h-6 rounded-full border-2 border-[#1E293B] bg-[#0F172A] flex items-center justify-center overflow-hidden"
                           title={pillar}
                         >
                           <span className="text-[8px] font-bold text-[#C9A96E]">{pillar[0]}</span>
                         </div>
                       ))}
                       {wf.content_pillars.length > 3 && (
                         <div className="w-6 h-6 rounded-full border-2 border-[#1E293B] bg-[#1E293B] flex items-center justify-center text-[8px] font-bold text-gray-400">
                           +{wf.content_pillars.length - 3}
                         </div>
                       )}
                    </div>
                    <div className="flex items-center gap-1.5 text-[#C9A96E] text-[10px] font-black uppercase tracking-tighter">
                      <TrendingUp className="w-3 h-3" />
                      Research Ready
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}

```
