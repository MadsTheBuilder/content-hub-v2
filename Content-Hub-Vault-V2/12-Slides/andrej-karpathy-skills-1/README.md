---
date: 2026-05-20
notebook_id: 78cda845-af9a-4c55-9166-80595d98a719
slug: andrej-karpathy-skills-1
status: partial
---

# Studio Slides — Andrej Karpathy Skills (Run 1)

Step 9 of the [[Refined_Pipeline]] — slide deck + video generation.

## Artifacts

| File | Status | Notes |
|------|--------|-------|
| `blog_deck.pdf` | ✅ | "The Architecture of Simplicity" |
| `linkedin_deck.pdf` | ✅ | "Radical Simplicity in AI" |
| `instagram_deck.pdf` | ❌ missing | Submission returned no task_id (rate limit) |

## Video

| File | Status | Notes |
|------|--------|-------|
| `13-Video/andrej-karpathy-skills-1/linkedin_video.mp4` | ❌ missing | Timed out at 900s in `pending` state; user stopped generation |

## Outstanding

- Re-run instagram deck + video when NLM quota resets
- Both can be retried standalone via `studio.inject_cascade_and_generate()` or the targeted retry script used in this session
