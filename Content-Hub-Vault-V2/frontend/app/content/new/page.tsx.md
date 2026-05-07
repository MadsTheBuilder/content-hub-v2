---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/content/new/page.tsx"
category: "Content Hub Source Code"
---

# page.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronLeft,
  Video,
  FileText,
  User,
  Layout,
  Rocket,
  Sparkles,
  Check,
  Zap,
  ArrowRight,
} from "lucide-react";
import { workflows as workflowsApi, content as contentApi } from "@/lib/api";
import type { Workflow } from "@/lib/types";

const CONTENT_TYPES = [
  { value: "slides", label: "Data Slides", desc: "1-5 PNG carousel slides", icon: Layout },
  { value: "topic", label: "Topic Content", desc: "3-8 educational cards", icon: FileText },
  { value: "short_form", label: "Short-form Video", desc: "15-30s vertical MP4", icon: Video },
  { value: "talking_head", label: "Talking Head", desc: "Production ZIP (script + storyboard)", icon: User },
];

const WIZARD_STEPS = [
  { label: "Workflow + Type" },
  { label: "Platform + Topic" },
  { label: "Generating" },
];

const GENERATION_STEPS = [
  { key: "generating", label: "Initialising Neural Pipeline" },
  { key: "scripting", label: "Synthesising Narrative with Gemini" },
  { key: "rendering", label: "Processing Multimodal Assets" },
  { key: "ready", label: "Finalising Artefacts" },
];

function StepIndicator({ currentStep }: { currentStep: number }) {
  return (
    <div className="flex items-center justify-center gap-0 mb-12">
      {WIZARD_STEPS.map((step, idx) => {
        const isCompleted = idx < currentStep;
        const isActive = idx === currentStep;
        return (
          <div key={step.label} className="flex items-center">
            <div className="flex flex-col items-center gap-2">
              <div
                className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-black border-2 transition-all duration-300 ${
                  isCompleted
                    ? "bg-[#C9A96E] border-[#C9A96E] text-[#0F172A]"
                    : isActive
                    ? "bg-[#C9A96E]/10 border-[#C9A96E] text-[#C9A96E]"
                    : "bg-[#1E293B] border-[#334155] text-gray-500"
                }`}
              >
                {isCompleted ? <Check className="w-4 h-4" /> : idx + 1}
              </div>
              <span
                className={`text-[10px] font-black uppercase tracking-[0.15em] whitespace-nowrap ${
                  isActive ? "text-[#C9A96E]" : isCompleted ? "text-[#C9A96E]/60" : "text-gray-600"
                }`}
              >
                {step.label}
              </span>
            </div>
            {idx < WIZARD_STEPS.length - 1 && (
              <div
                className={`w-16 h-0.5 mb-5 mx-1 transition-all duration-500 ${
                  idx < currentStep ? "bg-[#C9A96E]" : "bg-[#334155]"
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

function NewContentContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [workflowList, setWorkflowList] = useState<Workflow[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState(searchParams.get("workflow") || "");
  const [contentType, setContentType] = useState(searchParams.get("type") || "");
  const [platform, setPlatform] = useState("");
  const [topic, setTopic] = useState(searchParams.get("topic") || "");
  const [generating, setGenerating] = useState(false);
  const [status, setStatus] = useState("");
  const [contentId, setContentId] = useState("");
  const [step, setStep] = useState(0);

  useEffect(() => {
    workflowsApi.list().then((d) => setWorkflowList(d.workflows));
  }, [router]);

  const workflow = workflowList.find((w) => w.id === selectedWorkflow);

  async function handleGenerate() {
    setGenerating(true);
    setStep(2);
    setStatus("generating");
    try {
      const data = await contentApi.generate({
        workflow_id: selectedWorkflow,
        content_type: contentType,
        platform,
        topic,
      });
      setContentId(data.content_id);
      pollStatus(data.content_id);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Generation failed");
      setGenerating(false);
      setStep(1);
    }
  }

  function pollStatus(id: string) {
    const interval = setInterval(async () => {
      try {
        const data = await contentApi.status(id);
        setStatus(data.status);
        if (data.status === "ready" || data.status === "failed") {
          clearInterval(interval);
          if (data.status === "failed") {
            setGenerating(false);
            setStep(1);
            alert("Generation failed: " + (data.error_message || "Unknown error"));
          }
        }
      } catch {
        clearInterval(interval);
        setGenerating(false);
        setStep(1);
      }
    }, 2500);
  }

  const genStepIdx = GENERATION_STEPS.findIndex((s) => s.key === status);

  // Step 3 — Generating
  if (step === 2) {
    const isReady = status === "ready";

    return (
      <div className="min-h-screen bg-[#0F172A] flex items-center justify-center px-6">
        <div className="max-w-lg w-full">
          <StepIndicator currentStep={2} />

          <AnimatePresence mode="wait">
            {isReady ? (
              <motion.div
                key="ready"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center"
              >
                <div className="w-24 h-24 rounded-full bg-[#C9A96E]/10 border-2 border-[#C9A96E] flex items-center justify-center mx-auto mb-8 shadow-[0_0_40px_rgba(201,169,110,0.3)]">
                  <Check className="w-10 h-10 text-[#C9A96E]" />
                </div>
                <h2 className="text-3xl font-black text-white tracking-tight mb-3">Content Ready</h2>
                <p className="text-gray-400 mb-10">Your asset has been generated successfully.</p>
                <button
                  onClick={() => router.push(`/content/${contentId}`)}
                  className="inline-flex items-center gap-3 bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black px-8 py-3 rounded-2xl hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] active:scale-95 transition-all"
                >
                  View Content
                  <ArrowRight className="w-5 h-5" />
                </button>
              </motion.div>
            ) : (
              <motion.div
                key="generating"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center"
              >
                <div className="relative w-24 h-24 mx-auto mb-10">
                  <div className="w-24 h-24 rounded-full border-4 border-[#1E293B] border-t-[#C9A96E] animate-spin" />
                  <Rocket className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-[#C9A96E] animate-pulse" />
                </div>

                <h2 className="text-3xl font-black text-white tracking-tight mb-2">Creating Masterpiece</h2>
                <p className="text-[#C9A96E] font-bold italic text-base h-6 mb-12">
                  {GENERATION_STEPS.find((s) => s.key === status)?.label || "Synchronising..."}
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
                        <span
                          className={`text-sm font-bold ${
                            isPassed ? "text-[#C9A96E]" : isCurrent ? "text-white" : "text-gray-600"
                          }`}
                        >
                          {s.label}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0F172A]">
      <div className="max-w-3xl mx-auto py-12 px-6">
        {/* Back link */}
        <button
          onClick={() => router.back()}
          className="inline-flex items-center gap-1.5 text-gray-500 text-xs font-black uppercase tracking-[0.15em] hover:text-[#C9A96E] transition-colors mb-10"
        >
          <ChevronLeft className="w-4 h-4" />
          Back
        </button>

        {/* Header */}
        <div className="mb-10">
          <h1 className="text-4xl font-black text-white tracking-tight">New Content</h1>
          <p className="text-gray-500 mt-2">Generate high-fidelity assets for your brand</p>
        </div>

        <StepIndicator currentStep={step} />

        <AnimatePresence mode="wait">
          {/* Step 1 — Workflow + Type */}
          {step === 0 && (
            <motion.div
              key="step0"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-10"
            >
              {/* Workflow cards */}
              <section className="space-y-4">
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">
                  Select Target Engine
                </label>
                {workflowList.length === 0 ? (
                  <div className="py-10 text-center text-gray-600 text-sm border border-[#334155] rounded-2xl bg-[#1E293B]/20">
                    No workflows found. Create one first.
                  </div>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {workflowList.map((w) => {
                      const selected = selectedWorkflow === w.id;
                      return (
                        <button
                          key={w.id}
                          onClick={() => { setSelectedWorkflow(w.id); setPlatform(""); }}
                          className={`p-5 rounded-2xl border text-left transition-all duration-300 group ${
                            selected
                              ? "border-[#C9A96E] bg-[#C9A96E]/5 shadow-[0_0_20px_rgba(201,169,110,0.1)]"
                              : "bg-[#1E293B]/40 border-[#334155] hover:border-[#C9A96E]/40"
                          }`}
                        >
                          <div className="flex items-center justify-between mb-2">
                            <p className={`font-bold text-sm ${selected ? "text-white" : "text-gray-300"}`}>
                              {w.name}
                            </p>
                            {selected && <div className="w-2 h-2 rounded-full bg-[#C9A96E] shadow-[0_0_6px_rgba(201,169,110,0.8)]" />}
                          </div>
                          <p className="text-xs text-gray-600 capitalize">{w.template_type}</p>
                          {w.platforms.length > 0 && (
                            <div className="flex gap-1.5 flex-wrap mt-3">
                              {w.platforms.slice(0, 4).map((p) => (
                                <span
                                  key={p}
                                  className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-lg bg-[#0F172A] border border-[#334155] text-gray-500"
                                >
                                  {p}
                                </span>
                              ))}
                            </div>
                          )}
                        </button>
                      );
                    })}
                  </div>
                )}
              </section>

              {/* Content type tiles */}
              <section className="space-y-4">
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">
                  Content Modality
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {CONTENT_TYPES.map((ct) => {
                    const Icon = ct.icon;
                    const selected = contentType === ct.value;
                    return (
                      <button
                        key={ct.value}
                        onClick={() => setContentType(ct.value)}
                        className={`relative p-6 rounded-2xl border text-left transition-all duration-300 group overflow-hidden ${
                          selected
                            ? "border-[#C9A96E] bg-[#C9A96E]/5 shadow-[0_0_20px_rgba(201,169,110,0.1)]"
                            : "bg-[#1E293B]/40 border-[#334155] hover:border-[#C9A96E]/40"
                        }`}
                      >
                        <div
                          className={`w-10 h-10 rounded-xl flex items-center justify-center mb-4 transition-colors ${
                            selected
                              ? "bg-[#C9A96E] text-[#0F172A]"
                              : "bg-[#0F172A] border border-[#334155] text-gray-400 group-hover:text-white"
                          }`}
                        >
                          <Icon className="w-5 h-5" />
                        </div>
                        <p className={`font-bold transition-colors ${selected ? "text-white" : "text-gray-300"}`}>
                          {ct.label}
                        </p>
                        <p className="text-xs text-gray-500 mt-1 leading-snug">{ct.desc}</p>
                        {selected && (
                          <div className="absolute top-3 right-3 w-2 h-2 rounded-full bg-[#C9A96E] shadow-[0_0_6px_rgba(201,169,110,0.8)]" />
                        )}
                      </button>
                    );
                  })}
                </div>
              </section>

              <div className="pt-4">
                <button
                  onClick={() => setStep(1)}
                  disabled={!selectedWorkflow || !contentType}
                  className="w-full py-4 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black uppercase tracking-widest hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] disabled:opacity-40 transition-all active:scale-[0.98] flex items-center justify-center gap-3"
                >
                  Continue
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </motion.div>
          )}

          {/* Step 2 — Platform + Topic */}
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-10"
            >
              {/* Platform pills */}
              <section className="space-y-4">
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">
                  Platform Optimisation
                </label>
                {workflow ? (
                  <div className="flex gap-3 flex-wrap">
                    {workflow.platforms.map((p) => (
                      <button
                        key={p}
                        onClick={() => setPlatform(p)}
                        className={`px-6 py-2.5 rounded-xl capitalize font-bold border transition-all text-xs tracking-widest ${
                          platform === p
                            ? "bg-[#C9A96E] text-[#0F172A] border-[#C9A96E] shadow-[0_0_15px_rgba(201,169,110,0.3)]"
                            : "bg-[#0F172A] text-gray-500 border-[#334155] hover:border-[#C9A96E] hover:text-white"
                        }`}
                      >
                        {p}
                      </button>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-600 text-sm">No workflow selected.</p>
                )}
              </section>

              {/* Topic textarea */}
              <section className="space-y-4">
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">
                  Topic or Thesis
                </label>
                <div className="relative">
                  <div className="absolute left-5 top-5 text-[#C9A96E] opacity-50">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <textarea
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    className="w-full pl-12 pr-6 py-4 rounded-2xl bg-[#1E293B]/40 border border-[#334155] text-white focus:border-[#C9A96E] outline-none h-36 resize-none transition-all placeholder:text-gray-600 font-medium italic"
                    placeholder="e.g. Why deep work is the ultimate competitive advantage in the AI era..."
                  />
                </div>
              </section>

              <div className="flex gap-4 pt-4">
                <button
                  onClick={() => setStep(0)}
                  className="px-6 py-4 rounded-2xl bg-[#1E293B]/40 border border-[#334155] text-gray-400 font-black uppercase tracking-widest hover:border-[#C9A96E]/40 hover:text-white transition-all flex items-center gap-2"
                >
                  <ChevronLeft className="w-5 h-5" />
                  Back
                </button>
                <button
                  onClick={handleGenerate}
                  disabled={!platform || !topic}
                  className="flex-1 py-4 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black uppercase tracking-widest hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] disabled:opacity-40 transition-all active:scale-[0.98] flex items-center justify-center gap-3"
                >
                  <Zap className="w-5 h-5" />
                  Initialise Generation
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default function NewContentPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#0F172A] flex items-center justify-center text-gray-500">Loading...</div>}>
      <NewContentContent />
    </Suspense>
  );
}

```
