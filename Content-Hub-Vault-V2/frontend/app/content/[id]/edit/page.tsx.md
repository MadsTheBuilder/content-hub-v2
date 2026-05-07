---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/content/[id]/edit/page.tsx"
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
import { ChevronLeft, Loader2 } from "lucide-react";
import { content as contentApi } from "@/lib/api";

export default function EditContentPage() {
  const { id } = useParams();
  const router = useRouter();
  const [originalScript, setOriginalScript] = useState("");
  const [editedScript, setEditedScript] = useState("");
  const [saving, setSaving] = useState(false);
  const [title, setTitle] = useState("");

  useEffect(() => {
    contentApi.get(id as string).then((d) => {
      setOriginalScript(d.item.script_text);
      setEditedScript(d.item.script_text);
      setTitle(d.item.title);
    });
  }, [id, router]);

  async function handleSave() {
    setSaving(true);
    await contentApi.edit(id as string, editedScript);
    router.push(`/content/${id}`);
  }

  const hasChanges = originalScript !== editedScript;
  const originalWords = originalScript.split(/\s+/).filter(Boolean).length;
  const editedWords = editedScript.split(/\s+/).filter(Boolean).length;
  const wordDiff = editedWords - originalWords;

  return (
    <div className="min-h-screen bg-[#0F172A]">
      <div className="max-w-7xl mx-auto p-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
        {/* Back link */}
        <Link
          href={`/content/${id}`}
          className="text-gray-500 text-xs font-bold uppercase tracking-widest hover:text-[#C9A96E] flex items-center gap-2 mb-8 w-fit"
        >
          <ChevronLeft className="w-3.5 h-3.5" />
          Content Detail
        </Link>

        {/* Header */}
        <h1 className="text-4xl font-black text-white tracking-tight mb-8">
          Edit Script —{" "}
          <span className="text-[#C9A96E]">{title}</span>
        </h1>

        {/* Side-by-side panels */}
        <div className="grid grid-cols-2 gap-6 h-[calc(100vh-320px)] min-h-[400px]">
          {/* Left: Original (read-only) */}
          <div className="flex flex-col">
            <h2 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-3">
              Original
            </h2>
            <div className="flex-1 bg-[#0F172A] rounded-2xl border border-[#334155] p-6 font-mono text-sm text-gray-300 leading-relaxed whitespace-pre-wrap overflow-auto">
              {originalScript}
            </div>
          </div>

          {/* Right: Your Edit (editable textarea) */}
          <div className="flex flex-col">
            <h2 className="text-xs font-bold uppercase tracking-widest text-[#C9A96E] mb-3">
              Your Edit
            </h2>
            <textarea
              value={editedScript}
              onChange={(e) => setEditedScript(e.target.value)}
              className="flex-1 bg-[#0F172A] rounded-2xl border border-[#334155] p-6 font-mono text-sm text-gray-300 leading-relaxed resize-none focus:outline-none focus:border-[#C9A96E]/60 transition-colors"
            />
          </div>
        </div>

        {/* Word count diff */}
        <div className="mt-4 mb-6 flex items-center gap-2 text-sm text-gray-500">
          <span>
            Original:{" "}
            <span className="text-gray-300 font-bold">{originalWords} words</span>
          </span>
          <span className="text-gray-600">→</span>
          <span>
            Edited:{" "}
            <span className="text-gray-300 font-bold">{editedWords} words</span>
          </span>
          {hasChanges && (
            <span
              className={`font-bold ml-1 ${
                wordDiff > 0
                  ? "text-green-400"
                  : wordDiff < 0
                  ? "text-red-400"
                  : "text-gray-500"
              }`}
            >
              ({wordDiff > 0 ? `+${wordDiff}` : wordDiff})
            </span>
          )}
        </div>

        {/* Save + Cancel */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleSave}
            disabled={!hasChanges || saving}
            className="flex items-center gap-2 px-6 py-2.5 bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black rounded-xl hover:shadow-[0_0_20px_rgba(201,169,110,0.3)] disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {saving && <Loader2 className="w-4 h-4 animate-spin" />}
            {saving ? "Saving..." : "Save Changes"}
          </button>

          <Link
            href={`/content/${id}`}
            className="px-6 py-2.5 border border-[#334155] text-gray-300 hover:bg-[#1E293B] rounded-xl font-bold transition-colors"
          >
            Cancel
          </Link>
        </div>
      </div>
    </div>
  );
}

```
