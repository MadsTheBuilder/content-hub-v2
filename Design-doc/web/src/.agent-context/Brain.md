---
tags: [component, port, vite, react]
status: complete
date: 2026-05-23
description: Brain component ported from CDN React to Vite + React 19.2.6 with URL/file-drop features stripped per locked decision #8. Pasted-text textarea only. All 11 verification checks passed. Implements analysis workflow with expandable results panels and loading states.
---

# Brain Component - Vite + React 19.2.6 Port

**Related:** [[Local_First_Skill_Engine_Plan]], [[locked-decision-8]]

## Self-Verification Result: PASS

All 11 verification checks completed successfully.

---

## Stripped Features

The following state variables and UI blocks were removed from the CDN prototype:

### State Variables Removed:
- `urls` — array of stored URLs/links
- `urlDraft` — temporary URL input field state

### Handler Functions Removed:
- `handleUrlKey()` — Enter key handler for URL input

### JSX Blocks Removed:
- URL chips display (lines 58-70 in original) — rendered list of URL badges with delete buttons
- URL input row (lines 73-83 in original) — text input field with Icon.Link prefix
- "Drop a file" button (line 72 in original) — upload trigger button
- File-drop zone handlers — `onDrop`, `onDragOver`, `onDragEnter`, `onDragLeave` (none present in cleaned version)

### Label Text Updated:
- Changed from: "Paste content, drop a file, or enter a URL"
- Changed to: "Paste content to analyze"

---

## Kept Components

### Core Functionality:
- **Main textarea** (line 45) — `<textarea>` for pasting text content with onChange handler
- **Character counter** (line 52) — displays prompt length
- **Run Analysis button** (line 55) — calls `handleAnalyze()` with loading state
- **Loading spinner** (lines 56-68) — Icon.Loader with "Analyzing…" text during runState="loading"

### Result Display:
- **BrainSkeleton** — skeleton loaders while analyzing
- **BrainResults** — 6 analysis sections with expandable/collapsible content
- **ScoreCard** — circular progress indicators for Hook Quality, Structure, Emotional Triggers
- **AnalysisSection** — collapsible panels for Why It Works, Hook Breakdown, Structure Map, Emotional Triggers, Techniques, Template
- **StackedPanel** + **SourcesPanel** — flipped card display for results and sources

### State Management:
- `prompt` — textarea content state
- `runState` — "idle" | "loading" | "done" lifecycle
- `openSections` — collapsible section toggle state (object keyed by section index)
- `toggle()` — function to flip section open/closed

---

## Imports

```javascript
import { useState } from 'react';
import Icon from './Icons';
import StackedPanel from './StackedPanel';
import SourcesPanel from './SourcesPanel';
```

All imports are ESM syntax. No CDN `window.X` globals. No `const { ... } = React` destructure.

---

## File Structure

- **Brain** (main export) — wrapper component with state and layout
- **BrainSkeleton** — loading placeholder
- **BrainResults** — analysis results container
- **ScoreCard** — progress circle component (reusable)
- **AnalysisSection** — expandable content panel (reusable)

---

## Export

`export default Brain` on line 289 — enables `import Brain from './Brain'` in consumer code.
