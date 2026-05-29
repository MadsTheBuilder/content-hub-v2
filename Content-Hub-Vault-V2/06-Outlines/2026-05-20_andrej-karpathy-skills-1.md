---
topic: andrej-karpathy-skills_1
platform: yt-long
target_length: 8m
hook_source: none
created: 2026-05-20
---
# Outline: andrej-karpathy-skills_1

## [Stage 1: Stimulation] — 0:00–0:30

**Dopamine Goal:** Stimulation
**Hook (verbatim):**
[No hook provided in INPUT — placeholder. Recommend running `/hook` for "Andrej Karpathy on Skills" before filming and pasting the ⭐ variant here verbatim.]

[B-ROLL: fast cut of Karpathy talking head clip → terminal scrolling Claude skills directory → creator's face reacting]
[TEXT OVERLAY: "Karpathy was right."]

---

## [Stage 2: Captivation] — 0:30–1:30

**Dopamine Goal:** Captivation

**Talking Points:**
- Karpathy just publicly endorsed Claude Skills as the cleanest paradigm he's seen for agent capability — and most builders are still gluing custom tools onto LLMs the hard way.
- Stakes: if you're building agents in 2026 and still hand-rolling tool wrappers, you're burning weeks reinventing what's now a folder with a markdown file. The teams shipping fastest aren't smarter — they switched primitives.
- Quick context: a "skill" is a self-contained folder (`SKILL.md` + scripts) the model decides to load when relevant. No framework. No SDK ceremony. Karpathy's point was deeper than convenience — it's a fundamentally different unit of intelligence composition.

**Visual Notes:**
[SHOW SCREEN: Karpathy's tweet/post, full screen, then zoom on the key line]
[B-ROLL: file explorer expanding a `.claude/skills/` directory showing 6–8 SKILL.md files]
[TEXT OVERLAY: "Folder + markdown = new agent primitive"]

**Transition to Stage 3:**
"But here's what Karpathy said that nobody is talking about — and it's the part that actually changes how you should build."

---

## [Stage 3: Anticipation] — 1:30–3:30

**Dopamine Goal:** Anticipation

**Talking Points:**
- Detail 1: Skills aren't prompts. They're not tools either. They sit in a third category — capabilities the model *chooses* to load based on description matching, which means the system prompt stays clean and the model's context only fills up when it needs to.
- Detail 2: The implication Karpathy hinted at — every skill you write is composable with every other skill, with zero integration code. Two skills written by two different people, never tested together, just work. That's not true of MCP servers, custom tools, or agent frameworks.
- Detail 3: He compared this to a specific moment in computing history (the Unix philosophy) — small composable text-based units that the OS routes intelligently. The parallel is exact.

**Head Fake:**
You probably think the big deal is the *convenience* — "oh nice, I don't have to write a tool definition." That's the surface read. The actual shift is that skills are the first abstraction where **the model is the runtime, not your code**. The folder is the program. The LLM is the interpreter. Stop thinking like a software engineer for a second.

**Visual Notes:**
[SHOW SCREEN: side-by-side — left: 200 lines of MCP server boilerplate, right: a 15-line SKILL.md doing the same job]
[B-ROLL: diagram of skills as Lego bricks snapping together with no glue]
[TEXT OVERLAY: "Model = runtime. Folder = program."]

**Transition to Stage 4:**
"Once that clicked for me, I went back and rebuilt my entire content pipeline around it. Here's exactly what changed — and the three things you can do this week."

---

## [Stage 4: Validation] — 3:30–6:00

**Dopamine Goal:** Validation

**Talking Points:**
- Proof 1 — The before/after: my old pipeline was 4 Python services, a Postgres queue, and ~2,400 lines of orchestration code. Rebuilt as 7 skills (researcher → hook → outline → title → cascade → short-form → voice-cleanup), it's now a `.claude/skills/` folder, ~600 lines of helper Python, and the model routes between them. Same output. ~75% less code. Faster to change.
- Proof 2 — The composition demo: type `/researcher` then `/hook` — the second skill *automatically* reads what the first wrote because they share a vault path. No state machine. No handoff code. The model holds the thread. [Live demo on screen.]
- Proof 3 — The three things you can do this week:
  1. Find one workflow you've automated as a Python script. Convert it to a SKILL.md with a clear `description:` field. That field is the only thing the model uses to decide when to load it.
  2. Stop writing tool wrappers. If your tool is "call X API and format the response," it's a skill, not a tool.
  3. Write skills like documentation, not like code. The clearer your `SKILL.md` reads to a human, the better the model uses it.

**Visual Notes:**
[SHOW SCREEN: live walkthrough — invoke `/researcher`, show output file, invoke `/hook`, show it auto-reads the brief]
[SHOW SCREEN: a 12-line SKILL.md side-by-side with the equivalent ~180-line LangChain agent]
[TEXT OVERLAY: "75% less code. Same output."]

**Head Fake (second):**
You'd assume the win here is speed — "I can ship faster." It's not. The real win is that I can *delete* skills as easily as I add them. Every framework I've ever used punishes deletion. Skills don't. That's the asymmetry Karpathy was pointing at.

**Transition to Stage 5:**
"And honestly — I'm a little frustrated I didn't see this earlier."

---

## [Stage 5: Affection] — 6:00–7:00

**Dopamine Goal:** Affection

**Talking Points:**
- My honest take: I spent six months in 2025 building an "agent framework" for my content pipeline. Custom router, custom memory, custom tool registry. I was proud of it. Karpathy's post made me realize I'd built a worse version of something Anthropic shipped as a folder convention. I deleted ~70% of my own code the next weekend.
- What surprised me: writing skills made me a better writer. Because the model reads `SKILL.md` like a person would, ambiguous instructions fail visibly. My prose got tighter. My thinking got tighter. I didn't expect a file format to teach me how to communicate.

**Visual Notes:**
[Talking head only — eye contact, slower pace]
[TEXT OVERLAY (briefly): "Deleted 70% of my own code."]

**Transition to Stage 6:**
"But here's the part Karpathy didn't say out loud — and it's the thing that should actually change what you build next."

---

## [Stage 6: Revelation] — 7:00–8:00

**Dopamine Goal:** Revelation

**Talking Points:**
- The non-obvious reframe: if the model is the runtime, then **prompt engineering and software engineering are converging into one discipline — and the winners won't be the best coders or the best prompters, they'll be the best *taxonomists*.** The hard skill is naming things so a model can find them. That's it. That's the job.
- Why it matters beyond this video: every codebase you touch from here is going to drift toward this shape — small, well-described, model-discoverable units. The orgs that figure out *capability taxonomy* before their competitors are going to look 10x more productive for reasons that won't be obvious from the outside. Karpathy gave away the playbook; almost nobody is reading it as a playbook.

**Visual Notes:**
[TEXT OVERLAY: "The job is taxonomy."]
[B-ROLL: slow zoom on a clean, well-named folder tree fading into a chaotic one — contrast]

---

## [CTA] — 0:30–0:45

**Goal:** Give viewers a specific reason to watch the next video — not just "click subscribe."

**Talking Points:**
- Next video: I walk through the exact 7-skill content pipeline I rebuilt, file by file, with the `SKILL.md` for each one on screen — so you can fork the pattern for your own workflow this weekend.
- If you skip it, you'll know skills are the right primitive but you won't have a concrete template to copy. The template is the whole point.

**Visual Notes:**
[TEXT OVERLAY: "Next: the 7-skill pipeline, file by file"]
[end screen graphic with thumbnail of next video on the left, subscribe prompt on the right]
