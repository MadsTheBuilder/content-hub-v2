---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/content/synthesize/page.tsx"
category: "Content Hub Source Code"
---

# page.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
"use client";

import { useEffect, useState, useRef, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronLeft,
  Sparkles,
  Rocket,
  Check,
  ArrowRight,
  Edit3,
  Zap,
  Target,
  FileText,
} from "lucide-react";
import { content as contentApi } from "@/lib/api";
import type { StrategyDocument } from "@/lib/types";

const CONTENT_TYPES = [
  { value: "short_form", label: "Short-form Video" },
  { value: "slides", label: "Data Slides" },
  { value: "topic", label: "Topic Cards" },
  { value: "talking_head", label: "Talking Head" },
];

const GENERATION_STEPS = [
  { key: "generating", label: "Initialising Neural Pipeline" },
  { key: "scripting", label: "Synthesising Narrative with Gemini" },
  { key: "refining", label: "Applying Copy-Editing Sweeps" },
  { key: "rendering", label: "Processing Multimodal Assets" },
  { key: "ready", label: "Finalising Artefacts" },
];

function SynthesizePage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const workflowId = searchParams.get("workflow_id") || "";
  const platform = searchParams.get("platform") || "tiktok";
  const postIds = (searchParams.get("post_ids") || "").split(",").filter(Boolean);

  const [phase, setPhase] = useState<"loading" | "review" | "generating" | "done">("loading");
  const [strategy, setStrategy] = useState<StrategyDocument | null>(null);
  const [originalStrategy, setOriginalStrategy] = useState<StrategyDocument | null>(null);
  const [contentType, setContentType] = useState("short_form");
  const [userNotes, setUserNotes] = useState("");
  const [contentId, setContentId] = useState("");
  const [genStatus, setGenStatus] = useState("");

  useEffect(() => {
    if (!workflowId || postIds.length === 0) return;
    contentApi
      .synthesize({ workflow_id: workflowId, selected_post_ids: postIds, platform })
      .then((d) => {
        setStrategy(d.strategy as StrategyDocument);
        setOriginalStrategy(JSON.parse(JSON.stringify(d.strategy)));
        setPhase("review");
      })
      .catch(() => {
        alert("Failed to synthesize strategy. Please try again.");
        router.back();
      });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function updateStrategy(key: keyof StrategyDocument, value: unknown) {
    setStrategy((prev) => prev ? { ...prev, [key]: value } : prev);
  }

  function updateFormat(key: string, value: string) {
    setStrategy((prev) => {
      if (!prev) return prev;
      return { ...prev, recommended_format: { ...prev.recommended_format, [key]: value } };
    });
  }

  async function handleGenerate() {
    if (!strategy) return;
    setPhase("generating");
    setGenStatus("generating");
    try {
      const data = await contentApi.generateFromStrategy({
        workflow_id: workflowId,
        strategy: strategy as unknown as Record<string, unknown>,
        original_strategy: originalStrategy as unknown as Record<string, unknown>,
        user_notes: userNotes,
        content_type: contentType,
      });
      setContentId(data.content_id);
      pollStatus(data.content_id);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Generation failed");
      setPhase("review");
    }
  }

  function pollStatus(id: string) {
    const interval = setInterval(async () => {
      try {
        const data = await contentApi.status(id);
        setGenStatus(data.status);
        if (data.status === "ready") {
          clearInterval(interval);
          setPhase("done");
        } else if (data.status === "failed") {
          clearInterval(interval);
          alert("Generation failed: " + (data.error_message || "Unknown error"));
          setPhase("review");
        }
      } catch {
        clearInterval(interval);
        setPhase("review");
      }
    }, 2500);
  }

  // --- Loading ---
  if (phase === "loading") {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center gap-6">
        <div className="relative w-20 h-20">
          <div className="w-20 h-20 rounded-full border-4 border-[#1E293B] border-t-[#C9A96E] animate-spin" />
          <Sparkles className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-7 h-7 text-[#C9A96E] animate-pulse" />
        </div>
        <p className="text-[#C9A96E] font-black uppercase tracking-[0.2em] text-sm">Synthesising Strategy...</p>
        <p className="text-gray-600 text-xs">Analysing {postIds.length} trending post{postIds.length !== 1 ? "s" : ""} with Gemini</p>
      </div>
    );
  }

  // --- Generating ---
  if (phase === "generating") {
    const genStepIdx = GENERATION_STEPS.findIndex((s) => s.key === genStatus);
    return (
      <div className="min-h-screen bg-[#0F172A] flex items-center justify-center px-6">
        <div className="max-w-lg w-full text-center">
          <div className="relative w-24 h-24 mx-auto mb-10">
            <div className="w-24 h-24 rounded-full border-4 border-[#1E293B] border-t-[#C9A96E] animate-spin" />
            <Rocket className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-[#C9A96E] animate-pulse" />
          </div>
          <h2 className="text-3xl font-black text-white tracking-tight mb-2">Creating Masterpiece</h2>
          <p className="text-[#C9A96E] font-bold italic text-base h-6 mb-12">
            {GENERATION_STEPS.find((s) => s.key === genStatus)?.label || "Synchronising..."}
          </p>
          <div className="space-y-3">
            {GENERATION_STEPS.map((s, idx) => {
              const isPassed = idx < genStepIdx;
              const isCurrent = idx === genStepIdx;
              return (
                <div
                  key={s.key}
                  className={`flex items-center gap-4 px-5 py-3 rounded-xl border transition-all duration-500 ${
                    isPassed
                      ? "bg-[#C9A96E]/5 border-[#C9A96E]/40"
                      : isCurrent
                      ? "bg-[#1E293B]/60 border-[#C9A96E]"
                      : "bg-[#1E293B]/20 border-[#334155]"
                  }`}
                >
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 transition-all duration-500 ${
                      isPassed
                        ? "bg-[#C9A96E] shadow-[0_0_10px_rgba(201,169,110,0.5)]"
                        : isCurrent
                        ? "border-2 border-[#C9A96E]"
                        : "border-2 border-[#334155]"
                    }`}
                  >
                    {isPassed && <Check className="w-3 h-3 text-[#0F172A]" />}
                    {isCurrent && <div className="w-2 h-2 rounded-full bg-[#C9A96E] animate-pulse" />}
                  </div>
                  <span className={`text-sm font-bold ${isPassed ? "text-[#C9A96E]" : isCurrent ? "text-white" : "text-gray-600"}`}>
                    {s.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // --- Done ---
  if (phase === "done") {
    return (
      <div className="min-h-screen bg-[#0F172A] flex items-center justify-center px-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-md w-full text-center"
        >
          <div className="w-24 h-24 rounded-full bg-[#C9A96E]/10 border-2 border-[#C9A96E] flex items-center justify-center mx-auto mb-8 shadow-[0_0_40px_rgba(201,169,110,0.3)]">
            <Check className="w-10 h-10 text-[#C9A96E]" />
          </div>
          <h2 className="text-3xl font-black text-white tracking-tight mb-3">Content Ready</h2>
          <p className="text-gray-400 mb-10">Your asset has been generated from your approved strategy.</p>
          <button
            onClick={() => router.push(`/content/${contentId}`)}
            className="inline-flex items-center gap-3 bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black px-8 py-3 rounded-2xl hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] active:scale-95 transition-all"
          >
            View Content
            <ArrowRight className="w-5 h-5" />
          </button>
        </motion.div>
      </div>
    );
  }

  if (!strategy) return null;

  const fmt = strategy.recommended_format || {};

  // --- Review ---
  return (
    <div className="min-h-screen bg-[#0F172A]">
      <div className="max-w-3xl mx-auto py-12 px-6">
        <button
          onClick={() => router.back()}
          className="inline-flex items-center gap-1.5 text-gray-500 text-xs font-black uppercase tracking-[0.15em] hover:text-[#C9A96E] transition-colors mb-10"
        >
          <ChevronLeft className="w-4 h-4" />
          Back
        </button>

        <div className="mb-10">
          <div className="flex items-center gap-3 mb-2">
            <Sparkles className="w-5 h-5 text-[#C9A96E]" />
            <span className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">AI-Generated Strategy</span>
          </div>
          <h1 className="text-4xl font-black text-white tracking-tight">Review Your Strategy</h1>
          <p className="text-gray-500 mt-2">Edit any field before generating. The AI will follow this plan exactly.</p>
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key="review"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Content Angle */}
            <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155] space-y-4">
              <div className="flex items-center gap-2 mb-1">
                <Target className="w-4 h-4 text-[#C9A96E]" />
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">Content Angle</label>
              </div>
              <input
                value={strategy.content_angle}
                onChange={(e) => updateStrategy("content_angle", e.target.value)}
                className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-white font-bold text-lg focus:border-[#C9A96E] outline-none transition-all"
                placeholder="Your content angle..."
              />
              <div>
                <label className="text-[10px] font-black uppercase tracking-[0.15em] text-gray-500 block mb-2">Why This Works</label>
                <textarea
                  value={strategy.why_this_angle}
                  onChange={(e) => updateStrategy("why_this_angle", e.target.value)}
                  rows={2}
                  className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-gray-300 text-sm resize-none focus:border-[#C9A96E] outline-none transition-all"
                  placeholder="Why this angle resonates..."
                />
              </div>
              <div>
                <label className="text-[10px] font-black uppercase tracking-[0.15em] text-gray-500 block mb-2">Differentiation</label>
                <textarea
                  value={strategy.differentiation}
                  onChange={(e) => updateStrategy("differentiation", e.target.value)}
                  rows={2}
                  className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-gray-300 text-sm resize-none focus:border-[#C9A96E] outline-none transition-all"
                  placeholder="How to make this unique..."
                />
              </div>
            </div>

            {/* Recommended Format */}
            <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155] space-y-4">
              <div className="flex items-center gap-2 mb-1">
                <FileText className="w-4 h-4 text-[#C9A96E]" />
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">Recommended Format</label>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { key: "hook_style", label: "Hook Style", placeholder: "question / number / story" },
                  { key: "pacing", label: "Pacing", placeholder: "fast / medium / slow" },
                  { key: "cta_style", label: "CTA Style", placeholder: "follow / save / comment" },
                  { key: "length", label: "Length", placeholder: "30-45s / 5 slides" },
                ].map(({ key, label, placeholder }) => (
                  <div key={key}>
                    <label className="text-[10px] font-black uppercase tracking-[0.15em] text-gray-500 block mb-2">{label}</label>
                    <input
                      value={(fmt as Record<string, string>)[key] || ""}
                      onChange={(e) => updateFormat(key, e.target.value)}
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2.5 text-white text-sm focus:border-[#C9A96E] outline-none transition-all"
                      placeholder={placeholder}
                    />
                  </div>
                ))}
              </div>
            </div>

            {/* Inspired By */}
            {strategy.inspired_by && strategy.inspired_by.length > 0 && (
              <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155]">
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] block mb-4">Inspired By</label>
                <div className="space-y-3">
                  {strategy.inspired_by.map((item, i) => (
                    <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-[#0F172A]/50 border border-[#334155]">
                      <div className="w-6 h-6 rounded-lg bg-[#C9A96E]/10 border border-[#C9A96E]/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-[10px] font-black text-[#C9A96E]">{i + 1}</span>
                      </div>
                      <div className="min-w-0">
                        <p className="text-white text-sm font-bold leading-tight line-clamp-1">{item.post_title}</p>
                        <p className="text-gray-500 text-xs mt-0.5">{item.technique_borrowed}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Strategy Alternatives */}
            {strategy.alternatives && strategy.alternatives.length > 0 && (
              <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155]">
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] block mb-4">Alternative Angles</label>
                <p className="text-gray-500 text-xs mb-4">Click an alternative to swap it into your strategy.</p>
                <div className="space-y-3">
                  {strategy.alternatives.map((alt, i) => (
                    <button
                      key={i}
                      onClick={() => {
                        updateStrategy("content_angle", alt.content_angle);
                        updateStrategy("differentiation", alt.differentiation);
                        updateStrategy("why_this_angle", alt.hypothesis);
                      }}
                      className="w-full text-left p-4 rounded-xl bg-[#0F172A]/50 border border-[#334155] hover:border-[#C9A96E]/60 transition-all group"
                    >
                      <p className="text-white text-sm font-bold group-hover:text-[#C9A96E] transition-colors">{alt.content_angle}</p>
                      <p className="text-gray-500 text-xs mt-1 italic">{alt.hypothesis}</p>
                      <p className="text-gray-600 text-xs mt-1">{alt.differentiation}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* User Notes */}
            <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#334155]">
              <div className="flex items-center gap-2 mb-3">
                <Edit3 className="w-4 h-4 text-[#C9A96E]" />
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">Your Notes</label>
              </div>
              <textarea
                value={userNotes}
                onChange={(e) => setUserNotes(e.target.value)}
                rows={3}
                className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-gray-300 text-sm resize-none focus:border-[#C9A96E] outline-none transition-all"
                placeholder="Any specific instructions for the AI... (e.g. 'Open with a statistic', 'Target founders, not VCs')"
              />
            </div>

            {/* Content Type + Generate */}
            <div className="p-6 rounded-2xl bg-[#1E293B]/40 border border-[#C9A96E]/30 space-y-5">
              <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] block">Content Format</label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {CONTENT_TYPES.map((ct) => (
                  <button
                    key={ct.value}
                    onClick={() => setContentType(ct.value)}
                    className={`py-2.5 px-3 rounded-xl border text-xs font-bold transition-all ${
                      contentType === ct.value
                        ? "border-[#C9A96E] bg-[#C9A96E]/10 text-[#C9A96E]"
                        : "border-[#334155] bg-[#0F172A] text-gray-500 hover:border-[#C9A96E]/40 hover:text-white"
                    }`}
                  >
                    {ct.label}
                  </button>
                ))}
              </div>
              <button
                onClick={handleGenerate}
                className="w-full py-4 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black uppercase tracking-widest hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] transition-all active:scale-[0.98] flex items-center justify-center gap-3"
              >
                <Zap className="w-5 h-5" />
                Generate From Strategy
              </button>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

export default function SynthesizeContentPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#0F172A] flex items-center justify-center text-gray-500">Loading...</div>}>
      <SynthesizePage />
    </Suspense>
  );
}

```
