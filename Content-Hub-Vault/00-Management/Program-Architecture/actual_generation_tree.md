# Content Hub — Actual Generation Tree (Audit: 2026-04-14)

> Reality-check mapping of the software's current production pipeline. 
> Legend: ✅ Implemented | ⚠️ Partial/Degraded | ❌ Not Implemented | 🧠 Learning Loop Capture

---

## 1. Voice Configuration (Setup)
*Focus: Turning brand identity into actionable scraping/scripting rules.*

| Component | Status | Capability |
|---|---|---|
| **Competitor Parsing** | ✅ | Extracts `@handles` from list and resolves to multi-platform scrape targets. |
| **Persona Extraction** | ✅ | Gemini extracts audience age, interests, and style markers (high/low energy, tone). |
| **Pillar Expansion** | ✅ | Expands topic tags (e.g., "Fitness") into 5-10 platform-native search terms per pillar. |
| **Style Profile** | ⚠️ | Captures tone/energy, but "Transition Style" cues (e.g., "calm transitions") are still passive. |

---

## 2. Platform Strategy (Setup)
*Focus: Native rules for TikTok, YouTube, Instagram, etc.*

| Component | Status | Capability |
|---|---|---|
| **Knowledge Base** | ✅ | Static database in `platform_adapter.py` for 7 platforms (ideal length, hooks, CTAs). |
| **Voice Adaptation** | ✅ | Gemini-powered tone shifting (e.g., casual TikTok vs. professional LinkedIn). |
| **Scrape Weights** | ❌ | All pillars are currently weighted equally; no platform-niche prioritization logic yet. |

---

## 3. Trending Intelligence (Discovery)
*Focus: High-volume content discovery and analysis.*

| Component | Status | Capability |
|---|---|---|
| **Scraping Engine** | ✅ | Apify-powered multi-source (Competitor + Pillar + Hashtag) discovery. |
| **Enrichment** | ✅ | Gemini analysis for "Why it works" (Hook type, Style, Pacing). |
| **Thumbnail Render** | ✅ | Backend extracts thumbnail URLs; Frontend renders card grid via `TrendingContent`. |
| **Relevance Score** | ✅ | Weighted calculation: 40% Pillar match, 30% Organic, 20% Audience, 10% Recency. |
| **User Selection** | 🧠 | Multi-select on cards; captures "Preferred Hook/Style" signals into memory. |

---

## 4. Content Synthesis (Strategy Review)
*Focus: The "Strategy Document" review step.*

| Component | Status | Capability |
|---|---|---|
| **Strategy Generation** | ✅ | Synthesizes selections + brand + memory into a 1-page strategy document. |
| **Skill Injection** | ✅ | Loads `content-strategy.md` and `psychology.md` to ground angles in research. |
| **Alt Angles** | ✅ | Generates 2 alternative angles with hypotheses for user comparison. |
| **User Edit UI** | ✅ | Frontend allows editing Angle, Format, Hooks, and adding custom Notes. |
| **Strategy Feedback** | 🧠 | Captures difference between AI proposal vs. Approved version (format/angle bias). |

---

## 5. Script Generation (Creation)
*Focus: Turning strategy into refined copy.*

| Component | Status | Capability |
|---|---|---|
| **Prompt Enrichment**| ✅ | Massive context injection: Strategy + Notes + Persona + Platform Rules + Skills. |
| **Model Fallback** | ✅ | 4-tier chain: Gemini Flash → Flash-Lite → Claude 3.5 Sonnet → Placeholder. |
| **Skill Loading** | ✅ | Contextual loading of `copywriting.md`, `social-content.md`, and `copy-editing.md`. |
| **Copy-Editing Pass** | ✅ | Immediate automated refinement pass using the `copy-editing-quick` skill. |
| **Script Edits** | 🧠 | Captures diffs between Generated vs. Final script to learn length/hook preferences. |

---

## 6. Asset Rendering (Assets)
*Focus: Final media delivery.*

| Component | Status | Capability |
|---|---|---|
| **Slides (PNG)** | ✅ | Custom Playwright renderer creates polished brand-tailored slides + watermarks. |
| **Talking Head** | ✅ | ZIP packager for script + storyboard + instructions for actors. |
| **Video (MP4)** | ❌ | **CANNOT DO.** The `remotion-service/` directory is missing; the renderer calls a non-existent endpoint. |
| **Storyboard** | ⚠️ | **DEGRADED.** Currently produces minimal structure (headlines/body) without timing, transitions, or overlays. |

---

## 7. The Learning Loop (Intelligence)
*Focus: Self-improving content engine.*

| Component | Status | Capability |
|---|---|---|
| **Publication Mem** | ✅ | Updates `content_publication_memory` on every publish (Topics, Types, Hooks). |
| **Feedback loops** | ✅ | Strategy edits + Script edits are wired; influence future prompts via `memory_ctx`. |
| **Trend Tracking** | ✅ | Weekly APScheduler jobs for trend detection and score spikes. |

---

## Current Production Pipeline: Can vs. Cannot

### ✅ THE "CAN" LIST
- **Discovery:** Can discover trending topics in 30 seconds and tell you *why* they worked.
- **Strategy:** Can propose a marketing-grounded strategy and let you tweak it.
- **Copy:** Can generate high-quality scripts that sound like your brand and match platform rules.
- **Slides:** Can produce ready-to-post carousel PNGs with your brand colors.
- **Learning:** Can get better at your style every time you edit or publish.

### ❌ THE "CANNOT" LIST
- **Video:** Cannot yet generate final MP4 videos (Video rendering is the largest technical gap).
- **Strategy Nuance:** Cannot yet prioritize pillars based on platform performance (Scrape weights).
- **Library Search:** Cannot search across historical generated content (Library is a chronological list).
- **Visual Variety:** Slides use a single (premium) template; no choice of alternative layout styles yet.
