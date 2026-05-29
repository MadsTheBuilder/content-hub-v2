---
status: Draft
date: 2026-05-21
type: design_spec
description: "Claude Design handoff spec for the Content Hub V2 web app — layout, design system, pipeline stage workspaces, Knowledge Brain section, and component-level detail."
tags: [design, frontend, handoff, web-app, pipeline]
---

# Content Hub — Web App Design Specification
**Handoff to Claude Design | Version 1.0 | 2026-05-21**

References: [[Local_First_Skill_Engine_Plan]], [[context]]
Implements: [[researcher]], [[ideation]], [[hook]], [[outline]], [[cascade]]

---

## 1. System Overview

Content Hub is a local-first AI content production engine for YouTube creators. It turns trending signals and deep research into fully scripted, distribution-ready videos through a 5-stage pipeline described in [[Local_First_Skill_Engine_Plan]]:

**Trends → Research → Ideation → Hooks → Distribution**

Each stage is powered by AI and can be run independently. The web app is the control center — a creator studio, not a generic SaaS dashboard.

---

## 2. Design Personality

**The feeling:** A professional recording studio combined with an intelligence analyst's workstation. Precision and creative energy at once.

**Tone:** Dark, focused, high-signal. Not sterile enterprise. Not loud startup.

**References:**
- Layout discipline: Linear, Raycast
- Creative warmth: Arc browser, Framer
- Data density: Vercel dashboard, Posthog

**Not:** Notion-blank-page minimalism. Not Canva-colorful. Not a generic ChatGPT wrapper UI.

---

## 3. Design System

### Color Palette

| Token | Value | Use |
|-------|-------|-----|
| `bg-base` | `#0D0F12` | App background |
| `bg-surface` | `#13161B` | Cards, panels |
| `bg-elevated` | `#1A1E26` | Inputs, dropzones |
| `border` | `#252932` | Dividers, card borders |
| `border-active` | `#3A4152` | Focused/hovered states |
| `text-primary` | `#F0F2F5` | Headings, primary text |
| `text-secondary` | `#7A8394` | Labels, timestamps, meta |
| `text-muted` | `#4A5366` | Placeholder text |
| `accent` | `#5B8DEF` | CTAs, active states, links |
| `accent-glow` | `#5B8DEF22` | Glow halos on active elements |
| `success` | `#3DD68C` | Completed stage indicators |
| `warning` | `#F5A623` | Running/in-progress state |
| `danger` | `#E5534B` | Errors |
| `stage-trends` | `#F5A623` | Trends stage identity |
| `stage-research` | `#5B8DEF` | Research stage identity |
| `stage-ideation` | `#A855F7` | Ideation stage identity |
| `stage-hooks` | `#EC4899` | Hooks stage identity |
| `stage-distribution` | `#3DD68C` | Distribution stage identity |
| `brain` | `#06B6D4` | Knowledge Brain identity |

### Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| App name / logo | Geist Mono | 15px | 600 |
| Page heading | Inter | 24px | 600 |
| Card heading | Inter | 14px | 600 |
| Body text | Inter | 14px | 400 |
| Labels / meta | Inter | 12px | 400 |
| Code / output | Geist Mono | 13px | 400 |

### Spacing

4px base unit. Cards use 20px internal padding. Section gaps 24px. Sidebar width: 240px expanded / 56px collapsed.

### Border Radius

- Cards: 12px
- Inputs: 8px
- Buttons: 6px
- Stage pills/badges: 4px
- Avatars/icons: 8px

### Iconography

Use [Lucide Icons](https://lucide.dev) throughout. Stroke weight: 1.5px. Size: 16px inline, 20px in sidebar nav, 24px in section headers.

---

## 4. Layout Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  SIDEBAR (240px / 56px collapsed)  │  MAIN CONTENT AREA         │
│                                    │                            │
│  [Logo]                            │  [Page Header]             │
│                                    │                            │
│  PIPELINE                          │  [Content — varies by      │
│  ○ Trends                          │   active view]             │
│  ○ Research                        │                            │
│  ○ Ideation                        │                            │
│  ○ Hooks                           │                            │
│  ○ Distribution                    │                            │
│                                    │                            │
│  ─────────────────                 │                            │
│                                    │                            │
│  ● Knowledge Brain                 │                            │
│                                    │                            │
│  ─────────────────                 │                            │
│                                    │                            │
│  [Settings]                        │                            │
│  [Collapse ›]                      │                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Left Sidebar — Detailed Spec

### Behavior
- Default state: **expanded** (240px)
- Collapsed state: **icon-only** (56px) — labels hidden, tooltips on hover
- Toggle: click chevron button at bottom, or keyboard shortcut `Cmd/Ctrl + \`
- Transition: smooth 200ms ease, sidebar slides left, main content expands
- State persists in localStorage

### Structure (top to bottom)

**Brand mark** (top, 56px tall)
- Logo mark (16x16 geometric icon) + wordmark "Content Hub" in Geist Mono
- Below: tiny dim version tag `v2` in muted text
- Collapsed: logo mark only, centered

**Section label** — `PIPELINE` in 10px uppercase tracking-widest text-muted

**Pipeline nav items** — 5 stages in order:

Each item:
- Icon (20px, stage color) + Label (14px text-primary) + status dot (right-aligned)
- Status dot: hollow circle (idle) / animated amber pulse (running) / filled green (done)
- Hover: `bg-elevated` background, border-left 2px accent
- Active: `bg-elevated` + left border 2px stage-color + label in stage-color
- Collapsed: icon centered, no label, tooltip on hover

| # | Label | Icon | Color |
|---|-------|------|-------|
| 1 | Trends | `TrendingUp` | `#F5A623` |
| 2 | Research | `FlaskConical` | `#5B8DEF` |
| 3 | Ideation | `Lightbulb` | `#A855F7` |
| 4 | Hooks | `Zap` | `#EC4899` |
| 5 | Distribution | `Share2` | `#3DD68C` |

**Divider** — 1px `border` color, 16px horizontal margin

**Knowledge Brain nav item** — distinct section, not part of the numbered pipeline
- Icon: `Brain` (24px, `#06B6D4`)
- Label: "Knowledge Brain"
- Subtle glow on hover: `bg-elevated` with faint cyan border

**Divider**

**Bottom items**
- Settings (`Settings` icon, text-secondary)
- Collapse toggle (chevron icon, text-muted, rotates 180° when collapsed)

---

## 6. Dashboard — Landing View

The default view when the app loads. Active when no pipeline stage is selected.

### Page Header
- Title: "Dashboard" (24px, text-primary)
- Subtitle: today's date + "4 active stages" in text-secondary
- Right side: "New Video" button (accent fill, `Plus` icon)

### 4-Card Grid

**Layout:** 2×2 grid with 16px gap. Each card fills equal width. Cards are ~320px tall.

Each card shares the same anatomy:

```
┌─────────────────────────────────┐
│ [Stage Icon]  STAGE NAME   [→]  │  ← Card header (stage color icon, 
│ ──────────────────────────────  │    open button top-right)
│                                 │
│  Activity item 1    2h ago      │
│  Activity item 2    yesterday   │
│  Activity item 3    3 days ago  │
│                                 │
│ [Run Stage ▶]                   │  ← CTA button, stage color
└─────────────────────────────────┘
```

**Card details:**

**Trends card** (`stage-trends` accent)
- Icon: `TrendingUp` amber
- Recent activity: list of last 3 trending topics found, each with timestamp and a tiny topic pill (e.g. `#AITools`, `#Python`)
- CTA: "Run Trends" — amber outline button

**Research card** (`stage-research` accent)
- Icon: `FlaskConical` blue
- Recent activity: last 3 research brief titles, each with a source count badge (e.g. "12 sources")
- CTA: "Run Research" — blue outline button

**Ideation card** (`stage-ideation` accent)
- Icon: `Lightbulb` purple
- Recent activity: top 3 ideas from last session, shown as truncated titles with a relevance score bar (thin colored strip, 0–10)
- CTA: "Run Ideation" — purple outline button

**Outline card** (`stage-distribution` accent) — using Distribution green since outline feeds into distribution
- Icon: `FileText` green
- Recent activity: last 3 outline titles, each with a completion badge (e.g. "8 sections", "In Progress")
- CTA: "View Outlines" — green outline button

**Card hover state:** Slight `bg-elevated` lift, border changes from `border` to `border-active`, 150ms transition.

**Card running state:** Pulsing amber top border (2px), spinner icon replaces the `→` arrow in header.

---

## 7. Pipeline Stage Workspace

Activated when a sidebar nav item is clicked. Full main-content area replaces the dashboard.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  [←] Trends                                        [History]    │
│  Discover what's trending across AI, dev, and creator spaces    │
├─────────────────────────┬───────────────────────────────────────┤
│                         │                                       │
│   INPUT ZONE (40%)      │   OUTPUT ZONE (60%)                   │
│                         │                                       │
│   [Prompt textarea]     │   [Results render here]               │
│                         │                                       │
│   [Drop files here]     │                                       │
│                         │                                       │
│   [Paste a URL...]      │                                       │
│                         │                                       │
│   [▶ Run Trends]        │                                       │
│                         │                                       │
└─────────────────────────┴───────────────────────────────────────┘
```

### Stage Header (full width, above the split)
- Back arrow `←` returns to Dashboard
- Stage name (20px, 600, stage-color) + stage icon
- One-line description of what this stage does (text-secondary, 14px)
- Right: "History" button — opens a drawer/panel showing past runs for this stage

### Input Zone (left panel, 40%)

**Prompt textarea**
- Label: "What do you want to research?" (or stage-specific copy, see table below)
- Large textarea, min-height 120px, auto-grows
- Placeholder: stage-specific example prompt (see below)
- Styled: `bg-elevated`, `border`, focus ring in stage-color
- Bottom-right: character count in text-muted

**File drop zone**
- Dashed border rectangle, `bg-elevated`, `border` dashed
- Icon: `Upload` (24px, text-muted)
- Text: "Drop files here" / "or click to browse"
- Supported: `.md`, `.txt`, `.pdf`, `.docx` — shown as small pills below the zone
- After drop: file appears as a removable chip (filename + `×` button)

**URL input**
- Label: "Or paste a URL"
- Single-line input with `Link` icon prefix
- Styled: `bg-elevated`, `border`
- Supports multiple URLs (after Enter, URL becomes a chip, new input appears)

**Run button**
- Full width, stage-color fill
- Label: "Run [Stage Name]" with stage icon + `▶` 
- Loading state: spinner + "Running…" + disabled
- After completion: "✓ Done — View Results" with checkmark

**Per-stage prompt labels and placeholders:**

| Stage | Label | Placeholder |
|-------|-------|-------------|
| Trends | "What space should I trend-scan?" | "e.g. AI developer tools, productivity apps, LLMs" |
| Research | "What topic should I deep-research?" | "e.g. Why do AI tutorial videos go viral?" |
| Ideation | "Generate ideas based on:" | "e.g. Use my latest research brief, focus on beginner devs" |
| Hooks | "What is the video about?" | "e.g. How to build a local RAG system in 20 minutes" |
| Distribution | "What should I distribute?" | "e.g. Use the outline in my vault for my RAG video" |

### Output Zone (right panel, 60%)

**Empty state:** Centered illustration placeholder + "Run [stage] to see results here" in text-muted.

**Loading state:** Skeleton loader rows (3-4 animated shimmer blocks) — no spinner overlay.

**Results:**
- Rendered markdown output
- Monospace font for code blocks (`Geist Mono`)
- Top: result metadata bar — "Generated 2 min ago · 1,240 tokens · via Claude Sonnet" in text-muted small
- Top-right actions: `Copy` icon button, `Save to Vault` icon button, `Share` icon button
- Content scrolls independently from input zone

**History drawer** (slides in from right edge when "History" is clicked):
- List of past runs, most recent first
- Each entry: timestamp, prompt snippet (truncated), result word count
- Click an entry to reload it into the output zone

---

## 8. Knowledge Brain

Separate workspace, not part of the numbered pipeline. Accessible from sidebar.

### Purpose

Drop any piece of content — a video transcript, a competitor's article, a LinkedIn post, a Twitter thread — and get back a structured breakdown of **why it works**: the psychological hooks, structural choices, emotional triggers, and techniques a creator can steal and adapt.

### Layout

Full-width single-column layout (no split panel — this is analysis, not generation).

```
┌─────────────────────────────────────────────────────────────────┐
│  [Brain icon]  Knowledge Brain                                  │
│  Decode any content. Understand why it works.                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Paste content, drop a file, or enter a URL               │  │
│  │                                                          │  │
│  │ [Large text area — auto-grow]                            │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [Drop file]   [Paste URL]   [▶ Analyze]                        │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ANALYSIS RESULTS                                               │
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │ Hook Quality  │  │ Structure     │  │ Emotional     │       │
│  │     8.4/10    │  │ Score 7.9/10  │  │ Triggers: 5   │       │
│  └───────────────┘  └───────────────┘  └───────────────┘       │
│                                                                 │
│  [Full analysis rendered below — sections expandable]           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Input Area
- Large auto-growing textarea: "Paste the content you want to analyze…"
- Below the textarea: horizontal row — `[Drop a file]` `[Enter a URL]` `[▶ Analyze]`
- `[▶ Analyze]` uses `#06B6D4` (Brain cyan) as button color

### Results — 3 Summary Score Cards
Displayed horizontally after analysis completes:
- **Hook Quality** — score /10, with a thin cyan progress arc
- **Structure** — score /10
- **Emotional Triggers** — count of identified triggers

Cards: `bg-surface`, `border`, 12px radius, 16px padding.

### Results — Full Analysis
Collapsible sections, each with a `ChevronDown` toggle:

1. **Why It Works** — 2-3 paragraph plain-language explanation
2. **Hook Breakdown** — what the opening does in the first 30 seconds and why it holds attention
3. **Structure Map** — ordered list of content sections with a label for each (e.g. "Pattern interrupt", "Social proof", "CTA loop")
4. **Emotional Triggers** — chips for each trigger found (e.g. `Fear of Missing Out`, `Aspiration`, `Curiosity Gap`)
5. **Techniques to Steal** — 3-5 bullet points, each actionable and specific
6. **Replication Template** — a skeleton outline the user can take directly into /hooks or /outline

---

## 9. Micro-interactions & Motion

- **Page transitions:** 150ms fade between views — no slide animations (they feel slow)
- **Sidebar collapse:** 200ms cubic-bezier ease for width change
- **Button hover:** 80ms background shift
- **Card hover:** 100ms border color + subtle `translateY(-1px)` lift
- **Running state pulse:** amber dot, 1.5s ease-in-out infinite
- **Skeleton loaders:** shimmer left-to-right, 1.2s, no jitter
- **Toast notifications:** slide in from bottom-right, auto-dismiss 4s, can be dismissed early

---

## 10. Responsive Behavior

The app is **desktop-first**. The sidebar is always visible at ≥1200px.

- **1200px–1440px:** Default layout. Sidebar collapsed by default.
- **1440px+:** Sidebar expanded by default. Input/Output panels at 40/60.
- **<1200px:** Sidebar becomes a bottom sheet or hamburger. Not a primary concern for v1.

---

## 11. Empty & Loading States Summary

| View | Empty state | Loading state |
|------|-------------|---------------|
| Dashboard cards | "No activity yet — Run [stage] to start" | Skeleton card with shimmer |
| Stage output | Centered icon + "Run [stage] to see results" | 3–4 shimmer rows |
| History drawer | "No past runs yet" | Skeleton list items |
| Brain results | Centered brain icon + "Drop content to analyze" | Score card skeletons + shimmer analysis rows |

---

## 12. Key Screens to Design

1. **Dashboard** — 4-card grid, sidebar expanded, one card in "running" state
2. **Research workspace** — input zone with a URL chip added, output zone showing rendered markdown result
3. **Hooks workspace** — file chip in drop zone, output showing 5 hook variations as numbered cards
4. **Knowledge Brain** — analysis complete, score cards visible, "Structure Map" section expanded
5. **Sidebar collapsed** — icon-only mode, hover tooltip visible on "Ideation" item
6. **Mobile / narrow** — sidebar as bottom sheet (stretch goal)

---

## 13. Copy / Language Conventions

- Stage names are title-case: **Trends, Research, Ideation, Hooks, Distribution**
- Buttons use verb + noun: "Run Research", "Analyze Content", "Save to Vault"
- Error messages: specific and actionable — "No URL detected. Paste a full URL starting with https://"
- Empty states: encouraging, not apologetic — "Drop anything here to decode it"
- Timestamps: relative — "2h ago", "yesterday", "3 days ago"

---

*This document is the handoff spec for the Content Hub V2 web app. Design should follow this spec for layout, component structure, and personality. Visual polish (exact shadows, gradient treatment, icon sizing tweaks) is at the designer's discretion within the palette and tone defined here.*
