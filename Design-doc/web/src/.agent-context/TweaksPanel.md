---
title: TweaksPanel Vite Port Context
date: 2026-05-23
description: Ported TweaksPanel from CDN React globals to Vite + React 19.2.6 with localStorage persistence replacing postMessage. Includes useTweaks hook and all UI controls. Ready for App.jsx integration.
tags: [frontend, react, component-porting, localStorage, architecture]
---

# TweaksPanel Porting Context

## Summary
Ported `Design-doc/Content Hub/tweaks-panel.jsx` from CDN globals to [[Local_First_Skill_Engine_Plan|Vite + React 19.2.6]] with full localStorage replacement of postMessage persistence. Part of the [[design-doc/web]] frontend modernization.

## useTweaks Hook Signature
```js
export function useTweaks(defaults)
// Returns: [values, setTweak]
// - values: object containing all tweak values (hydrated from localStorage or defaults)
// - setTweak: function(keyOrEdits, val?) => void
```

**Behavior:**
- On mount: reads all keys from localStorage with prefix `tweak:` and merges with defaults
- On `setTweak(key, value)`: writes to localStorage immediately, updates state, emits CustomEvent
- On `setTweak({ ...edits })`: batch-writes all keys to localStorage, updates state

## localStorage Keys
- `tweak:{keyName}` — individual tweak values (JSON-serialized)
- `tweak:__panel_open` — panel visibility state (boolean)

**Example:**
```js
const DEFAULTS = { fontSize: 16, primaryColor: '#D97757' };
const [t, setTweak] = useTweaks(DEFAULTS);
// Reads localStorage('tweak:fontSize') and localStorage('tweak:primaryColor')
setTweak('fontSize', 18);
// Writes localStorage('tweak:fontSize', '18') and updates state
```

## Removed postMessage Events
1. **Client → Host (now gone):**
   - `window.parent.postMessage({ type: '__edit_mode_set_keys', edits }, '*')` — replaced with localStorage
   - `window.parent.postMessage({ type: '__edit_mode_available' }, '*')` — no host in Vite, removed
   - `window.parent.postMessage({ type: '__edit_mode_dismissed' }, '*')` — replaced with localStorage

2. **Host → Client (now gone):**
   - `addEventListener('message', ...)` for `__activate_edit_mode` / `__deactivate_edit_mode` — replaced with localStorage

## Preserved Behaviors
- `window.dispatchEvent(new CustomEvent('tweakchange', ...))` — kept for same-window listeners
- All UI controls (slider, toggle, radio, color, etc.) unchanged
- Drag behavior, viewport clamping, scrolling all preserved
- Styling (`.twk-*` classes) fully preserved

## Self-Verification Result
**PASS**
- [x] File exists and is not empty
- [x] React hooks imported: `import { useState, useCallback, useEffect, useRef }`
- [x] `useTweaks` is named export: `export function useTweaks(defaults)`
- [x] Reads from localStorage: `localStorage.getItem('tweak:${key}')` (5 instances)
- [x] Writes to localStorage: `localStorage.setItem('tweak:${key}', JSON.stringify(value))` (multiple instances)
- [x] Zero `postMessage` calls
- [x] Zero `addEventListener('message'` calls
- [x] Zero `window.React` or CDN patterns
- [x] Default export: `export default TweaksPanel`

## Export Deduplication
**Status: VERIFIED (2026-05-23)**
- Confirmed: `useTweaks` is exported exactly once (inline at line 116: `export function useTweaks(defaults)`)
- No duplicate `export { useTweaks }` block found in file
- No barrel re-exports of `useTweaks` in the export block (lines 469–473)
