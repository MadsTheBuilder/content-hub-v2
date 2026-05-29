---
created: 2026-05-23
modified: 2026-05-23
date: 2026-05-23
type: frontend-assembly
status: complete
tags: [vite, react, app-root, view-routing, state-management]
description: Root component assembly for Content Hub V2 Vite app. Implements view routing, tweaks state management via useTweaks hook, sidebar/main layout, and per-view accent colors. Integrates Dashboard, StageWorkspace, Brain, and Settings sub-components.
---

# App.jsx Assembly

Assembly of full Vite app root component from Group 1 sub-components. Implements complete view routing, state management via [[TweaksPanel]], and per-view ambient accent colors.

## Full Import List
- `useState`, `useEffect` from 'react'
- `useTweaks` (named) from './TweaksPanel.jsx'
- `Dashboard` (default) from './Dashboard.jsx'
- `Sidebar` (default) from './Sidebar.jsx'
- `StageWorkspace` (default) from './StageWorkspace.jsx'
- `TweaksPanel` (default) + `TweakSection`, `TweakColor`, `TweakRadio`, `TweakToggle`, `TweakSelect` (named) from './TweaksPanel.jsx'
- `Brain` (default) from './Brain.jsx'

## View Routing
State variable: `view` (initialized from `t.view || "dashboard"`)
Routes handled:
- `"dashboard"` → Dashboard
- `"trends"` → StageWorkspace with stageId="trends"
- `"research"` → StageWorkspace with stageId="research" + initialState (prompt + URL)
- `"ideation"` → StageWorkspace with stageId="ideation"
- `"hooks"` → StageWorkspace with stageId="hooks" + initialState (prompt + file)
- `"title"` → StageWorkspace with stageId="title" + initialState (prompt + file)
- `"outline"` → StageWorkspace with stageId="outline" + initialState (prompt + 2 files)
- `"distribution"` → StageWorkspace with stageId="distribution"
- `"brain"` → Brain
- `"settings"` → SettingsPlaceholder

Navigation via `navigate(v)` function which updates both view state and localStorage via `setTweak("view", v)`.

## useTweaks Hook Call
```javascript
const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
```

TWEAK_DEFAULTS structure:
```javascript
{
  "accent": "#5B8DEF",
  "view": "dashboard",
  "sidebarCollapsed": false,
  "density": "comfortable"
}
```

useTweaks returns:
- `t`: object with all current tweak values (hydrated from localStorage with fallback to defaults)
- `setTweak(key, value)`: function that updates state + persists to localStorage with `tweak:` prefix

## Per-View Accent Logic
CSS variable `--page-accent` is set via useEffect based on current view:
- dashboard, brain → #06B6D4 (cyan)
- trends → #F5A623 (orange)
- research → #5B8DEF (indigo)
- ideation → #A855F7 (purple)
- hooks → #EC4899 (pink)
- title → #F97316 (orange-red)
- outline → #14B8A6 (teal)
- distribution → #3DD68C (green)
- settings → user's selected accent (t.accent)
- default fallback → t.accent

Also applies:
- `--accent` CSS variable from user tweak
- `--main-pad` CSS variable based on density ("compact" vs "comfortable")

## Self-Verification Result
**PASS** — All 13 checklist items verified:
1. useState, useEffect imports present
2. useTweaks named import from TweaksPanel
3. Dashboard default import
4. Sidebar default import
5. StageWorkspace default import
6. TweaksPanel default + named exports from TweaksPanel
7. Brain default import
8. export default App at end
9. File is 200 lines (not stub)
10. Zero CDN patterns
11. Particle bootstrap present in useEffect
12. TWEAK_DEFAULTS in App.jsx (not moved)
13. View routing + per-view accent logic both present

No issues found or fixed. Assembly complete.
