---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/workflows/[id]/page.tsx"
category: "Content Hub Source Code"
---

# page.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronLeft,
  Plus,
  Settings,
  TrendingUp,
  Lightbulb,
  ExternalLink,
  Eye,
  Heart,
  MessageCircle,
  Share2,
  Target,
  Zap,
  Users,
  CheckSquare,
  Square,
  ChevronDown,
  ChevronUp,
  Sparkles,
  RefreshCw,
} from "lucide-react";
import { workflows as workflowsApi } from "@/lib/api";
import type { Workflow, TrendingContent, Suggestion } from "@/lib/types";

function fmtNum(n: number): string {
  if (!n) return "0";
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K`;
  return String(n);
}

function RelevanceBadge({ score }: { score: number }) {
  const pct = Math.min(Math.round(score), 100);
  const color = pct >= 70 ? "#C9A96E" : pct >= 40 ? "#94a3b8" : "#475569";
  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative w-10 h-10">
        <svg className="w-10 h-10 -rotate-90" viewBox="0 0 36 36">
          <circle cx="18" cy="18" r="15" fill="none" stroke="#1E293B" strokeWidth="3" />
          <circle
            cx="18" cy="18" r="15" fill="none"
            stroke={color} strokeWidth="3"
            strokeDasharray={`${(pct / 100) * 94.2} 94.2`}
            strokeLinecap="round"
          />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center text-[9px] font-black" style={{ color }}>
          {pct}
        </span>
      </div>
      <span className="text-[8px] font-black uppercase tracking-wider text-gray-600">match</span>
    </div>
  );
}

function TrendingCard({
  post,
  selected,
  onToggle,
}: {
  post: TrendingContent;
  selected: boolean;
  onToggle: (id: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const analysis = post.content_analysis as Record<string, unknown> | null;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`rounded-2xl border transition-all duration-300 overflow-hidden ${
        selected
          ? "border-[#C9A96E] bg-[#C9A96E]/5 shadow-[0_0_20px_rgba(201,169,110,0.08)]"
          : "border-[#334155] bg-[#1E293B]/30 hover:border-[#C9A96E]/30"
      }`}
    >
      {/* Card header */}
      <div className="p-4 flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={() => onToggle(post.id)}
          className="flex-shrink-0 mt-0.5 text-[#C9A96E] hover:scale-110 transition-transform"
          aria-label={selected ? "Deselect" : "Select"}
        >
          {selected ? (
            <CheckSquare className="w-5 h-5" />
          ) : (
            <Square className="w-5 h-5 text-gray-600 hover:text-[#C9A96E]" />
          )}
        </button>

        {/* Main content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-[9px] font-black uppercase tracking-wider text-[#C9A96E] bg-[#C9A96E]/10 px-2 py-0.5 rounded">
              {post.platform}
            </span>
            <span className="text-xs text-gray-500">@{post.author_username}</span>
          </div>
          <p className="text-white font-bold text-sm leading-snug line-clamp-2">{post.title}</p>

          {/* Metrics row */}
          <div className="flex items-center gap-4 mt-3 text-gray-600">
            <span className="flex items-center gap-1 text-xs">
              <Eye className="w-3 h-3" />
              {fmtNum(post.view_count)}
            </span>
            <span className="flex items-center gap-1 text-xs">
              <Heart className="w-3 h-3" />
              {fmtNum(post.like_count)}
            </span>
            <span className="flex items-center gap-1 text-xs">
              <MessageCircle className="w-3 h-3" />
              {fmtNum(post.comment_count)}
            </span>
            {post.share_count > 0 && (
              <span className="flex items-center gap-1 text-xs">
                <Share2 className="w-3 h-3" />
                {fmtNum(post.share_count)}
              </span>
            )}
          </div>

          {/* Analysis tags */}
          {analysis && (
            <div className="flex flex-wrap gap-1.5 mt-3">
              {(analysis.hook_type as string) && (
                <span className="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-lg bg-[#0F172A] border border-[#334155] text-[#C9A96E]">
                  {analysis.hook_type as string}
                </span>
              )}
              {(analysis.content_style as string) && (
                <span className="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-lg bg-[#0F172A] border border-[#334155] text-gray-400">
                  {analysis.content_style as string}
                </span>
              )}
              {(analysis.pacing as string) && (
                <span className="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-lg bg-[#0F172A] border border-[#334155] text-gray-400">
                  {analysis.pacing as string} pace
                </span>
              )}
            </div>
          )}
        </div>

        {/* Right side: relevance + external link */}
        <div className="flex flex-col items-center gap-3 flex-shrink-0">
          <RelevanceBadge score={post.relevance_score ?? post.organic_score ?? 0} />
          <a
            href={post.post_url}
            target="_blank"
            rel="noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="p-2 rounded-xl bg-[#0F172A] border border-[#334155] text-gray-600 hover:text-white hover:border-[#C9A96E]/50 transition-all"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* Expandable: why it works */}
      {analysis && (analysis.why_it_works as string) && (
        <>
          <button
            onClick={() => setExpanded(!expanded)}
            className="w-full flex items-center justify-between px-4 py-2.5 border-t border-[#1E293B] text-[10px] font-black uppercase tracking-wider text-gray-600 hover:text-[#C9A96E] transition-colors"
          >
            <span>Why it works</span>
            {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
          <AnimatePresence>
            {expanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="px-4 pb-4 space-y-3">
                  <p className="text-gray-400 text-xs leading-relaxed">{analysis.why_it_works as string}</p>
                  {Array.isArray(analysis.applicable_techniques) && (analysis.applicable_techniques as string[]).length > 0 && (
                    <div>
                      <p className="text-[9px] font-black uppercase tracking-wider text-gray-600 mb-2">Techniques to borrow</p>
                      <ul className="space-y-1">
                        {(analysis.applicable_techniques as string[]).map((t, i) => (
                          <li key={i} className="text-xs text-gray-500 flex items-start gap-2">
                            <span className="text-[#C9A96E] mt-0.5">→</span>
                            {t}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {Array.isArray(analysis.engagement_drivers) && (analysis.engagement_drivers as string[]).length > 0 && (
                    <div>
                      <p className="text-[9px] font-black uppercase tracking-wider text-gray-600 mb-2">Engagement drivers</p>
                      <ul className="space-y-1">
                        {(analysis.engagement_drivers as string[]).map((d, i) => (
                          <li key={i} className="text-xs text-gray-500 flex items-start gap-2">
                            <span className="text-[#C9A96E] mt-0.5">·</span>
                            {d}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </>
      )}
    </motion.div>
  );
}

export default function WorkflowDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const wfId = id as string;

  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [trending, setTrending] = useState<TrendingContent[]>([]);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [tab, setTab] = useState<"trending" | "suggestions">("trending");
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [scraping, setScraping] = useState(false);

  const load = useCallback(() => {
    workflowsApi.get(wfId).then((d) => setWorkflow(d.workflow));
    workflowsApi.trending(wfId).then((d) => setTrending(d.trending));
    workflowsApi.suggestions(wfId).then((d) => setSuggestions(d.suggestions)).catch(() => {});
  }, [wfId]);

  useEffect(() => { load(); }, [load]);

  function toggleSelect(postId: string) {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(postId)) next.delete(postId);
      else next.add(postId);
      return next;
    });
  }

  function toggleAll() {
    if (selectedIds.size === trending.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(trending.map((t) => t.id)));
    }
  }

  async function handleScrape() {
    setScraping(true);
    try {
      await workflowsApi.scrape(wfId);
      setTimeout(() => { load(); setScraping(false); }, 3000);
    } catch {
      setScraping(false);
    }
  }

  function handleSynthesize() {
    if (selectedIds.size === 0) return;
    const platform = workflow?.platforms[0] || "tiktok";
    const postIds = Array.from(selectedIds).join(",");
    // Record selections for learning (fire and forget)
    workflowsApi.recordSelections(wfId, Array.from(selectedIds)).catch((err) => {
      console.error("[Intelligence Engine] Failed to record selection signals", err);
    });
    router.push(`/content/synthesize?workflow_id=${wfId}&platform=${platform}&post_ids=${encodeURIComponent(postIds)}`);
  }

  if (!workflow) return (
    <div className="flex flex-col items-center justify-center py-40 grayscale opacity-40">
      <div className="w-12 h-12 rounded-full border-2 border-t-[#C9A96E] border-[#1E293B] animate-spin mb-4" />
      <p className="text-sm font-medium animate-pulse tracking-widest uppercase">Initialising Engine...</p>
    </div>
  );

  const allSelected = trending.length > 0 && selectedIds.size === trending.length;

  return (
    <div className="space-y-10 py-6 animate-in fade-in slide-in-from-bottom-4 duration-1000 pb-32">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-8 border-b border-[#1E293B]">
        <div>
          <Link href="/dashboard" className="inline-flex items-center gap-2 text-gray-500 text-xs font-bold uppercase tracking-widest hover:text-[#C9A96E] transition-colors mb-4">
            <ChevronLeft className="w-4 h-4" />
            Back to Dashboard
          </Link>
          <div className="flex items-center gap-4">
            <h1 className="text-4xl font-black text-white tracking-tight">{workflow.name}</h1>
            <span className="text-[10px] px-2 py-1 rounded-lg bg-[#C9A96E]/10 border border-[#C9A96E]/30 text-[#C9A96E] font-black uppercase tracking-widest">
              {workflow.template_type.replace("_", " ")}
            </span>
          </div>
        </div>
        <div className="flex gap-3">
          <Link
            href={`/brand/${workflow.id}`}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl border border-[#334155] text-gray-300 font-bold hover:bg-[#1E293B] hover:border-gray-500 transition-all text-sm"
          >
            <Settings className="w-4 h-4" />
            Brand Protocol
          </Link>
          <Link
            href={`/content/new?workflow=${workflow.id}`}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black hover:shadow-[0_0_20px_rgba(201,169,110,0.3)] transition-all active:scale-95 text-sm"
          >
            <Plus className="w-5 h-5" />
            Generate Content
          </Link>
        </div>
      </div>

      {/* Workflow Strategy Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155] relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <Users className="w-12 h-12 text-white" />
          </div>
          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] mb-3">Platform Matrix</p>
          <div className="flex gap-2 flex-wrap">
            {workflow.platforms.map((p) => (
              <span key={p} className="text-xs font-bold text-white capitalize bg-[#0F172A] px-3 py-1 rounded-lg border border-[#334155]">{p}</span>
            ))}
          </div>
        </div>
        <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155] relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <Target className="w-12 h-12 text-white" />
          </div>
          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] mb-3">Research Anchors</p>
          <div className="flex gap-2 flex-wrap">
            {workflow.content_pillars.map((p) => (
              <span key={p} className="text-[10px] font-medium text-gray-300 px-2 py-1 rounded bg-[#0F172A]/50 border border-[#334155]">{p}</span>
            ))}
          </div>
        </div>
        <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155] relative overflow-hidden group border-l-4 border-l-[#C9A96E]">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <Zap className="w-12 h-12 text-white" />
          </div>
          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] mb-3">Persona Signature</p>
          <p className="text-sm font-medium text-gray-300 italic line-clamp-2">&ldquo;{workflow.brand_voice || "Autonomous authority"}&rdquo;</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="space-y-6">
        <div className="flex gap-8 border-b border-[#1E293B]">
          <button
            onClick={() => setTab("trending")}
            className={`flex items-center gap-2 pb-4 text-xs font-black uppercase tracking-widest border-b-2 transition-all ${
              tab === "trending" ? "border-[#C9A96E] text-[#C9A96E]" : "border-transparent text-gray-500 hover:text-white"
            }`}
          >
            <TrendingUp className="w-4 h-4" />
            Trending Intelligence ({trending.length})
          </button>
          <button
            onClick={() => setTab("suggestions")}
            className={`flex items-center gap-2 pb-4 text-xs font-black uppercase tracking-widest border-b-2 transition-all ${
              tab === "suggestions" ? "border-[#C9A96E] text-[#C9A96E]" : "border-transparent text-gray-500 hover:text-white"
            }`}
          >
            <Lightbulb className="w-4 h-4" />
            Content Suggestions ({suggestions.length})
          </button>
        </div>

        <div className="min-h-[400px]">
          <AnimatePresence mode="wait">
            {tab === "trending" && (
              <motion.div
                key="trending"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                {trending.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-20 text-center space-y-6">
                    <TrendingUp className="w-12 h-12 text-gray-800" />
                    <p className="text-gray-500 text-sm font-medium max-w-xs">No intelligence data detected. Run a scrape to populate trending posts.</p>
                    <button
                      onClick={handleScrape}
                      disabled={scraping}
                      className="flex items-center gap-2 px-6 py-3 rounded-xl bg-[#1E293B] border border-[#334155] text-gray-300 font-bold text-sm hover:border-[#C9A96E]/40 hover:text-white disabled:opacity-50 transition-all"
                    >
                      <RefreshCw className={`w-4 h-4 ${scraping ? "animate-spin" : ""}`} />
                      {scraping ? "Scraping..." : "Run Scrape"}
                    </button>
                  </div>
                ) : (
                  <>
                    {/* Toolbar */}
                    <div className="flex items-center justify-between mb-4">
                      <button
                        onClick={toggleAll}
                        className="flex items-center gap-2 text-xs font-bold text-gray-500 hover:text-[#C9A96E] transition-colors"
                      >
                        {allSelected ? <CheckSquare className="w-4 h-4 text-[#C9A96E]" /> : <Square className="w-4 h-4" />}
                        {allSelected ? "Deselect All" : "Select All"}
                      </button>
                      <button
                        onClick={handleScrape}
                        disabled={scraping}
                        className="flex items-center gap-2 px-4 py-2 rounded-xl bg-[#1E293B]/60 border border-[#334155] text-gray-500 font-bold text-xs hover:border-[#C9A96E]/30 hover:text-white disabled:opacity-50 transition-all"
                      >
                        <RefreshCw className={`w-3.5 h-3.5 ${scraping ? "animate-spin" : ""}`} />
                        {scraping ? "Scraping..." : "Re-scrape"}
                      </button>
                    </div>

                    {/* Card grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                      {trending.map((post) => (
                        <TrendingCard
                          key={post.id}
                          post={post}
                          selected={selectedIds.has(post.id)}
                          onToggle={toggleSelect}
                        />
                      ))}
                    </div>
                  </>
                )}
              </motion.div>
            )}

            {tab === "suggestions" && (
              <motion.div
                key="suggestions"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="space-y-4"
              >
                {suggestions.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-20 text-center space-y-4">
                    <Lightbulb className="w-12 h-12 text-gray-800" />
                    <p className="text-gray-500 text-sm font-medium max-w-xs">Waiting for trending signals to synthesise new content suggestions.</p>
                  </div>
                ) : (
                  suggestions.map((s, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="p-6 rounded-2xl bg-[#1E293B]/30 border border-[#334155] border-l-4 border-l-[#C9A96E]"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <div className="flex items-center gap-3 mb-2">
                            <span className="text-[10px] px-2 py-0.5 rounded bg-[#C9A96E] text-[#0F172A] font-black uppercase tracking-widest">{s.recommended_type}</span>
                            <span className="text-[10px] font-black uppercase tracking-widest text-gray-500">{s.platform}</span>
                          </div>
                          <h4 className="text-xl font-bold text-white tracking-tight">{s.topic}</h4>
                        </div>
                        <div className="text-right">
                          <p className="text-xs font-black uppercase tracking-widest text-gray-600 mb-1">Potential</p>
                          <p className="text-[#C9A96E] font-black text-2xl leading-none">{s.organic_score.toFixed(0)}</p>
                        </div>
                      </div>
                      {s.warning && (
                        <div className="flex items-center gap-2 p-3 rounded-xl bg-orange-500/5 border border-orange-500/20 text-orange-400 text-xs font-medium mt-2">
                          <Zap className="w-3 h-3" />
                          {s.warning}
                        </div>
                      )}
                      <div className="mt-6 flex justify-end">
                        <Link
                          href={`/content/new?workflow=${workflow.id}&topic=${encodeURIComponent(s.topic)}&type=${s.recommended_type}`}
                          className="text-xs font-black uppercase tracking-[0.2em] text-[#C9A96E] hover:text-white transition-colors"
                        >
                          Draft Script &rarr;
                        </Link>
                      </div>
                    </motion.div>
                  ))
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Sticky bottom bar — appears when posts selected */}
      <AnimatePresence>
        {selectedIds.size > 0 && (
          <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            transition={{ type: "spring", stiffness: 400, damping: 30 }}
            className="fixed bottom-0 left-0 right-0 z-50 flex justify-center px-6 pb-6 pointer-events-none"
          >
            <div className="pointer-events-auto bg-[#0F172A]/95 backdrop-blur-xl border border-[#C9A96E]/30 rounded-2xl px-6 py-4 shadow-[0_0_40px_rgba(201,169,110,0.2)] flex items-center gap-6 max-w-lg w-full">
              <div className="flex-1">
                <p className="text-white font-black text-lg leading-none">{selectedIds.size} selected</p>
                <p className="text-gray-500 text-xs mt-0.5">Ready to synthesise strategy</p>
              </div>
              <button
                onClick={() => setSelectedIds(new Set())}
                className="text-xs font-bold text-gray-500 hover:text-white transition-colors px-3 py-2 rounded-xl hover:bg-[#1E293B]"
              >
                Clear
              </button>
              <button
                onClick={handleSynthesize}
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black text-sm hover:shadow-[0_0_20px_rgba(201,169,110,0.4)] active:scale-95 transition-all"
              >
                <Sparkles className="w-4 h-4" />
                Synthesise Strategy
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

```
