---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/app/content/[id]/page.tsx"
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
import type { ContentItem } from "@/lib/types";

export default function ContentDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [item, setItem] = useState<ContentItem | null>(null);
  const [publishing, setPublishing] = useState(false);

  useEffect(() => {
    contentApi.get(id as string).then((d) => setItem(d.item));
  }, [id, router]);

  async function handlePublish() {
    setPublishing(true);
    await contentApi.publish(id as string);
    setItem({ ...item!, status: "posted" });
    setPublishing(false);
  }

  async function handleDownload() {
    const data = await contentApi.download(id as string);
    data.download_urls.forEach((url: string) => window.open(url, "_blank"));
  }

  async function handleDelete() {
    if (!confirm("Delete this content?")) return;
    await contentApi.delete(id as string);
    router.push("/content/library");
  }

  if (!item)
    return (
      <div className="min-h-screen bg-[#0F172A] flex items-center justify-center">
        <div className="flex items-center gap-3 text-gray-400">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span className="text-sm font-medium">Loading...</span>
        </div>
      </div>
    );

  const STATUS_BADGE: Record<string, string> = {
    ready: "bg-blue-500/20 text-blue-400 border border-blue-500/30",
    posted: "bg-green-500/20 text-green-400 border border-green-500/30",
    generating: "bg-blue-400/20 text-blue-400 border border-blue-400/30",
    scripting: "bg-purple-500/20 text-purple-400 border border-purple-500/30",
    rendering: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30",
    failed: "bg-red-500/20 text-red-400 border border-red-500/30",
  };
  const statusBadge = STATUS_BADGE[item.status] ?? "bg-gray-500/20 text-gray-400 border border-gray-500/30";

  return (
    <div className="min-h-screen bg-[#0F172A]">
      <div
        className="max-w-4xl mx-auto p-8 animate-in fade-in slide-in-from-bottom-4 duration-1000"
      >
        {/* Back link */}
        <Link
          href="/content/library"
          className="text-gray-500 text-xs font-bold uppercase tracking-widest hover:text-[#C9A96E] flex items-center gap-2 mb-8 w-fit"
        >
          <ChevronLeft className="w-3.5 h-3.5" />
          Content Library
        </Link>

        {/* Header row: title + status badge */}
        <div className="flex items-start justify-between mb-4">
          <h1 className="text-4xl font-black text-white tracking-tight leading-tight max-w-2xl">
            {item.title}
          </h1>
          <span
            className={`mt-1.5 ml-4 shrink-0 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${statusBadge}`}
          >
            {item.status}
          </span>
        </div>

        {/* Info row: platform + content_type + created_at */}
        <div className="flex items-center gap-3 mb-8">
          <span className="px-3 py-1 rounded-full bg-[#1E293B]/40 border border-[#334155] text-gray-300 text-xs font-bold uppercase tracking-wider capitalize">
            {item.platform}
          </span>
          <span className="px-3 py-1 rounded-full bg-[#1E293B]/40 border border-[#334155] text-gray-300 text-xs font-bold uppercase tracking-wider capitalize">
            {item.content_type.replace("_", " ")}
          </span>
          <span className="text-gray-500 text-xs">
            {new Date(item.created_at).toLocaleDateString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric",
            })}
          </span>
        </div>

        {/* Script section */}
        <div className="mb-8">
          <h2 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-3">
            Generated Script
          </h2>
          <div className="bg-[#0F172A] rounded-2xl border border-[#334155] p-6 font-mono text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
            {item.script_text}
          </div>
        </div>

        {/* Action buttons row */}
        <div className="flex flex-wrap items-center gap-3">
          {item.status !== "posted" && (
            <button
              onClick={handlePublish}
              disabled={publishing}
              className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-[#C9A96E] to-[#8E744A] text-[#0F172A] font-black rounded-xl hover:shadow-[0_0_20px_rgba(201,169,110,0.3)] disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {publishing && <Loader2 className="w-4 h-4 animate-spin" />}
              {publishing ? "Publishing..." : "Publish"}
            </button>
          )}

          <button
            onClick={handleDownload}
            className="px-5 py-2.5 border border-[#334155] text-gray-300 hover:bg-[#1E293B] rounded-xl font-bold transition-colors"
          >
            Download
          </button>

          <Link
            href={`/content/${id}/edit`}
            className="px-5 py-2.5 border border-[#334155] text-gray-300 hover:bg-[#1E293B] rounded-xl font-bold transition-colors"
          >
            Edit
          </Link>

          <button
            onClick={handleDelete}
            className="px-5 py-2.5 border border-red-500/30 text-red-400 hover:bg-red-500/10 rounded-xl font-bold transition-colors"
          >
            Delete
          </button>
        </div>

        {/* Assets */}
        {item.asset_urls.length > 0 && (
          <div className="mt-10">
            <h2 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-3">
              Assets
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {item.asset_urls.map((url, i) => (
                <div
                  key={i}
                  className="rounded-xl overflow-hidden border border-[#334155]"
                >
                  {url.endsWith(".mp4") ? (
                    <video src={url} controls className="w-full" />
                  ) : url.endsWith(".zip") ? (
                    <a
                      href={url}
                      className="block p-6 text-center text-[#C9A96E] hover:underline font-bold text-sm"
                    >
                      Download ZIP Package
                    </a>
                  ) : (
                    <img src={url} alt={`Asset ${i + 1}`} className="w-full" />
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Error message */}
        {item.error_message && (
          <div className="mt-8 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400">
            <p className="font-bold text-sm">Error</p>
            <p className="text-sm mt-1 text-red-400/80">{item.error_message}</p>
          </div>
        )}
      </div>
    </div>
  );
}

```
