---
topic: Why open-source design tools are suddenly worth watching
platform: yt-long
target_length: 8 minutes
hook_used: Hook 3 — Shock Value (The Awareness Play)
created: 2026-05-29
date: 2026-05-29
status: ready-to-film
pipeline_stage: outline
linked_hook: "[[2026-05-24_hook-why-open-source-design-tools]]"
description: "Dopamine Ladder outline for 8-min YouTube video on Open Design — agent-native design tool that runs inside Claude Code, Codex, and Cursor. Hook 3 selected."
tags: [outline, yt-long, open-source, design-tools, agent-native, dopamine-ladder, pipeline]
---

# Outline: Why open-source design tools are suddenly worth watching

---

## [Stage 1: Stimulation] — 0:30

**Dopamine Goal:** Stimulation

**Hook (verbatim — Hook 3):**

**Spoken Line** (first 3 seconds):
> "The design tool you're paying for just became optional."

**Setup** (next 10 seconds):
> "Open Design runs inside Claude Code, Codex, and Cursor. 71 design systems built in. Prototype generation. HTML, PDF, video export — no subscription. It doesn't replace your coding agent. It uses it."

**Promise** (next 15 seconds):
> "I spent a week testing it against my current stack. Here's what it does, where it breaks, and whether you should switch today."

`[B-ROLL: Extreme close-up of a "Cancel Subscription" button — hard cut to Open Design outputting a polished UI in under 10 seconds]`

`[TEXT OVERLAY: "Your design subscription is now optional."]`

**Transition to Stage 2:**
> "Here's what actually changed — and why it took this long."

---

## [Stage 2: Captivation] — 0:55

**Dopamine Goal:** Captivation

**Talking Points:**
- Most AI builders are paying two subscriptions: one for their coding agent, one for their design tool. Those two never talk to each other — the agent writes code, you leave, open the design tool, export assets, come back. The loop adds 30–45 minutes to every feature cycle.
- The reason open-source design never replaced this: it was always too rough. Hard to install, poor component libraries, no AI, no export. You'd save $15/month and lose two hours of productivity every time. That trade-off just inverted.
- Open Design's key difference is that it doesn't bundle its own AI model. It detects whichever coding agent you already have — Claude Code, Codex, Cursor — and hands the entire design loop to it. Your coding agent now has design as a native action.

**Stakes:** If this works at production quality: $15/month saved is the small version. The larger version is eliminating the design-to-code handoff loop entirely — one fewer app switch, one fewer export cycle, one fewer round of "does this match what I designed?" per feature.

`[B-ROLL: Side-by-side screen recording — left: switching between Figma and VS Code; right: single terminal session outputting prototype]`

`[TEXT OVERLAY: "Two tools. One loop. $0."]`

**Transition to Stage 3:**
> "But before you cancel anything — there's a reason most people haven't heard of this yet. And it's not what you'd expect."

---

## [Stage 3: Anticipation] — 1:25

**Dopamine Goal:** Anticipation

**Talking Points:**
- Open Design has 71 design systems included — brand-grade, production-ready. Figma's community has more, but the majority are incomplete drafts. These 71 are full component sets with tokens, variants, and states. The comparison isn't volume; it's usability out of the box.
- It's not a visual editor. There is no canvas, no drag-and-drop, no layers panel. If you're looking for a Figma replacement with a GUI, this isn't it — and that's actually the point. The interface is your coding agent's chat window. You already know it.
- The workflow: describe the UI in plain language or spec → agent reads your existing codebase → selects the closest design system → generates a working prototype → exports to HTML, PDF, or video. One command, one output.

**Head Fake 1:**
> "You might think: the quality must be rough — open-source, no dedicated design team. I thought the same thing. Then I asked it to build a SaaS dashboard from scratch and it matched a paid Figma template I had been using for six months — in under two minutes."

`[SHOW SCREEN: Split comparison — Open Design output vs. paid Figma template, components aligned side-by-side]`

**Transition to Stage 4:**
> "Here's the exact setup — and the one thing you need to do before it works properly."

---

## [Stage 4: Validation] — 2:30

**Dopamine Goal:** Validation

**Talking Points:**

**Step 1 — Install (60 seconds or less):**
- One npm install, one config line pointing to your agent. No account, no OAuth, no API key for the tool itself — it inherits your existing agent's credentials.

`[SHOW SCREEN: Terminal — full install sequence, timestamp visible in corner, under 60 seconds elapsed]`

**Step 2 — First prompt:**
- Type a design brief in plain language: component type, layout constraints, any brand tokens you have. The agent reads your repo for existing styles first — it won't introduce a conflicting color system if you already have one.

`[SHOW SCREEN: Chat window — design prompt entered; agent response includes component code + preview link]`

**Step 3 — 71 design systems in practice:**
- The system picker is automatic, but you can override it. Type "use [system name]" in the chat. Switch mid-session without resetting. Each system is versioned and pinned — no silent updates breaking your prototypes.

`[SHOW SCREEN: System switcher prompt → three different outputs from the same spec using different design systems]`

**Step 4 — Export:**
- HTML export is clean, production-grade markup — not a Figma-style flat export. PDF for stakeholder handoffs. Video export generates a scrolling walkthrough automatically, no screen recording needed.

`[SHOW SCREEN: Export menu; HTML file opened in browser — inspect panel showing clean semantic markup]`

**Head Fake 2:**
> "At this point I assumed the limitation would be responsiveness — that I'd get a desktop layout and have to rebuild mobile. Wrong. It generates responsive breakpoints from the spec unless you tell it not to."

`[SHOW SCREEN: Browser dev tools — responsive toggle showing mobile and desktop breakpoints from the same export]`

**What it can't do yet (be honest):**
- Real-time collaboration. If you're on a team where designers and developers share a Figma file simultaneously, this doesn't replace that workflow today.
- Complex animation. Micro-interactions, scroll-triggered effects — not there yet. Static and transition-based UI: fully covered.

`[TEXT OVERLAY: "Where it breaks — collaboration + complex animation"]`

**Transition to Stage 5:**
> "I want to tell you about the moment I actually understood what this tool is — because it changed how I think about the whole category."

---

## [Stage 5: Affection] — 1:05

**Dopamine Goal:** Affection

**Talking Points:**
- I went into this assuming I'd find a clever indie project — useful for prototypes, not for anything real. I was wrong in a specific way: I had assumed that "agent-native" was a marketing phrase. Then I ran it on an actual feature I was building — a multi-step form with conditional logic — and the agent pulled in my existing component library, matched the spacing system I'd already defined in tokens, and gave me something I could hand off. Not a mockup. A working component.
- The moment of realization: I opened the exported HTML file and the class names matched my existing codebase conventions. Not because I told it to. Because the agent had read my repo before generating.
- What I got wrong: I kept thinking of this as a design tool. It's not. It's a design action inside your coding agent. That's a different thing entirely.

`[TALKING HEAD: no overlay, direct to camera — no cuts]`

**Transition to Stage 6:**
> "And that distinction points to something bigger — something that I think most of the reviews of this tool are completely missing."

---

## [Stage 6: Revelation] — 1:05

**Dopamine Goal:** Revelation

**Talking Points:**
- The real shift here isn't about saving $15 a month. It's about where design decisions get made. In every current workflow, design happens in a sandboxed tool that knows nothing about your codebase. Your agent writes code in one context; your designer works in a completely separate context. They never share state.
- Agent-native design collapses that gap. When your coding agent generates a UI, it already knows your types, your component library, your naming conventions, your spacing tokens. The design output is consistent with the code output because it's generated by the same system in the same context.
- This is what "design-code parity" actually looks like in practice — not design handoff tools, not Figma dev mode. The agent writes both, from the same prompt, from the same repo context. Paid design tools can't replicate this because they're architecturally isolated from your codebase.

`[TEXT OVERLAY: "Design decisions made in code context — not in a separate sandbox."]`

`[B-ROLL: Single terminal window — one prompt generating both UI component code and the design spec simultaneously]`

---

## [CTA] — 0:35

**Goal:** Drive to the next video in the series — specifically the agent-native workflow deep dive.

**Talking Points:**
- If you want to see this running inside a real project — not a demo repo, an actual SaaS feature build — that's the next video. I run the full cycle: spec to prototype to production component, zero context switches.
- If you leave before watching that one, you'll have the tool installed but you'll miss the setup step that unlocks repo-aware generation. It's not in the docs.

`[TEXT OVERLAY: "Subscribe — the full agent-native build is next."]`
`[SHOW SCREEN: End card with next video thumbnail pinned]`
