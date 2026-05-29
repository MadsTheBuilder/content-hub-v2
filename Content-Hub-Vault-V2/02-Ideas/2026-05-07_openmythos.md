---
topic: OpenMythos
date: 2026-05-07
research_source: 2026-05-06_ruflo_skills_agents_architecture.md
provider: claude/cli
---

# Video Ideas — OpenMythos

The research is already embedded in your message — running ideation directly from the provided notes.

---

### Rank 1 — "OpenMythos Explained: What It Actually Means to Reconstruct Claude's Architecture"

**Angle:** Goes beyond "what is this repo" to dissect *what theoretical reconstruction means in practice* — comparing OpenMythos's claims against Anthropic's published Constitutional AI papers to show exactly what's novel vs. what's reverse-engineered speculation.

**Gap it fills:** Every incoming video will be a surface-level "new open-source Claude!" explainer. None will answer the harder question: is this a genuine architectural blueprint or a well-organized guess? That gap is wide open.

**Audience desire:** "Can I actually build something that behaves like Claude using this, or is it vaporware?"

**Competitive signal:** 11,100 stars at 1,110/day velocity is top-3 in the 30-day chart, beating repos with months of runway. That spike is driven by people who want to understand it — not just star it.

**Hook direction:** "Anthropic has published exactly three papers that describe how Claude thinks. OpenMythos claims to reconstruct the rest. Here's what that actually means."

**Format recommendation:** Long-form 10-14min — the legitimacy question requires enough time to compare source material; a short-form version can't carry the evidence.

---

### Rank 2 — "OpenMythos vs ruflo: Training-Time vs Runtime — Two Completely Different Things"

**Angle:** Positions OpenMythos (a training-time/constitutional philosophy reconstruction) against ruflo's runtime orchestration layer — a distinction no existing video makes, but which is the key to understanding where each tool fits.

**Gap it fills:** Both repos are framed as "open-source Claude infrastructure" but they operate at entirely different layers. Conflating them is the single biggest misconception in coverage so far.

**Audience desire:** "I want to build Claude-like agents — which of these do I actually need?"

**Competitive signal:** ruflo's deep research (109 sources via NotebookLM) produced a four-layer stack model. OpenMythos is a peer artifact operating one level below that stack — the comparison is a natural editorial pairing that no one has made yet.

**Hook direction:** "Two repos blew up this month claiming to open-source Claude. One handles how Claude *thinks*. The other handles how Claude *works*. They're not the same thing — and mixing them up will break your stack."

**Format recommendation:** Long-form 8-12min — the architectural comparison needs a diagram and at least two code examples to be convincing.

---

### Rank 3 — "I Ran OpenMythos on Claude Code for 7 Days. Here's What I Found."

**Angle:** First-person practitioner trial — not a repo walkthrough but a structured experiment: what does an agent built with OpenMythos's principles actually do differently under stress?

**Gap it fills:** All current coverage will be repo-tours and star-count reactions. Nobody is doing empirical testing and reporting concrete behavioral differences.

**Audience desire:** "Does this actually change how the model behaves, or is it a README?"

**Competitive signal:** The ruflo research shows that Skills without tools are useless and tools without Skill instructions are dangerous — OpenMythos's value claim is at a higher abstraction level than either. Testing whether that claim survives contact with reality is exactly what viewers are waiting for.

**Hook direction:** "11,000 people starred this repo. I wanted to know if any of them actually ran it. So I did, for a week, and logged everything."

**Format recommendation:** Long-form 12-15min — the credibility comes from showing the experiment log, not just asserting conclusions.

---

### Rank 4 — "The Four Primitives That Make Claude Work — and How OpenMythos Adds a Fifth"

**Angle:** Uses the ruflo research's primitives framework (Skills, Agents, Slash Commands, Plugins) as the "runtime" layer, then positions OpenMythos as the missing "constitutional" primitive — the training-time philosophy that governs all the others.

**Gap it fills:** The ruflo primitives framework is dense and well-researched but disconnected from OpenMythos. Nobody has written the "complete picture" video that shows where each primitive sits in the full stack.

**Audience desire:** "How does Claude actually work end-to-end, from training to agent execution?"

**Competitive signal:** The comparison matrix from the ruflo notes (MCP = Hands, Skills = Brain, Agents = Workers, Plugins = Extension Packs) is a clean teachable structure. Adding OpenMythos as the "DNA" or "Constitution" layer completes the metaphor without forcing it.

**Hook direction:** "There are four things that make Claude Code work. Anthropic built a fifth one they didn't publish — and someone just reverse-engineered it."

**Format recommendation:** Long-form 10-12min — the framework needs to be built visually before OpenMythos's role is intelligible.

---

### Rank 5 — "kyegomez Keeps Shipping: What OpenMythos Tells Us About How He Works"

**Angle:** Profile-driven analysis of kye gomez's open-source pattern — Swarms, Zeta Alpha, now OpenMythos — to extract a replicable framework for "theoretical reconstruction" as a content and research strategy.

**Gap it fills:** The repo is already famous; the builder is less analyzed. Practitioner audiences want to understand the *method* behind viral open-source projects, not just the output.

**Audience desire:** "How does one person ship 10+ high-starred repos? What's the actual system?"

**Competitive signal:** OpenMythos at 1,110 stars/day is not a fluke — it follows a pattern. Documenting that pattern is original editorial work that no other channel has done.

**Hook direction:** "This is the third repo this builder has shipped that hit 10,000 stars. I went looking for the pattern."

**Format recommendation:** Long-form 10-12min — profile pieces need enough evidence to be convincing; this works better as a documentary-style narrative.

---

### Rank 6 — "What Anthropic Actually Published vs. What OpenMythos Claims to Reconstruct"

**Angle:** Line-by-line comparison: Anthropic's Constitutional AI paper, the model card, and the Claude Character Overview vs. OpenMythos's reconstruction — surfacing exactly where the reconstruction has evidence and where it's speculative.

**Gap it fills:** Nobody is doing primary source comparison. The video positions the creator as a researcher who read the actual papers, not just the README.

**Audience desire:** "How much of this is real and how much is made up?"

**Competitive signal:** This is the due-diligence video the 11,000 people who starred the repo haven't found yet. It's the second video a viewer watches after the explainer — and it performs better on search over time.

**Hook direction:** "Before you build anything on OpenMythos, you should know what Anthropic has actually confirmed about Claude's architecture — and what they haven't."

**Format recommendation:** Long-form 12-15min — source comparison is inherently dense; shortcuts undermine the credibility angle.

---

### Rank 7 — "Build a Constitutional Agent in 20 Minutes Using OpenMythos + Claude Code"

**Angle:** Fastest practical tutorial: wire OpenMythos's constitutional principles into a Claude Code agent using the ruflo Skills/Agents primitives, producing a working artifact in under 20 minutes of screen time.

**Gap it fills:** Existing tutorials will either be too abstract (philosophy only) or too narrow (just running the repo). Nobody is combining both into a single build-along that produces a usable output.

**Audience desire:** "How do I actually use this — give me something I can run today."

**Competitive signal:** The ruflo skill structure (`.claude/skills/<name>/SKILL.md`) maps directly to where OpenMythos principles would be applied. The integration path is clear from the research; it just hasn't been made into a tutorial yet.

**Hook direction:** "OpenMythos tells you how Claude is supposed to think. Here's how to actually make an agent that thinks that way — in 20 minutes."

**Format recommendation:** Both — long-form for the tutorial, 90-second short showing the finished agent running as a proof of concept.

---

### Rank 8 — "OpenMythos + MemPalace: The Open-Source Claude Infrastructure Stack Nobody Is Talking About"

**Angle:** Pairs the two highest-velocity Python repos from the 30-day chart — OpenMythos (architecture/constitution) and MemPalace (memory/retrieval) — as complementary infrastructure layers that together approximate what Anthropic runs internally.

**Gap it fills:** Both repos are covered in isolation. The combined stack angle — "here's the full open-source Claude infrastructure" — hasn't been articulated.

**Audience desire:** "What would it take to build a Claude-quality agent without Anthropic's infrastructure?"

**Competitive signal:** MemPalace at 50,278 stars (2,094/day) is the highest-velocity repo in the 30-day chart. A video that piggybacks on both audiences is a legitimate play — the overlap in viewer intent is high.

**Hook direction:** "Two repos blew up this month. One reconstructs how Claude thinks. The other reconstructs how Claude remembers. Together they're closer to the full picture than anything else out there."

**Format recommendation:** Long-form 10-12min — the combination requires enough architecture explanation to justify the pairing.

---

### Rank 9 — "Is OpenMythos the Claude Design Alternative We Actually Need?"

**Angle:** Reframes OpenMythos not as a Claude *replacement* but as a design tool — a constitutional framework that helps builders make better decisions about agent behavior before writing a single line of code.

**Gap it fills:** The default framing is "open-source Claude model." The underserved framing is "decision framework for agent designers" — a completely different audience with different search intent.

**Audience desire:** "How do I make my AI agents less erratic and more principled without fine-tuning a model?"

**Competitive signal:** The ruflo research explicitly flags that "a Skill without tools is useless and tools without Skill instructions are dangerous" — OpenMythos's constitutional layer is precisely the missing instruction layer that most agent builders skip. That pain point is real and documented.

**Hook direction:** "Most agent builders skip the hardest question: what should your agent *refuse* to do? OpenMythos is the first open framework that forces you to answer it."

**Format recommendation:** Short-form 60-90s as entry point (punchy reframe), long-form 8-10min for builders who want to implement it.
