---
date: 2026-05-19
type: session_summary
description: "Built and ran a NIM-managed NotebookLM test pipeline for YouTube video glAoiBWVkmU (Claude Code + Obsidian Command Center)."
tags: [nim, notebooklm, pipeline, test-run]
---

# Session: NIM-Managed NotebookLM Pipeline — Test Run

Implements: [[NIM Full Pipeline Takeover]] | Modifies: [[scratch/test_pipeline_glAoiBWVkmU.py]]
Adds: [[scratch/resume_pipeline_video.py]], [[10-Research/pipeline-test-glAoiBWVkmU/]]
References: [[2026-05-15_NIM_Full_Pipeline_Takeover]]

## What Was Done

Built a two-phase pipeline script that uses NIM as the orchestrator and notebooklm-py for execution.

### Architecture

```
Phase 1: NIM (meta/llama-3.3-70b-instruct)
  → generates context-aware prompts for 4 artifacts (nim_prompts.json)

Phase 2: notebooklm-py
  → create notebook, add YouTube source
  → implementation report (ReportFormat.CUSTOM + NIM prompt)
  → brief report (ReportFormat.CUSTOM + NIM prompt)
  → slide deck (PPTX for manual gold/aluminum/red restyling)
  → explainer video (VideoFormat.EXPLAINER + VideoStyle.WHITEBOARD)

Phase 3: NIM
  → writes pipeline management summary (pipeline_management_summary.md)
```

### Files Produced

| File | Status |
|------|--------|
| `nim_prompts.json` | ✓ — NIM-generated prompts for all 4 artifacts |
| `implementation_report.md` | ✓ — Technical report, 6 sections, bullet points |
| `brief_report.md` | ✓ — Executive brief, 5 sections, bullets only |
| `slide_deck.pptx` | ✓ — 7.2MB PPTX (apply gold/aluminum/red theme manually) |
| `explainer_video.mp4` | Generating (resume_pipeline_video.py running) |
| `pipeline_management_summary.md` | Pending NIM write after video completes |

### Scripts

- `scratch/test_pipeline_glAoiBWVkmU.py` — full pipeline (NIM orchestrator + notebooklm-py)
- `scratch/resume_pipeline_video.py` — targeted resume: video + NIM summary

### Key Design Decisions

- **NIM generates all prompts upfront** — one call returns JSON with all 4 artifact instructions; used as `custom_prompt` / `instructions` in notebooklm-py calls
- **PPTX not PDF for slide deck** — API doesn't support color themes; PPTX allows manual gold/aluminum/red restyling in PowerPoint/Google Slides
- **VideoStyle.WHITEBOARD** — no characters, text/diagrams animate in as topics are covered; closest to user's spec
- **Sequential generation** — avoids NotebookLM rate limits; each step waits before the next begins
- **artifact_id on every download** — prevents the second report download from grabbing the first report

### Alignment with Existing NIM Integration

Session [[2026-05-15_NIM_Full_Pipeline_Takeover]] already moved all pipeline LLM calls to NIM cascade (NIM → Gemini → Ollama). This session extends that pattern to the NotebookLM pipeline layer, making NIM the orchestrator for notebooklm-py artifact generation too.

## Open Items

- Video generation still running (resume_pipeline_video.py) — monitor completion
- NIM management summary will be written after video completes
- PPTX needs manual colour theming (gold, aluminium grey, deep red)
- Consider converting these two scripts into a proper `/yt-pipeline` or `/notebooklm-pipeline` skill for reuse
