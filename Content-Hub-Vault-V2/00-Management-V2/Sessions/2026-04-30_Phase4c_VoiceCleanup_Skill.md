---
date: "2026-04-30"
session: "Phase 4c — Voice Cleanup Skill"
status: Complete
---

# Session Log: Phase 4c — `/voice-cleanup`

Implements: [[Phase4c_VoiceCleanup]]
References: [[Architecture_Building]] | [[voice_profile]] | [[2026-04-29_Phase4a_Cascade_Skill]] | [[2026-04-29_Phase4b_ShortForm_Skill]]
Modifies: [[skills/voice_cleanup.py]] | [[prompts/voice_cleanup.md]] | [[.claude/skills/voice-cleanup/SKILL.md]]

---

## What Was Done

Built the `/voice-cleanup` skill — the third and final Phase 3 (distribution) skill. De-AI'ifies any output from `/cascade` or `/short-form` before the human review + publish step.

### Files Created

| File | Purpose |
|------|---------|
| `prompts/voice_cleanup.md` | Prompt template — consolidated banned list, positive voice markers, rewrite rules. `{text}` placeholder. |
| `skills/voice_cleanup.py` | Python runner — accepts file path arg or stdin. Routes to Claude via `polish()`. Saves `_cleaned.md` beside original. |
| `.claude/skills/voice-cleanup/SKILL.md` | Slash command entry — covers file mode, stdin mode, and common post-cascade workflow. |

### Voice Profile Assessment (done this session)

The `voice_profile.md` is solid in structure but had two gaps relevant to this skill:

1. **Incomplete banned list** — cascade/short_form prompts blocked `leverage`, `cutting-edge`, `unleash`, `seamless`, `robust`, `paradigm shift`, `it's worth noting`, `as we navigate` but these were absent from the voice_profile itself. All consolidated into `prompts/voice_cleanup.md`.
2. **No positive voice markers** — the profile described what NOT to do but not what TO use. Extracted from the authentic voice examples: `"the reason for that is simple"`, `"the beauty of X is"`, lowercase casual connectors, plain opinionated takes. Embedded in the prompt.

The voice_profile.md was **not modified** — these additions live in the cleanup prompt only. If the voice_profile needs patching, that's a separate ask.

### Design Decisions

- **Claude-first routing** (`polish()`) — voice cleanup is premium polish work, not a drafting task. Gemini fallback available if Claude CLI fails.
- **Non-destructive output** — saves `{stem}_cleaned.md` beside original. `--inplace` flag available but gated behind explicit user ask in SKILL.md.
- **Stdin fallback** — skill works without a file path for ad-hoc paste-in text, matching the "pasted AI text in" smoke test requirement.

---

## Open Items

- Voice profile itself could be enriched with the consolidated banned list and positive markers — worth doing once a few more cleanup runs have validated the prompt. Not blocking anything.
- Next up: [[Phase2_Ideation_Skill]] (`/ideation`)
