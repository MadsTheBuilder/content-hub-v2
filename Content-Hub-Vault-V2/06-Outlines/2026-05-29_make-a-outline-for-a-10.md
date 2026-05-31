## [Stage 1: Stimulation] — 0:30

**Dopamine Goal:** Stimulation

**Hook (verbatim):**

> "If you've been running Claude Code for weeks and still feel like you're just chatting with it — this is exactly why."

> "You don't have a Claude problem. You have a skill gap. There are 10 things separating builders who prompt from builders who ship — and you're missing most of them."

> "I'll close that gap right now. These are the 10 skills, in the order they build on each other — so each one you add makes the next one click instantly."

`[TEXT OVERLAY: "The 10 Skills You're Missing"]`
`[B-ROLL: Numbered checklist filling with green checkmarks at speed-ramped pace — final frame: all 10 checked]`

---

## [Stage 2: Captivation] — 0:45

**Dopamine Goal:** Captivation

**Talking Points:**
- Claude Code is not a chatbot with a code plugin. It's an autonomous agent runtime — it reads your filesystem, runs shell commands, spawns sub-agents, and loops until a verification condition passes. If you're treating it like a chat window, you're running at about 10% of what it can actually do.
- The back-and-forths aren't Claude being slow. That's you without Skills 1 and 2 in place — Claude re-deriving your project conventions from scratch on every single exchange. You're paying the full context tax every session start. Every time.
- The builders shipping 3–5 features a week aren't writing better prompts. They front-loaded this skill stack. Each session opens at a higher baseline than where the last one ended.

`[SHOW SCREEN: Two Claude Code sessions side by side — left: 50+ exchanges, context nearly full, task incomplete — right: 4 exchanges, task resolved, context at 12%]`
`[TEXT OVERLAY: "10% capacity vs. full capacity"]`

**Transition to Stage 3:**
> "Before I give you the list — here's the one assumption that kills most Claude Code sessions before the first message is even sent."

---

## [Stage 3: Anticipation] — 1:00

**Dopamine Goal:** Anticipation

**Talking Points:**
- Most builders think Claude Code skill is about prompt quality. They spend hours on phrasing — more context, more examples, more explicit instructions — trying to engineer the perfect first response.
- That's the wrong axis. The highest-leverage inputs aren't in the message body. They're in how the session is structured before you type anything — what files Claude can see, what project conventions are pre-loaded, what verification step closes each task.

**Head Fake #1:**
> "You'd think Skill #1 is prompt engineering. It's not. Prompt engineering is Skill #6. The five skills before it are what make any prompt actually land — without them, a perfectly written prompt still fails half the time, and you spend the next hour figuring out why."

`[B-ROLL: 10 numbered skill cards flashing in rapid sequence — titles blurred, numbers only visible. Viewer knows there are 10 but can't read a single one yet.]`
`[TEXT OVERLAY: "The order matters more than the skills themselves"]`

**Transition to Stage 4:**
> "Here are all 10. In order. Starting with the one that changes every skill that follows."

---

## [Stage 4: Validation] — 4:00

**Dopamine Goal:** Validation

**Skill 1 — Multi-File Context (~0:25)**
- Most builders prompt Claude against one file at a time. That's like asking a surgeon to operate through a keyhole — they can't see what's adjacent, what they'll break downstream, or what already handles the case three files over.
- Fix: before your first message, use `@filename`, `/add-dir`, or CLAUDE.md `#include` patterns to load the full relevant module into context. Claude reasons across file relationships — but only when it can actually see them.

`[SHOW SCREEN: CLAUDE.md with an #include src/models/ directive — Claude Code session opening with the full tree already visible in context before a single prompt is typed]`

**Skill 2 — CLAUDE.md Configuration (~0:25)**
- Without a CLAUDE.md, Claude re-derives your stack, conventions, and constraints from scratch every session. That's 5–8 exchanges of overhead before real work starts — and it compounds across every session you run.
- A CLAUDE.md that actually pays off has five sections: stack, file structure, test conventions, what not to change, and explicit anti-patterns. Nothing else. If it takes more than 30 lines to write, you're over-explaining.

`[SHOW SCREEN: A 30-line CLAUDE.md with those five sections annotated — no walls of text, just constraints Claude can act on]`

**Skill 3 — Agentic Task Decomposition (~0:25)**
- Dumping a 10-step task in one message produces one attempt at a 10-step task — typically 60% correct and fragile under any follow-on changes. Decompose it into sequenced sub-tasks with explicit verification criteria and you get working code that holds.
- Exact format: `"Step 1: [task]. Verify: [specific check]. Step 2: [task]. Verify: [specific check]."` Claude loops until each check passes before moving forward.

`[SHOW SCREEN: A task decomposed in the message input — numbered steps with inline verification criteria — first step resolved, verified, then Step 2 starting clean]`

**Skill 4 — Context Window Management (~0:25)**
- Claude Code has a finite context window. Builders who don't track it hit the wall mid-session — Claude starts losing thread, responses degrade, the task stalls with no clean save point. Recovery costs 30 minutes.
- Rule: run `/compact` before you hit 80% context. The summary carries your project state and prior decisions forward. The thread doesn't break. You don't re-explain what was resolved 40 messages ago.

`[SHOW SCREEN: Context window indicator at 75% — /compact command executing — session continues with a clean summary node replacing raw history, prior decisions intact]`

**Skill 5 — Custom Slash Commands (~0:25)**
- Retyping the same 10-line task setup every session adds up fast. Every project has 3–4 recurring task patterns — outline generation, code review, schema migration, full test run.
- Encode each one as a custom slash command in `.claude/commands/`. A single `/outline` or `/review` replaces 10 lines of setup and runs identically every time, on every project that uses it.

`[SHOW SCREEN: .claude/commands/ folder with four .md command files — then a single /outline slash command triggering a full multi-step pipeline from one keystroke]`

**Head Fake #2:**
> "You'd think MCP servers are advanced territory — only relevant if you're building tooling or you're a senior engineer who already has the fundamentals locked. That's exactly backwards. Non-engineers who wire MCP early gain the biggest edge, because they stop describing their system to Claude and start letting Claude read it directly."

**Skill 6 — Constrained Prompt Engineering (~0:20)**
- Prompt engineering for code is not about length or example count — it's about constraints. The more precisely you constrain the output surface, the less Claude has to infer, and the fewer correction loops you run.
- Four constraints that matter in every prompt: file to edit, function signature or interface shape, what not to change, expected output format. Everything beyond that is decoration.

`[TEXT OVERLAY: "Constraints > Detail"]`
`[SHOW SCREEN: A 6-line prompt with those four constraints annotated alongside a 25-line prompt with none — same task, cleaner first-pass output on the shorter version]`

**Skill 7 — MCP Servers and Tool Use (~0:25)**
- MCP lets Claude reach outside the conversation into live system state — your filesystem, APIs, databases, browser. Without it, Claude reasons about your system from your description of it. With it, Claude reads the actual file, the actual schema, the actual API response.
- Start with the two external systems Claude touches most in your workflow. Wire them as MCP tools. The first session where Claude reads a live config and patches it correctly — no guessing, no back-and-forth — makes the 20-minute setup feel irrelevant.

`[SHOW SCREEN: Claude using an MCP filesystem tool to read a live .env config, identify a missing key, and insert it correctly — zero clarifying exchanges]`

**Skill 8 — Iterative Verification Loops (~0:20)**
- Accepting Claude's first output on a visual scan is how bugs compound silently. By the time you catch the issue, it's across four files and the root cause is in a session from three days ago.
- One rule that catches most issues: before accepting any output, ask Claude: *"State exactly what you changed and why — including what you chose not to change."* If the answer surprises you, you caught a bug before it shipped.

`[TEXT OVERLAY: "What did you change, and why?"]`
`[SHOW SCREEN: Claude's self-report on a change — surfacing a decision the builder would have missed on a line-by-line read]`

**Skill 9 — Test-First Development with Claude (~0:20)**
- Tell Claude to write the failing test before writing any implementation. This sounds slower. It's not. The test defines the success criteria Claude is building toward — and the test run gives you a binary verified/not-verified signal instead of a visual scan that misses edge cases.
- Bonus: when Claude produces a test that's hard to write, that's Claude telling you the interface design is wrong. Fix the interface before writing the implementation.

`[SHOW SCREEN: Claude writing a failing test — RED in terminal — then the implementation — then the test turning GREEN. Three messages, zero rework.]`

**Skill 10 — Multi-Agent Orchestration (~0:20)**
- Single-agent sessions hit a ceiling at roughly three specialist domains. Any task spanning frontend + backend + schema simultaneously will produce shallow work in at least one of them — Claude can't hold full depth across all three at once.
- Use `/orchestrate` for cross-domain tasks. Each agent owns one domain with role-specific context loaded. A coordinator agent merges outputs and flags conflicts. You review one diff, not three independent outputs.

`[SHOW SCREEN: /orchestrate spawning three agents with explicit role headers — schema agent, API agent, UI agent — their outputs merged into a single diff in the coordinator review pass]`

**Transition to Stage 5:**
> "That's the stack. Here's what I got completely wrong for the first two months — and why this exact order is the only one that actually works."

---

## [Stage 5: Affection] — 1:00

**Dopamine Goal:** Affection

**Talking Points:**
- I spent the first two months treating Claude Code like a smarter autocomplete. Dump a task in, get output, paste it in, move on. Sessions were fast. Code was fragile. Features worked in isolation and broke the moment anything adjacent changed.
- The shift wasn't a new prompt formula. It was realizing Claude Code is a collaborator, not a vending machine. The skill isn't in the request — it's in the setup before the request and the verify step after. Everything else is just hoping the first output happens to be right.
- The week I added CLAUDE.md to every active project and stopped accepting outputs without asking Claude to account for exactly what it changed — my shipped-feature rate doubled. Not the number of sessions I ran. The number of things that actually worked when I pushed them.

`[Talking head — no text overlay. Direct to camera.]`
`[B-ROLL: Brief cut to a project root folder with CLAUDE.md visible — then back to talking head]`

**Transition to Stage 6:**
> "Here's the thing no tutorial will tell you about these 10 skills — and why most people who learn them out of order still get mediocre results even after they've learned all 10."

---

## [Stage 6: Revelation] — 0:45

**Dopamine Goal:** Revelation

**Talking Points:**
- These skills don't add — they multiply. Skill 1 (multi-file context) makes every subsequent skill more effective because Claude is reasoning over the full system, not a fragment. Add Skill 2 (CLAUDE.md) and you've cut 80% of re-derivation overhead. By Skill 5, sessions run on institutional memory instead of explanation. The ceiling moves every time you add a layer.
- The trap every builder falls into: learning skills out of order. They pick up Skill 7 (MCP) from a tweet, wire it up without Skills 1–3 in place, and it underdelivers. They conclude MCP doesn't scale to their use case. MCP scales. The foundation was missing.
- Stack them in sequence and Skill 10 stops feeling like a feature. You're no longer prompting an AI. You're running a parallel engineering team from a single slash command — each agent holding its domain and handing off clean state. That's not a metaphor. That's what the output looks like.

`[TEXT OVERLAY: "Skills don't add. They multiply."]`
`[B-ROLL: The checklist from Stage 1 — each skill lighting up in sequence, the interval between checkmarks getting shorter with each one, all 10 lit simultaneously on the final frame]`

---

## [CTA] — 0:30

**Goal:** Pull to the next video with the specific problem the viewer now knows they have.

**Talking Points:**
- The hardest skill to build from documentation alone is #10 — multi-agent orchestration. Most resources show you the concept. None of them show you how to define agent roles so they don't duplicate work, conflict on shared files, or drop state at the handoff — which is exactly where 80% of first attempts fail.
- The next video is the exact orchestration template I use for every cross-domain task: role definitions, the handoff protocol, and the one structural mistake that breaks most first attempts without you even knowing it happened.
- If you're shipping anything complex with Claude Code, you need that template before your next session.

`[TEXT OVERLAY: "Next: The Multi-Agent Orchestration Template"]`
`[End screen graphic — subscribe prompt + next video card pointing to orchestration video]`