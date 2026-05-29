---
date: 2026-05-27
tags: [session, design-doc, frontend]
description: "Rewrote systems-deck.html to V2 design system theme; created graph.html interactive D3.js force-directed system graph."
---

# Session: Design Doc Theme Rewrite + System Graph

Implements: [[Design_Doc_Web_App_Plan]]
Modifies: [[Design-doc/systems-deck.html]], [[Design-doc/graph.html]]

## What Changed

### `Design-doc/systems-deck.html` — Full theme rewrite

Replaced the old Cormorant Garamond / DM Mono / dark-teal aesthetic with the V2 design system tokens extracted from [[Design-doc/web/src/styles.css]].

- **Fonts**: Inter (100–700) + JetBrains Mono replace Cormorant Garamond + DM Mono + Lora
- **Root variables**: Same names kept (`--bg`, `--surface`, `--green`, `--blue`, etc.); values updated to V2 palette (`#0D0F12` base, `#5B8DEF` accent, `#3DD68C` green, `#06B6D4` cyan, `#A855F7` purple, `#F5A623` amber, `#E5534B` red)
- **Per-slide ambient glow**: `data-accent` attribute on each slide; JS sets `--page-accent` CSS var on navigation; `.slide` background uses `radial-gradient(..., color-mix(in oklab, var(--page-accent) 14%, transparent) ...)` for live ambient recolor
- **Ghost numerals**: Inter weight 100 (replaces Cormorant Garamond weight 300)
- **Layer colors**: `.layer.ls` (Skill) → `--purple`; `.layer.lv` (Vault) → `--green`
- **Bug fix**: `.cn` class used for both cascade provider divs (slide 5) and skill name spans in `.cov-item` (slide 8) — override rule added to fix visual clash

Per-slide accents: s1=#5B8DEF, s2=#06B6D4, s3=#3DD68C, s4=#14B8A6, s5=#5B8DEF, s6=#F5A623, s7=#E5534B, s8=#A855F7, s9=#3DD68C, s10=#06B6D4

### `Design-doc/graph.html` — New file

Interactive D3.js v7 force-directed system graph of the Content Hub V2 architecture. Same V2 design system (Inter + JetBrains Mono, `#0D0F12` bg, `--r-card: 12px`).

**29 nodes**, 6 types:
- `human` (1): You
- `skill` (8): /researcher, /hook, /ideation, /title, /outline, /cascade, /short-form, /voice-cleanup
- `python` (5): researcher.py, cascade.py, voice_cleanup.py, utils/ai.py, pipeline.py
- `deterministic` (2): nlm_seed.py, yt_pipeline.py
- `ai` (3): Claude CLI, NIM, Ollama
- `vault` (9): vault root, research/, hooks/, ideation/, titles/, outline/, 08-Dist/, raw/, cleaned/

**40 directed edges**, 6 link types: flow, human, uses, calls, writes, reads — each with distinct color, opacity, dash pattern.

**Interactions**:
- Click node → focus mode (dims non-connected, shows info panel with connections list)
- Hover → glow
- Legend → toggle type visibility
- Zoom/pan + drag nodes
- Arrowheads positioned at circle boundaries (not centers)

## Files Touched

- `Design-doc/systems-deck.html` — full CSS rewrite (HTML untouched)
- `Design-doc/graph.html` — new file

## Open Items

- Vault output folder structure refactor still pending (raw/cleaned subfolders in `08-Dist/`) — tracked in [[project_vault_output_folder_structure]]
- Phase 7 (launch convenience + E2E) of [[Webapp_sprint]] still next
