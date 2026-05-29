---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 06-voice-cleanup-tab-agent
task: Create VoiceCleanupTab.jsx — folder selector + VaultPicker across 7 output folders, inplace toggle, posts { file_path, inplace }.
description: "VoiceCleanupTab: folder selector (02/05/06/07/08/09/10), VaultPicker for concrete file, inplace checkbox, posts { file_path, inplace } to /api/pipeline/voice-cleanup."
tags: [phase5, voice-cleanup, distribution, webapp-sprint]
owned_files:
  - Design-doc/web/src/DistributionTabs/VoiceCleanupTab.jsx
verification:
  - Request body is { file_path, inplace }
  - inplace true returns original path
  - inplace false returns _cleaned sibling path preview
  - No raw fetch
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 06-VoiceCleanupTab

## Self-Verification

- [x] `VOICE_FOLDERS` covers all 7 approved source folders.
- [x] Folder selector drives `VaultPicker` — changing folder resets `filePath` to null.
- [x] Body: `{ file_path: filePath, inplace }`.
- [x] `inplace: true` → resolver returns original `file_path`.
- [x] `inplace: false` → resolver returns `_cleaned` sibling; UI previews path.
- [x] No raw `fetch`.

## Open Items

None.
