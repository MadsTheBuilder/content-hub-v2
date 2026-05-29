---
date: 2026-05-21
type: outline
topic: "Content Hub V2 — Full System Demo"
platform: yt-long
target_length: "8-10 min"
hook_pattern: "Pain Point Agitation + Speed to Value"
description: "Rewritten Dopamine Ladder outline for the Content Hub V2 demo video. Replaces the raw stream-of-consciousness walkthrough scored at 23/100."
tags: [content-hub-v2, dopamine-ladder, kallaway, demo-video]
---

# Outline: Content Hub V2 — System Demo (Rewrite)

**References:** [[hook_prompts]] · [[outline_prompts]] · [[voice_profile]] · [[2026-05-21_Video_Audit_ContentHub_Demo]]

---

## [Stage 1: Stimulation] — 0:00–0:30

**Dopamine Goal:** Stimulation  
**Kallaway Pattern:** Pain Point Agitation (#9) + Speed to Value (#3)

**Spoken Line (0:00–0:03):**
> "Most YouTube creators spend 4 hours on research and scripting. I cut that to 20 minutes — and my hooks are now trained on Kallaway."

**Setup (0:03–0:15):**
> "Seven slash commands in Claude Code. You point it at GitHub trending repos. It researches, writes your hook, builds your outline, titles the video, distributes it across platforms, and writes your short-form scripts — in sequence, automatically."

**Promise (0:15–0:30):**
> "I'm going to show you the whole thing, why it actually works, and the one part that breaks everything if you skip it."

**Visual Cue:** Split screen — timer showing "4 hrs" on left vs "20 min" on right. Hook output appears on right side as text.  
`[TEXT OVERLAY: "7 Commands. Research → Script. 20 Minutes."]`

---

## [Stage 2: Captivation] — 0:30–2:00

**Dopamine Goal:** Captivation

**Talking Points:**
- Every AI writing tool gives you generic output. ChatGPT doesn't know Kallaway. Claude by default gives you opening statements, not hooks.
- Show the contrast immediately: ask raw Claude for a hook → get "I spent three months building a pipeline. I found 10 skills that mattered." That's a recap, not a hook.
- Run `/hook` → get: "These 10 skills are the difference between Claude Code being a cool toy and being the best hire you've ever made." 5 variations, each labelled with a Kallaway pattern, each with the psychological reason it works.
- Stakes: if your hook fails, the video is dead before the first edit. The hook is where 80% of watch time is decided.

`[SHOW SCREEN: Side-by-side — raw Claude response vs /hook output]`

**Transition to Stage 3:**
> "But the hook is step 3 of 7. Let me show you what has to happen first — because this is where most people would build this wrong."

---

## [Stage 3: Anticipation] — 2:00–3:30

**Dopamine Goal:** Anticipation

**Talking Points:**
- Most people when they automate YouTube content start with the script. Wrong starting point.
- You need research first — real research. Not "summarize this topic." Research that shows you what's *missing* from the internet right now.
- Step 1: point the researcher at GitHub trending. Top 5 this week, top 10 this month. It runs through NotebookLM and comes back with a gap analysis — not just what's trending, but what no one is making videos about yet.

`[SHOW SCREEN: GitHub trending page → researcher running → vault output file opening]`

**Head Fake #1:**
> "You'd think this research step is the most impressive part of the system. It's not. The part that impressed me is what I found when I compared the AI writing hooks *with* this research versus *without* it — same model, completely different outputs."

**Transition to Stage 4:**
> "Here's the full pipeline, step by step — and I'll show you each one live."

---

## [Stage 4: Validation] — 3:30–7:00

**Dopamine Goal:** Validation

**Talking Point 1 — The hook comparison (the "wow" demo):**
- `[SHOW SCREEN: Claude CLI — raw hook request typed live]`
- "No skill. I say: write me a hook for a video about top 10 Claude Code skills. Output." Read it aloud. "That's an opening statement."
- `[SHOW SCREEN: Run /hook — watch it invoke hooks.md]`
- "Now with the skill. It reads hooks.md — which contains all 10 Kallaway patterns, the Dopamine Ladder opening stages, banned openers, retention rules. Output." Read the top variation. Show the pattern label and the psychological 'Why' underneath.
- "The system doesn't just write a hook. It tells you *why* that hook works and *what it's promising* — so you can't accidentally over-promise in the hook and under-deliver in the video."

**Talking Point 2 — The full pipeline, fast:**
- `[SHOW SCREEN: Obsidian vault folder tree — pre-navigated, clean]`
- `/outline` → 6-stage Dopamine Ladder. Each section has a duration target, talking points, visual cues, head fakes pre-marked.
- `/title` → 10 options. Experimental ones flagged. Thumbnail text for each.
- `/cascade` → once your video is recorded, it distributes: LinkedIn post, Instagram deck, platform-specific formats.
- `/short-form` → 30, 60, 90-second script versions from the same outline.
- `/voice-cleanup` → runs every output through your voice profile.

**Talking Point 3 — Voice profile (the part that breaks everything if skipped):**
- `[SHOW SCREEN: voice_profile.md]`
- "This is what stops the output from sounding like AI. Banned words: 'crucially,' 'furthermore,' 'tapestry.' My cadence: punchy, one idea at a time, direct. It cleans every output against this. Skip it and every script sounds the same — and sounds like AI."

**Head Fake #2:**
> "You're probably thinking: this is just prompt engineering stacked on prompt engineering. It's not. The architecture is the actual point — and it's why this scales when a single giant system prompt wouldn't."

`[SHOW SCREEN: Skill anatomy diagram — SKILL.md + .py file + prompt.md]`

- "Every skill is three files. SKILL.md is the Claude Code entry point — what triggers when you type the slash command. The Python file runs the actual logic in the background — no token waste, no context contamination. The prompt.md is the single source of truth. Kallaway lives in hooks.md. The Dopamine Ladder lives in outline.md. They're versioned files you can read, update, and swap."

**Transition to Stage 5:**
> "Now I want to tell you *why* I actually built this — because it's not the reason you'd expect."

---

## [Stage 5: Affection] — 7:00–8:00

**Dopamine Goal:** Affection

**Talking Points:**
- "I know myself. I get excited about things for 3-4 years and then I want to move on. Automation means when I'm done being excited, the system still runs."
- "I'm not building a media company. I'm building a machine that makes content while I figure out what I want to do next. That feels more honest than pretending I want to be a full-time creator forever."
- "The part that surprised me building this: the research and hook generation were straightforward. The hard part was voice. Getting the AI to not sound like AI took longer than everything else combined. The voice profile is the most underrated piece."

`[Talking head — no screen share here]`

**Transition to Stage 6:**
> "And that surprised me enough that it changed how I think about AI content systems in general."

---

## [Stage 6: Revelation] — 8:00–8:45

**Dopamine Goal:** Revelation

**Talking Points:**
- "Nobody talks about this when they say 'automate your YouTube channel': the bottleneck was never production. It was decision fatigue. Which topic? Which hook? Which title? Every one of those decisions drains you before you even open a camera."
- "This system doesn't make those decisions for you. It gives you 5 hooks — you pick one. It gives you 10 titles — you pick one. The automation isn't about removing your judgment. It's about removing the blank page. You only ever *respond*. You never *generate from nothing*."

`[TEXT OVERLAY: "Automation removes the blank page. Not your judgment."]`

---

## [CTA] — 8:45–9:15

**Goal:** Give them a specific next action, not a generic subscribe ask.

**Talking Points:**
- "If you want to build something like this, the next video covers the architecture in detail — how to wire a Python skill to a prompt file in Claude Code, and why the three-layer pattern matters when you want to swap models."
- "The full hooks.md — 10 Kallaway patterns, Dopamine Ladder, retention rules — is in the repo linked below."

`[TEXT OVERLAY: repo link]` · `[End screen: next video card]`

---

**Write only from this outline. Do not read it verbatim — speak from the points. Film Stage 5 in one take, talking head only.**
