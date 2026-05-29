---
date: 2026-05-21
type: script
topic: "Content Hub V2 — Full System Demo"
platform: yt-long
target_length: "8-10 min"
description: "Full word-for-word spoken script for the Content Hub V2 demo video. Written in voice profile. Follows the Dopamine Ladder outline."
tags: [content-hub-v2, script, dopamine-ladder, kallaway]
---

# Full Script: Content Hub V2 — System Demo

**References:** [[2026-05-21_Content-Hub-V2-Demo-Rewrite]] · [[voice_profile]] · [[hook_prompts]] · [[outline_prompts]]

*Production note: `[brackets]` = visual direction. Speak naturally from this — don't read it verbatim. Stage 5 is the one place to go fully off-script.*

---

## [Stage 1: Stimulation] — 0:00–0:30

`[COLD OPEN — no intro music, no title card. Jump straight in. Talking head, direct camera.]`

Most creators spend 4 hours on research and scripting.

I cut that to 20 minutes.

And the hooks this system writes? Trained on Kallaway.

`[TEXT OVERLAY: "7 Commands. Research → Script. 20 Minutes."]`

Here's what it does. Seven slash commands inside Claude Code. You point it at GitHub trending repos. It researches the topic, writes your hook, structures the full video, titles it, distributes it across platforms, and turns it into short-form scripts — in that exact order, one step triggering the next.

I'm going to show you the whole pipeline, how it snowballs, and the one piece that breaks everything if you skip it.

---

## [Stage 2: Captivation] — 0:30–2:00

`[SHOW SCREEN: Claude CLI — clean terminal, nothing typed yet]`

Let me show you the hook part first because this is what actually changes your output.

You go to raw Claude — no skill, no system, nothing — and you type: *"Write me a hook for a video about the top 10 Claude Code skills."*

Here's what you get back.

`[SHOW SCREEN: Raw Claude response]`

*"I spent three months building a full content production pipeline with nothing but Claude Code. In that time I found 10 skills that actually mattered. Skip the rest."*

That is not a hook. That is an opening statement. A recap. There's no scroll-stop in there. No curiosity loop. No reason for someone who just landed on your video to stay.

Claude doesn't know Kallaway. ChatGPT doesn't know Kallaway. Any model you throw at this will give you the same thing — technically correct, completely forgettable.

Now watch what happens when the skill runs.

`[SHOW SCREEN: Type /hook in Claude Code — watch it invoke]`

Same model. Same topic.

`[SHOW SCREEN: /hook output — 5 variations, pattern labels visible]`

*"These 10 skills are the difference between Claude Code being a cool toy and being the best hire you've ever made."*

Look at what's underneath that. Pattern name. Why it stops the scroll. What it's promising the viewer. Visual cue. Text overlay. Five variations total, each using a different Kallaway framework.

The system doesn't just write the hook. It tells you why the hook works and exactly what you're committing to deliver. That's the thing — you can't promise something in the hook and not deliver it in the video. The skill makes that impossible to miss.

That's step 3. Let me show you what has to happen before you even get there — because this is where most people would build this wrong.

---

## [Stage 3: Anticipation] — 2:00–3:30

`[SHOW SCREEN: GitHub trending page — pre-navigated, top repos visible]`

Most people when they think about automating content, they start with the script. Wrong move.

The script has nothing to stand on if the research isn't there first.

Step one is the researcher. You point it at GitHub trending — top 5 repositories of the last 7 days, top 10 of the last 30. That's your raw feed. That's what the developer world is actually building right now, this week, this month.

`[SHOW SCREEN: /researcher running in Claude Code]`

The researcher pulls those repos and feeds them into NotebookLM through a Python bridge — an open-source tool called notebooklm-py. It's a CLI that gives any LLM direct access to NotebookLM programmatically. The researcher uses this to run deep analysis on the repos — not just what they do, but what they enable, what use cases nobody's explained yet, what questions developers are going to have in two weeks when this hits mainstream.

`[SHOW SCREEN: Research brief landing in Obsidian — 10-Research folder, dated file]`

That brief lands in your vault. Dated. Linked. Every time you run it, it's a new node in your knowledge graph.

Now here's the thing you'd assume at this point — you'd assume the research is the heavy lift. It's not. The research is almost fully automatic. You point it, it runs, it comes back.

The heavy lift — the part with actual nuance — is everything that comes after the research hits the vault.

---

## [Stage 4: Validation] — 3:30–7:00

`[SHOW SCREEN: Obsidian vault — 10-Research folder, research brief open]`

The research brief is sitting in your vault. You read it, you pick the angle that interests you, and you run `/hook`.

`[SHOW SCREEN: /hook running — Python file executing in background]`

Here's what's happening under the hood when that runs. The SKILL.md file — which is the Claude Code entry point, what triggers when you type the slash command — calls a Python file. That Python file runs in the background. It reads the research brief, it reads hooks.md, and it passes all of that to Claude with no token waste. None of that execution noise ends up in Claude's context window. Claude only sees what it needs to see: the topic, the research, and the hook framework.

`[SHOW SCREEN: hooks.md open — 10 patterns visible]`

That hook framework — hooks.md — is the single source of truth for all hook generation. Ten Kallaway patterns. The Dopamine Ladder opening stages. Banned openers. Retention rules. When Kallaway releases new material, you update one file and the entire system updates.

`[SHOW SCREEN: /hook output file in Obsidian — 05-Hooks folder]`

Five hook variations come back. You pick one. That's your entire job at this step.

---

Now the snowball starts.

You take that approved hook and run `/outline`.

`[SHOW SCREEN: /outline running → output appearing in Obsidian — 06-Outlines folder]`

The outline skill takes your hook — verbatim, exactly what you approved — and builds a six-stage Dopamine Ladder around it. Every stage is named. Every section has a duration target. Talking points are written out. Visual cues are marked inline — B-roll notes, screen share cues, text overlays. And at least two head fakes are pre-marked in the structure — places where you plant a wrong expectation and subvert it, to reset the curiosity loop mid-video and stop people from dropping off at section transitions.

You film from this. Not word for word. You speak from the structure.

Then `/title`.

`[SHOW SCREEN: /title running → 10 titles with thumbnail text]`

Ten title options. The ones the model itself flags as uncertain get marked experimental — so you always know which are proven patterns and which are tests. Every title comes with thumbnail text. You pick one. Done.

At this point you have a hook, a structure, and a title. You've made the video.

---

Now you drop the finished recording into a specific folder in your vault and run `/cascade`.

`[SHOW SCREEN: Cascade folder structure → /cascade running]`

Cascade — I'm renaming this to Distribution after this video because that's what it actually does — takes your finished video and generates the full distribution layer. LinkedIn post. Instagram slide deck. Platform-specific captions and formats. Every output is adapted for the platform it's going to. The tone shifts. The length shifts. The hook of the LinkedIn post is different from the Instagram caption because the audiences and scroll behaviors are different.

While cascade is running, `/short-form` takes the same outline and compresses it.

`[SHOW SCREEN: Short-form outputs — 30s, 60s, 90s scripts side by side]`

Three outputs: 30-second script, 60-second script, 90-second script. All pulled from the same video structure. Same core idea, different depths. You pick which one you're shooting based on what the platform needs that week.

---

And then every single one of those outputs — the LinkedIn post, the Instagram deck, the short scripts, all of it — runs through `/voice-cleanup`.

`[SHOW SCREEN: voice_profile.md open]`

This is my voice profile. Two things live here.

First: banned words. "Crucially." "Furthermore." "Tapestry." "Landscape." Every word that makes AI output sound like it came from a model instead of a person — listed and banned. The cleanup skill strips all of it.

Second: my cadence. Punchy. Direct. One idea at a time. No "as I mentioned earlier." No recap sentences. No "in conclusion." The skill reads every output against this profile and rewrites anything that violates it.

If you skip voice cleanup, every script this system produces sounds identical. And it sounds like AI. The research will be solid, the hook will be good, the structure will be right — and the script will be unlistenable. Voice cleanup is the step that makes it yours.

---

Now let me show you why this works as three files instead of one giant system prompt.

`[SHOW SCREEN: Skill anatomy — SKILL.md, hook.py, hooks.md side by side]`

Every skill in this system is three files.

**SKILL.md** — the Claude Code entry point. This is what fires when you type the slash command. It's one or two lines. No logic, no intelligence. Just a trigger.

**The Python file** — this is the execution layer. hook.py, outline.py, title.py — one per skill. Each one runs in the background, handles file reads, calls the model, writes to the vault. None of that logic contaminates Claude's context. Claude stays clean.

**The prompt.md file** — this is where the intelligence lives. hooks.md for hook generation. outline.md for the Dopamine Ladder. voice_cleanup.md for the voice rules. These are readable files. You can open them, read them, understand exactly what the system is doing. When you want to update the Kallaway patterns, you edit one file. When you want to change your cadence rules, you edit one file. The system is transparent by design.

That's why a monolith — one giant system prompt with everything jammed into it — would break. You can't update one part without risking the whole thing. You can't see what's doing what. The three-layer structure keeps it modular, readable, and maintainable.

---

## [Stage 5: Affection] — 7:00–8:00

`[TALKING HEAD — no screen share. Direct camera. This is the personal section.]`

Why did I build this?

Honest answer — I know myself. I get excited about something for three or four years. And then I want to move on to the next thing. That's just how I'm wired.

Every time I've tried to build something that requires my active enthusiasm to survive — it dies the moment I get bored. The system stops because I stopped.

Automation changes that. The pipeline runs whether I'm excited about YouTube or not. I can step away, come back six months later, point it at a new topic, and it works. I'm not tied to the system being alive. That's the actual value to me — not speed, not efficiency. Optionality. The ability to walk away and come back.

And the part that genuinely surprised me building this: the research step was easy. The hook generation was easy. The hard part was voice. Getting AI to not sound like AI took longer than every other piece of this system combined. Most people building something like this would ship after the hook skill works and call it done. The output would be technically good and completely unlistenable. The voice profile is the piece that nobody would think to build — and it's the piece that makes everything else worth using.

---

## [Stage 6: Revelation] — 8:00–8:45

`[TEXT OVERLAY: "Automation removes the blank page. Not your judgment."]`

Here's the thing nobody says when they talk about automating content.

The bottleneck was never production. It was decision fatigue.

Which topic do I pick? Which hook is strongest? Which title will actually perform? Every one of those decisions costs mental energy before you've even touched a camera. By the time you've decided all of that, you're already drained. The filming feels like a tax.

This system doesn't make those decisions for you. It gives you five hooks — you pick one. It gives you ten titles — you pick one. A six-stage outline — you film from it. The system generates. You select.

Selection is faster. Selection is less draining. And selection actually produces better output than trying to generate and evaluate at the same time — because you're comparing options, not building from nothing.

That's the real shift this system makes. Not speed. Not automation. The removal of the blank page.

Your judgment is still in the loop at every step. The system just means you never have to stare at an empty document and wonder where to start.

---

## [CTA] — 8:45–9:15

`[End screen cards visible. Talking head.]`

If you want to build something like this — the next video covers the architecture in detail. How to wire a Python skill file to a prompt file inside Claude Code. Why the three-layer pattern matters the moment you want to swap models or run parts of the pipeline locally on Ollama instead of Claude.

The full hooks.md — ten Kallaway patterns, the Dopamine Ladder stages, retention rules, banned openers — is in the repo. Link's below. Start there if you want to understand how the hook generation actually works.

And if you only pull one thing from this video: start with the hook system. It's the piece that changes your output the most. Everything else builds on top of it.

---

*End of script. Total estimated runtime: 8–9 minutes at natural speaking pace.*
