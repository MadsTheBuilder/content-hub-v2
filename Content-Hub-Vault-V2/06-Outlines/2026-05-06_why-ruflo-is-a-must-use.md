---
topic: Why Ruflo is a must-use repo for Claude builders
platform: yt-long
target_length: 8m
hook_source: Content-Hub-Vault-V2/05-Hooks/2026-05-06_the-github-repo-that-gives-claude.md
created: 2026-05-06
---
# Outline: Why Ruflo is a must-use repo for Claude builders

## [Stage 1: Stimulation] — 0:30

**Dopamine Goal:** Stimulation
**Hook (verbatim):**

> **Spoken Line:** You're thinking about Claude API costs all wrong.
>
> **Setup:** Most builders try to fix costs by shortening prompts. That's the wrong lever. The real savings come from agent architecture — and there's a GitHub repo that already solved it. 100 specialized agents, built for token efficiency. One repo. 75% cheaper.
>
> **Promise:** I'll show you exactly what they changed, why it works, and how to use it in your current Claude Code setup. You don't have to reverse-engineer it — I already did.
>
> **Visual Cue:** Close-up of a prompt being trimmed — then a hard cut to a "WRONG" graphic. New frame: a GitHub repo directory, 100 agent files. Cost graph drops 75%.
>
> **Text Overlay:** The Real Reason Your API Costs Are High. (It's Not What You Think.)

---

## [Stage 2: Captivation] — 1:00 (0:30–1:30)

**Dopamine Goal:** Captivation

**Talking Points:**
- Claude Code bills per token — and at production scale that compounds fast. Two developers running active agents can hit $800–$1,200/month without any unusual usage pattern. That's not edge-case math; it's default behavior.
- The fix everyone reaches for — shorter prompts, fewer words in the system prompt — reduces costs by 8–12%. Real, but not the lever. The actual lever is agent architecture: how many calls you're making, what scope each agent carries, and whether a routing layer filters inputs before the expensive model ever fires.
- Ruflo is a GitHub repo with 100 pre-built Claude agents, structured exactly around these architectural principles. Free, MIT-licensed, and the savings are repeatable — not a one-off optimization you have to rediscover every sprint.

**Visual Notes:**
[SHOW SCREEN: Claude API billing dashboard — real monthly invoice with line items visible, total highlighted in red]
[TEXT OVERLAY: "Prompt trimming cuts 8–12%. Agent architecture cuts 75%."]
[B-ROLL: Developer shortening a system prompt on the left — token counter on the right barely moves]

**Transition to Stage 3:**
"Before I show you which agents to pull first — I need to show you why every Claude builder gets the cost problem backwards. Because the misdiagnosis is what's expensive."

---

## [Stage 3: Anticipation] — 1:30 (1:30–3:00)

**Dopamine Goal:** Anticipation

**Talking Points:**
- Token costs break into three buckets: input tokens, output tokens, and context reuse. Most builders over-index on output length and system prompt size. Neither is the primary cost driver at scale.
- The real cost multiplier is redundant context loading — every time Claude receives full, unfiltered input because there's no routing layer upstream, you pay for tokens the model didn't need to see. Ruflo's agents eliminate this by enforcing scope at the entry point before a Sonnet or Opus call is ever made.

**Head Fake #1:**
"Your instinct is probably to grab the most capable-sounding agents first — the multi-step reasoning ones, the ones that sound like they do everything. [pause] The highest-ROI agents in this repo are the ones that look the most boring. A classifier and a router. Two files. They're the reason the other 98 agents work at all."

[TEXT OVERLAY: "Most valuable agent in the repo: a classifier."]

**Visual Notes:**
[SHOW SCREEN: GitHub repo file tree — 100 agent files listed, slow scroll, pause on `/routing` folder]
[B-ROLL: Terminal window firing Claude agent calls — cost ticker incrementing in the corner of the screen]

**Transition to Stage 4:**
"Let me prove it. Here's what the API logs look like before and after Ruflo — and I'll show you exactly which four files to pull first and in what order."

---

## [Stage 4: Validation] — 3:00 (3:00–6:00)

**Dopamine Goal:** Validation

**Talking Points:**
- **The Before/After — Real API Logs:** 7-day usage dashboard. Day 1 baseline: 2.4M tokens/day, $38.40 at standard Sonnet 3.5 pricing. Day 7 with Ruflo fully deployed: 610K tokens/day, $9.76. Same workload, same output quality. That's the 75% cut — not from prompt trimming, from routing and scope discipline.
- **Deploy in This Order, Not Random:** Start with `classify-intent.md` and `route-task.md` from the `/routing` folder. These two agents intercept every user input before Sonnet sees it. A Haiku call classifies the request type; the router sends it to the correct specialized agent. Main model call count drops 40–60% on day one.
- **Repo Structure — Three Directories That Matter:** `/routing` first (install before anything else), `/task-specific` second (add agents that match your use cases), `/context-managers` third. Skip `/experimental` entirely until you've run the core pipeline for two weeks. The README quickstart is four commands — clone, copy agent files into `.claude/`, reference them in CLAUDE.md, fire a test call.

**Head Fake #2:**
"Most people install the context-manager agents first — the name implies maximum token savings. They're actually third priority, not first. Without the routing layer upstream, context managers have nothing to scope. The pipeline runs hot regardless of what you stack on top."

[TEXT OVERLAY: "Context managers without routing = zero impact."]

**Visual Notes:**
[SHOW SCREEN: API usage dashboard — two-column view, token counts before vs. after, real numbers side by side]
[SHOW SCREEN: GitHub repo — navigate to `/routing`, open `classify-intent.md`, highlight the token budget field in the system prompt]
[B-ROLL: Four-command terminal setup sequence running in real time — each command output visible, no cuts]
[TEXT OVERLAY: "Day 1: 2.4M tokens/day → Day 7: 610K tokens/day. Same workload."]

**Transition to Stage 5:**
"I didn't figure out this deployment order from the README. I figured it out by doing it wrong first — and it cost me two days."

---

## [Stage 5: Affection] — 1:00 (6:00–7:00)

**Dopamine Goal:** Affection

**Talking Points:**
- Deployed context-manager agents first — because "context manager" sounded like it solved the exact problem I'd diagnosed. Costs barely moved. Spent two days checking routing logic I thought was broken before realizing the issue was sequencing. Without classifiers upstream, Claude was still receiving full raw input on every call. The context managers had nothing to act on.
- The mental model that fixed it: Ruflo isn't a toolbox you dip into. It's a pipeline you install in sequence — classify, route, task agent, context manager — and each stage only works because the previous one ran. Once I re-deployed in order, costs dropped within 24 hours of the first real traffic.

**Visual Notes:**
[Talking head only — no screen share. Direct eye contact. Conversational pace.]
[TEXT OVERLAY: "It's a pipeline, not a toolbox. Order is load-bearing."]

**Transition to Stage 6:**
"But the cost savings — the 75% — isn't actually the most interesting thing this repo shows you. This is."

---

## [Stage 6: Revelation] — 0:45 (7:00–7:45)

**Dopamine Goal:** Revelation

**Talking Points:**
- The 75% cost cut is real — but it's a diagnostic, not the destination. When you're forced to define agent scope precisely enough to use Ruflo's architecture, you immediately see every place in your existing build where you were asking Claude to do too much in a single call. Every "all-purpose agent" you built is a liability you can now name and fix. Ruflo doesn't cut your bill — it exposes the architectural sloppiness that inflated it.
- This is the pattern across every production-grade Claude deployment: cost discipline and capability discipline are the same discipline. The teams running Claude at real scale aren't using bigger models — they're using smaller, scoped agents that do one thing precisely. Ruflo forces that discipline by design. The 75% is just what scope discipline looks like on an invoice.

**Visual Notes:**
[TEXT OVERLAY: "75% cost cut = a diagnostic. Scope discipline is the actual skill."]
[B-ROLL: Wide shot — two monitors side by side. Ruflo repo on the left. Flat cost graph on the right. No dramatic motion. Just flat.]

---

## [CTA] — 0:30 (7:45–8:15)

**Goal:** Give viewers a specific reason to watch the next video — not just "click subscribe."

**Talking Points:**
- The next video covers how to build a custom agent from scratch that fits Ruflo's scoping architecture — so when your use case outgrows the 100 pre-built agents, you can extend the library without reverting to the expensive all-purpose pattern that inflated your bill in the first place.
- Skip it and you'll hit the exact wall most Ruflo users hit at week two: the pre-built library runs out for your specific use case, and there's no framework for adding agents without blowing the cost structure you just built.

**Visual Notes:**
[TEXT OVERLAY: subscribe prompt] · [end screen graphic with thumbnail of next video]
