---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/workflows/new/page.tsx"
category: "Content Hub Source Code"
---

# page.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ChevronRight, 
  ChevronLeft, 
  Check, 
  Sparkles, 
  Rocket, 
  Search, 
  Globe,
  Dumbbell,
  Home,
  Code,
  DollarSign,
  UserCircle
} from "lucide-react";
import { workflows as workflowsApi } from "@/lib/api";
import type { NicheTemplate, QuestionnaireItem } from "@/lib/types";

const STEPS = ["Niche", "Voice", "Platforms", "Review", "Engine"];

const ICON_MAP: Record<string, any> = {
  fitness: Dumbbell,
  real_estate: Home,
  software_dev: Code,
  finance: DollarSign,
  coaching: UserCircle,
  custom: Sparkles
};

export default function NewWorkflowPage() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [templates, setTemplates] = useState<Record<string, NicheTemplate>>({});
  const [questionnaire, setQuestionnaire] = useState<QuestionnaireItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);

  // Form state
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [name, setName] = useState("");
  const [brandVoice, setBrandVoice] = useState("");
  const [pillars, setPillars] = useState<string[]>([]);
  const [platforms, setPlatforms] = useState<string[]>([]);
  const [competitors, setCompetitors] = useState("");
  const [questionnaireAnswers, setQuestionnaireAnswers] = useState<Record<string, string | string[]>>({});

  useEffect(() => {
    workflowsApi.templates().then((data) => {
      setTemplates(data.templates);
      setQuestionnaire(data.questionnaire);
    });
  }, []);

  const isCustom = selectedTemplate === "custom";
  const template = templates[selectedTemplate];

  function handleTemplateSelect(key: string) {
    setSelectedTemplate(key);
    const t = templates[key];
    if (t && !t.requires_questionnaire) {
      setPillars(t.content_pillars);
      setPlatforms(t.platform_defaults);
      setName(t.name);
    } else {
      setPillars([]);
      setPlatforms([]);
      setName("");
    }
    setStep(1);
  }

  async function handleCreate() {
    setLoading(true);
    try {
      const data = await workflowsApi.create({
        name,
        template_type: selectedTemplate,
        brand_voice: brandVoice,
        content_pillars: pillars,
        platforms,
        competitors: competitors.split(",").map((c) => c.trim()).filter(Boolean),
        questionnaire_answers: isCustom ? questionnaireAnswers : null,
      });
      const workflowId = data.workflow.id;

      // Step 5: Initial scrape
      setStep(4);
      setScraping(true);
      await workflowsApi.scrape(workflowId);
      setScraping(false);

      router.push(`/workflows/${workflowId}`);
    } catch (err) {
      setLoading(false);
      alert(err instanceof Error ? err.message : "Failed to create workflow");
    }
  }

  const allPlatforms = ["tiktok", "instagram", "youtube", "linkedin", "twitter", "facebook"];

  return (
    <div className="max-w-4xl mx-auto py-12 px-6">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-black text-white tracking-tight mb-4">Initialise Engine</h1>
        <p className="text-gray-400">Configure your autonomous content pipeline in {STEPS.length} steps</p>
      </div>

      {/* Step indicator */}
      <div className="relative mb-8 px-4">
        <div className="absolute top-1/2 left-0 w-full h-0.5 bg-[#1E293B] -translate-y-1/2" />
        <div 
          className="absolute top-1/2 left-0 h-0.5 bg-[#C9A96E] -translate-y-1/2 transition-all duration-500" 
          style={{ width: `${(step / (STEPS.length - 1)) * 100}%` }}
        />
        <div className="relative flex justify-between">
          {STEPS.map((s, i) => (
            <div key={s} className="flex flex-col items-center">
              <div 
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
                  i < step ? "bg-[#C9A96E] border-[#C9A96E] text-[#0F172A]" : 
                  i === step ? "bg-[#0F172A] border-[#C9A96E] text-[#C9A96E] shadow-[0_0_15px_rgba(201,169,110,0.3)]" : 
                  "bg-[#0F172A] border-[#334155] text-gray-500"
                }`}
              >
                {i < step ? <Check className="w-5 h-5 font-bold" /> : <span className="text-sm font-bold">{i + 1}</span>}
              </div>
              <span className={`absolute -bottom-7 text-[10px] font-bold uppercase tracking-widest ${i <= step ? "text-[#C9A96E]" : "text-gray-500"}`}>
                {s}
              </span>
            </div>
          ))}
        </div>
      </div>

      <AnimatePresence mode="sync">
        <motion.div
          key={step}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.15 }}
          className="min-h-0"
        >
          {/* ── Step 0: Template ── */}
          {step === 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(templates).map(([key, t]) => {
                const Icon = ICON_MAP[key] || Sparkles;
                return (
                  <button
                    key={key}
                    onClick={() => handleTemplateSelect(key)}
                    className="group relative p-8 rounded-3xl bg-[#1E293B]/40 border border-[#334155] hover:border-[#C9A96E]/50 transition-all text-left overflow-hidden"
                  >
                    <div className="absolute -right-4 -top-4 w-24 h-24 bg-[#C9A96E]/5 rounded-full blur-2xl group-hover:bg-[#C9A96E]/10 transition-colors" />
                    <div className="w-12 h-12 rounded-2xl bg-[#0F172A] border border-[#334155] flex items-center justify-center mb-6 group-hover:bg-[#C9A96E] transition-colors">
                      <Icon className="w-6 h-6 text-[#C9A96E] group-hover:text-[#0F172A]" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">{t.name}</h3>
                    <p className="text-sm text-gray-400 leading-relaxed">{t.description}</p>
                  </button>
                );
              })}
            </div>
          )}

          {/* ── Step 1: Brand / Questionnaire ── */}
          {step === 1 && (
            <div className="bg-[#1E293B]/40 border border-[#334155] rounded-3xl p-8 space-y-8">
              {isCustom && questionnaire.map((q) => (
                <div key={q.id} className="space-y-3">
                  <label className="text-sm font-bold uppercase tracking-widest text-gray-400">{q.question}</label>
                  {q.type === "text" && (
                    <input
                      type="text"
                      spellCheck={true}
                      autoCorrect="on"
                      value={(questionnaireAnswers[q.id] as string) || ""}
                      onChange={(e) => setQuestionnaireAnswers({ ...questionnaireAnswers, [q.id]: e.target.value })}
                      className="w-full px-5 py-4 rounded-2xl bg-[#0F172A] border border-[#334155] text-white focus:border-[#C9A96E] focus:outline-none focus:ring-1 focus:ring-[#C9A96E]/20 transition-all font-medium"
                      placeholder="Type your response..."
                    />
                  )}
                  {(q.type === "choice" || q.type === "multi_choice") && (
                    <div className="flex flex-wrap gap-3">
                      {q.options?.map((opt) => {
                        const isMulti = q.type === "multi_choice";
                        const selected = isMulti
                          ? ((questionnaireAnswers[q.id] as string[]) || []).includes(opt)
                          : questionnaireAnswers[q.id] === opt;
                        return (
                          <button
                            key={opt}
                            onClick={() => {
                              if (isMulti) {
                                const current = (questionnaireAnswers[q.id] as string[]) || [];
                                setQuestionnaireAnswers({ ...questionnaireAnswers, [q.id]: selected ? current.filter((c) => c !== opt) : [...current, opt] });
                              } else {
                                setQuestionnaireAnswers({ ...questionnaireAnswers, [q.id]: opt });
                              }
                            }}
                            className={`px-5 py-3 rounded-2xl text-xs font-bold border transition-all ${selected ? "bg-[#C9A96E] text-[#0F172A] border-[#C9A96E]" : "bg-[#0F172A] text-gray-400 border-[#334155] hover:border-[#C9A96E] hover:text-white"}`}
                          >{opt}</button>
                        );
                      })}
                    </div>
                  )}
                </div>
              ))}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-3">
                  <label className="text-sm font-bold uppercase tracking-widest text-gray-400">Workflow Identity</label>
                  <input
                    type="text"
                    spellCheck={true}
                    autoCorrect="on"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-5 py-4 rounded-2xl bg-[#0F172A] border border-[#334155] text-white focus:border-[#C9A96E] outline-none transition-all font-medium"
                    placeholder="e.g. Real Estate Insider"
                  />
                </div>
                <div className="space-y-3">
                  <label className="text-sm font-bold uppercase tracking-widest text-gray-400">Competitors (Comma-separated)</label>
                  <input
                    type="text"
                    spellCheck={false}
                    value={competitors}
                    onChange={(e) => setCompetitors(e.target.value)}
                    className="w-full px-5 py-4 rounded-2xl bg-[#0F172A] border border-[#334155] text-white focus:border-[#C9A96E] outline-none transition-all font-medium"
                    placeholder="@alex, @serena"
                  />
                </div>
              </div>

              <div className="space-y-3">
                <label className="text-sm font-bold uppercase tracking-widest text-gray-400">Brand Persona</label>
                <textarea
                  spellCheck={true}
                  autoCorrect="on"
                  value={brandVoice}
                  onChange={(e) => setBrandVoice(e.target.value)}
                  className="w-full px-5 py-4 rounded-2xl bg-[#0F172A] border border-[#334155] text-white focus:border-[#C9A96E] outline-none h-32 resize-none transition-all font-medium leading-relaxed"
                  placeholder="Describe your brand's unique energy, tone, and vocabulary..."
                />
              </div>

              <div className="space-y-3">
                <label className="text-sm font-bold uppercase tracking-widest text-gray-400">Content Pillars</label>
                <div className="flex flex-wrap gap-3 mb-3">
                  {pillars.map((p, i) => (
                    <motion.span key={i} layout initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }}
                      className="px-4 py-2 rounded-xl bg-[#C9A96E]/10 border border-[#C9A96E]/30 text-[#C9A96E] text-xs font-bold flex items-center gap-2"
                    >
                      {p}
                      <button onClick={() => setPillars(pillars.filter((_, j) => j !== i))} className="ml-1 hover:text-white transition-colors">&times;</button>
                    </motion.span>
                  ))}
                </div>
                <div className="relative group">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-[#C9A96E] transition-colors" />
                  <input
                    type="text"
                    spellCheck={true}
                    placeholder="Type a research pillar and press Enter"
                    className="w-full px-12 py-4 rounded-2xl bg-[#0F172A] border border-[#334155] text-white focus:border-[#C9A96E] outline-none transition-all font-medium"
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault();
                        const val = (e.target as HTMLInputElement).value.trim();
                        if (val && !pillars.includes(val)) { setPillars([...pillars, val]); (e.target as HTMLInputElement).value = ""; }
                      }
                    }}
                  />
                </div>
              </div>

              <div className="flex justify-between pt-6">
                <button onClick={() => setStep(0)} className="flex items-center gap-2 px-6 py-3 text-gray-400 hover:text-white font-bold transition-colors">
                  <ChevronLeft className="w-5 h-5" />Back
                </button>
                <button onClick={() => setStep(2)} disabled={!name}
                  className="flex items-center gap-2 px-10 py-3 rounded-2xl bg-[#C9A96E] text-[#0F172A] font-black uppercase tracking-widest disabled:opacity-50 hover:shadow-[0_0_20px_rgba(201,169,110,0.4)] transition-all active:scale-95"
                >
                  Next Step<ChevronRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}

          {/* ── Step 2: Platforms ── */}
          {step === 2 && (
            <div className="bg-[#1E293B]/40 border border-[#334155] rounded-3xl p-8 space-y-8">
              <div>
                <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] mb-1">Distribution Strategy</p>
                <p className="text-gray-400 text-sm">Select every platform you want to publish to. Toggle to add or remove.</p>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {allPlatforms.map((p) => {
                  const selected = platforms.includes(p);
                  return (
                    <button
                      key={p}
                      onClick={() => setPlatforms(selected ? platforms.filter((x) => x !== p) : [...platforms, p])}
                      className={`group relative p-6 rounded-2xl border text-center capitalize transition-all duration-200 overflow-hidden ${
                        selected ? "bg-[#C9A96E]/10 border-[#C9A96E] text-[#C9A96E] shadow-[0_0_15px_rgba(201,169,110,0.1)]"
                               : "bg-[#0F172A] border-[#334155] text-gray-500 hover:border-[#C9A96E]/50 hover:text-gray-300"}`}
                    >
                      <Globe className={`w-6 h-6 mx-auto mb-3 transition-colors ${selected ? "text-[#C9A96E]" : "text-gray-600 group-hover:text-gray-400"}`} />
                      <span className="font-bold tracking-tight">{p}</span>
                      {selected && <div className="absolute top-2 right-2 w-2 h-2 rounded-full bg-[#C9A96E]" />}
                    </button>
                  );
                })}
              </div>
              <div className="flex justify-between pt-2">
                <button onClick={() => setStep(1)} className="flex items-center gap-2 px-6 py-3 text-gray-400 hover:text-white font-bold transition-colors">
                  <ChevronLeft className="w-4 h-4" />Back
                </button>
                <button onClick={() => setStep(3)} disabled={platforms.length === 0}
                  className="flex items-center gap-2 px-10 py-3 rounded-2xl bg-[#C9A96E] text-[#0F172A] font-black uppercase tracking-widest disabled:opacity-50 hover:shadow-[0_0_20px_rgba(201,169,110,0.4)] transition-all active:scale-95"
                >
                  Confirm Strategy<ChevronRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}

          {/* ── Step 3: Review ── */}
          {step === 3 && (
            <div className="bg-[#1E293B]/40 border border-[#334155] rounded-3xl p-8 space-y-10">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                <div className="space-y-6">
                  <div className="space-y-1">
                    <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">Niche & Identity</p>
                    <h4 className="text-2xl font-bold text-white leading-tight">{name}</h4>
                    <p className="text-gray-400 text-sm font-medium">{template?.name || selectedTemplate}</p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">Persona Definition</p>
                    <p className="text-gray-300 text-sm italic leading-relaxed">"{brandVoice || "Universal authority"}"</p>
                  </div>
                </div>
                <div className="space-y-10">
                  <div className="space-y-3">
                    <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">Platform Matrix</p>
                    <div className="flex flex-wrap gap-2">
                      {platforms.map(p => <span key={p} className="px-3 py-1.5 rounded-xl bg-[#0F172A] border border-[#334155] text-xs font-bold text-gray-300 capitalize">{p}</span>)}
                    </div>
                  </div>
                  <div className="space-y-3">
                    <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E]">Research Anchors</p>
                    <div className="flex flex-wrap gap-2">
                      {pillars.map(p => <span key={p} className="px-3 py-1.5 rounded-xl bg-[#0F172A] border border-[#334155] text-xs font-medium text-gray-300">{p}</span>)}
                      {pillars.length === 0 && <span className="text-xs text-gray-600">No pillars defined</span>}
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-between pt-10 border-t border-[#334155]">
                <button onClick={() => setStep(2)} className="flex items-center gap-2 px-6 py-3 text-gray-400 hover:text-white font-bold transition-colors">
                  <ChevronLeft className="w-5 h-5" />Modify
                </button>
                <button onClick={handleCreate} disabled={loading}
                  className="flex items-center gap-3 px-10 py-4 rounded-2xl bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black uppercase tracking-widest hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] disabled:opacity-50 transition-all active:scale-95"
                >
                  <Rocket className="w-5 h-5" />Launch Content Engine
                </button>
              </div>
            </div>
          )}

          {/* ── Step 4: Initial Scrape ── */}
          {step === 4 && (
            <div className="flex flex-col items-center justify-center min-h-[500px] p-8 text-center">
              <div className="relative mb-8">
                <div className="w-24 h-24 rounded-full border-4 border-[#1E293B] border-t-[#C9A96E] animate-spin" />
                <Sparkles className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-[#C9A96E] animate-pulse" />
              </div>
              <h2 className="text-3xl font-black text-white mb-3">Syncing Neural Networks</h2>
              <p className="text-gray-400 max-w-sm mx-auto animate-pulse">
                {scraping
                  ? "Scouring platforms for high-performance organic trends... Initialising RAG vector embeddings."
                  : "Calibrating brand voice layers and synthesis models..."}
              </p>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

```
