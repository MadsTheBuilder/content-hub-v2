---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 04-cascade-tab-agent
task: Create CascadeTab.jsx — vault mode (research_file + outline_file) or URL mode (youtube_url); renders bundle via OutputBrowser.
description: "CascadeTab: mode toggle vault/url, pickers for 10-Research and 06-Outlines, or YouTube URL input; posts to /api/pipeline/cascade; renders 08-Distribution bundle."
tags: [phase5, cascade, distribution, webapp-sprint]
owned_files:
  - Design-doc/web/src/DistributionTabs/CascadeTab.jsx
verification:
  - Bundle output opens primary_path by default
  - Vault mode body is { research_file, outline_file }
  - URL mode body is { youtube_url }
  - Result resolves to 08-Distribution bundle
  - No raw fetch
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 04-CascadeTab

## Self-Verification

- [x] Mode toggle: `vault` (research + outline pickers) vs `url` (YouTube URL input). Both modes mutually exclusive — user fills one at a time.
- [x] Vault body: `{ research_file, outline_file }`.
- [x] URL body: `{ youtube_url }`.
- [x] `OutputBrowser result={jobResult}` opens `primary_path` by default (bundle behaviour built into OutputBrowser).
- [x] No raw `fetch`.

## Open Items

None.
