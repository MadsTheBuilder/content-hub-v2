---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/brand/[workflowId]/page.tsx"
category: "Content Hub Source Code"
---

# page.tsx

**Description:** Next.js frontend page component defining routing and page layout.

---

```typescript
"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { ChevronLeft, Save, Loader2 } from "lucide-react";
import { brand as brandApi } from "@/lib/api";
import type { BrandConfig } from "@/lib/types";

const FONT_OPTIONS = [
  "Inter",
  "Roboto",
  "Poppins",
  "Montserrat",
  "Open Sans",
  "Lato",
  "Playfair Display",
];

export default function BrandConfigPage() {
  const { workflowId } = useParams();
  const router = useRouter();
  const [config, setConfig] = useState<BrandConfig | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    brandApi.get(workflowId as string).then((d) => setConfig(d.brand));
  }, [workflowId, router]);

  async function handleSave() {
    if (!config) return;
    setSaving(true);
    await brandApi.update(workflowId as string, {
      primary_color: config.primary_color,
      secondary_color: config.secondary_color,
      accent_color: config.accent_color,
      font_family: config.font_family,
      watermark_enabled: config.watermark_enabled,
      watermark_text: config.watermark_text,
    });
    setSaving(false);
    router.push(`/workflows/${workflowId}`);
  }

  if (!config) {
    return (
      <div className="min-h-screen bg-[#0F172A] flex items-center justify-center">
        <div className="flex items-center gap-3 text-gray-500">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span className="text-sm font-bold uppercase tracking-widest">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="min-h-screen bg-[#0F172A]"
    >
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Back link */}
        <Link
          href={`/workflows/${workflowId}`}
          className="inline-flex items-center gap-1.5 text-gray-500 text-xs font-black uppercase tracking-[0.15em] hover:text-[#C9A96E] transition-colors mb-10"
        >
          <ChevronLeft className="w-4 h-4" />
          Workflow
        </Link>

        {/* Page header */}
        <div className="mb-10">
          <h1 className="text-4xl font-black text-white tracking-tight">Brand Protocol</h1>
          <p className="text-gray-500 mt-2">Configure visual identity for your content engine</p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-5 gap-8 items-start">
          {/* Form — left 3 cols */}
          <div className="xl:col-span-3 space-y-6">

            {/* Colour System */}
            <div className="bg-[#1E293B]/40 border border-[#334155] rounded-2xl p-6 space-y-5">
              <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] block">
                Colour System
              </label>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                {/* Primary color */}
                <div className="space-y-2">
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Primary</p>
                  <div className="flex items-center gap-3">
                    <div className="relative flex-shrink-0">
                      <input
                        type="color"
                        value={config.primary_color}
                        onChange={(e) => setConfig({ ...config, primary_color: e.target.value })}
                        className="w-12 h-12 rounded-xl cursor-pointer border-2 border-[#334155] bg-transparent p-0.5"
                      />
                    </div>
                    <input
                      type="text"
                      value={config.primary_color}
                      onChange={(e) => setConfig({ ...config, primary_color: e.target.value })}
                      className="bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[#C9A96E] transition-colors w-full font-mono text-sm"
                      placeholder="#000000"
                    />
                  </div>
                </div>

                {/* Secondary color */}
                <div className="space-y-2">
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Secondary</p>
                  <div className="flex items-center gap-3">
                    <div className="relative flex-shrink-0">
                      <input
                        type="color"
                        value={config.secondary_color}
                        onChange={(e) => setConfig({ ...config, secondary_color: e.target.value })}
                        className="w-12 h-12 rounded-xl cursor-pointer border-2 border-[#334155] bg-transparent p-0.5"
                      />
                    </div>
                    <input
                      type="text"
                      value={config.secondary_color}
                      onChange={(e) => setConfig({ ...config, secondary_color: e.target.value })}
                      className="bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[#C9A96E] transition-colors w-full font-mono text-sm"
                      placeholder="#000000"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Typography */}
            <div className="bg-[#1E293B]/40 border border-[#334155] rounded-2xl p-6 space-y-4">
              <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] block">
                Typography
              </label>
              <div className="space-y-2">
                <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Font Family</p>
                <select
                  value={config.font_family}
                  onChange={(e) => setConfig({ ...config, font_family: e.target.value })}
                  className="bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[#C9A96E] transition-colors w-full appearance-none cursor-pointer"
                >
                  {FONT_OPTIONS.map((f) => (
                    <option key={f} value={f}>
                      {f}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Voice Signature */}
            <div className="bg-[#1E293B]/40 border border-[#334155] rounded-2xl p-6 space-y-4">
              <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] block">
                Voice Signature
              </label>
              <div className="space-y-2">
                <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Style Notes</p>
                <textarea
                  value={config.watermark_text}
                  onChange={(e) => setConfig({ ...config, watermark_text: e.target.value })}
                  rows={4}
                  className="bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[#C9A96E] transition-colors w-full resize-none placeholder:text-gray-600 italic"
                  placeholder="Describe your brand voice, tone, and content style..."
                />
              </div>

              {/* Watermark toggle */}
              <div className="flex items-center gap-3 pt-2">
                <button
                  onClick={() => setConfig({ ...config, watermark_enabled: !config.watermark_enabled })}
                  className={`relative w-11 h-6 rounded-full border-2 transition-all duration-300 flex-shrink-0 ${
                    config.watermark_enabled
                      ? "bg-[#C9A96E]/20 border-[#C9A96E]"
                      : "bg-[#0F172A] border-[#334155]"
                  }`}
                >
                  <div
                    className={`absolute top-0.5 w-4 h-4 rounded-full transition-all duration-300 ${
                      config.watermark_enabled
                        ? "left-5 bg-[#C9A96E]"
                        : "left-0.5 bg-[#334155]"
                    }`}
                  />
                </button>
                <span className="text-sm font-bold text-gray-400">Enable Watermark</span>
              </div>
            </div>

            {/* Save button */}
            <button
              onClick={handleSave}
              disabled={saving}
              className="w-full flex items-center justify-center gap-3 bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black px-8 py-3 rounded-2xl hover:shadow-[0_0_30px_rgba(201,169,110,0.4)] active:scale-95 disabled:opacity-50 transition-all uppercase tracking-widest"
            >
              {saving ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  Save Brand Protocol
                </>
              )}
            </button>
          </div>

          {/* Live preview — right 2 cols */}
          <div className="xl:col-span-2">
            <div className="sticky top-8">
              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#C9A96E] mb-4">
                Live Preview
              </p>

              <div className="bg-[#1E293B]/40 border border-[#334155] rounded-2xl overflow-hidden">
                {/* Preview card */}
                <div
                  className="p-8 flex flex-col gap-4 min-h-[220px] justify-center transition-all duration-300"
                  style={{ backgroundColor: config.primary_color, fontFamily: config.font_family }}
                >
                  <h3
                    className="text-2xl font-black leading-tight"
                    style={{ color: config.accent_color }}
                  >
                    Sample Headline
                  </h3>
                  <p
                    className="text-sm leading-relaxed opacity-80"
                    style={{ color: config.secondary_color || "#ffffff" }}
                  >
                    This is how your brand content will look. Typography and colour choices shape your audience's perception.
                  </p>
                  <div
                    className="inline-flex w-fit px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider"
                    style={{ backgroundColor: config.accent_color, color: config.primary_color }}
                  >
                    Call to Action
                  </div>
                </div>

                {/* Color chips */}
                <div className="px-5 py-4 border-t border-[#334155] flex items-center gap-3">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-5 h-5 rounded-lg border border-white/10 flex-shrink-0"
                      style={{ backgroundColor: config.primary_color }}
                    />
                    <span className="text-[10px] font-bold text-gray-600 uppercase tracking-wider font-mono">
                      {config.primary_color}
                    </span>
                  </div>
                  <div className="w-px h-4 bg-[#334155]" />
                  <div className="flex items-center gap-2">
                    <div
                      className="w-5 h-5 rounded-lg border border-white/10 flex-shrink-0"
                      style={{ backgroundColor: config.secondary_color }}
                    />
                    <span className="text-[10px] font-bold text-gray-600 uppercase tracking-wider font-mono">
                      {config.secondary_color}
                    </span>
                  </div>
                </div>

                {/* Font specimen */}
                <div className="px-5 py-4 border-t border-[#334155]">
                  <p className="text-[10px] font-black uppercase tracking-[0.15em] text-gray-600 mb-2">
                    Typeface
                  </p>
                  <p
                    className="text-white text-lg font-bold"
                    style={{ fontFamily: config.font_family }}
                  >
                    {config.font_family}
                  </p>
                  <p
                    className="text-gray-500 text-xs mt-1"
                    style={{ fontFamily: config.font_family }}
                  >
                    Aa Bb Cc — The quick brown fox
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

```
