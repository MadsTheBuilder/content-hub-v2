---
topic: Angles from the latest design tools research brief
date: 2026-05-24
research_source: 2026-05-21_open-source-design-tools_brief.md
provider: claude/cli
---

# Video Ideas — Angles from the latest design tools research brief

---

### Rank 1 — I Replaced Figma With a CLI Tool That Uses My Existing AI Agents

**Angle:** Open Design doesn't bundle its own AI — it detects whichever coding agent CLI you already have installed and delegates the entire design loop to it, meaning Claude Code, Codex, or Cursor becomes your design engine without any new subscription.

**Gap it fills:** Every "AI design tool" video assumes you'll pay for another proprietary AI. Nobody has explained a tool that parasitically leverages the AI tooling you already own — a genuinely different cost structure that creators are ignoring.

**Audience desire:** "Can I stop paying for so many AI subscriptions and still do design work?" — not "what design tools exist."

**Competitive signal:** design-extract (2,488 stars, 92 stars/day) shows massive appetite for design tooling that works from the command line. Open Design's README explicitly positions against Anthropic's Claude Design, meaning search intent already exists from people who looked up Claude Design and wanted a free alternative.

**Hook direction:** Open with the daemon running `which claude` and finding your Claude Code install — "This tool just found my Claude Code and is about to use it as a Figma replacement."

**Format recommendation:** Long-form 10-12min — the detection mechanism, adapter layer, and live demo need time; a short-form can't show the full prototype-to-export loop.

---

### Rank 2 — This Tool Extracts Any Website's Design System and Then Builds From It (design-extract + Open Design pipeline)

**Angle:** Chain design-extract (trending, 2,488 stars) to Open Design's 71 brand systems: scrape a competitor's design tokens in one command, import them as a DESIGN.md, then generate a matching prototype — a full reverse-engineering-to-prototype pipeline in under 5 minutes.

**Gap it fills:** Both tools are covered separately; nobody has shown them as a two-step pipeline. The design-extract README stops at export; Open Design's README stops at "bring your own brand." The bridge between them is an untouched video.

**Audience desire:** "How do I clone the look and feel of a site I like without starting from scratch in Figma?"

**Competitive signal:** design-extract's 2,488 stars in 30 days with 92 stars/day is one of the strongest trending signals in the design-tools niche. Pairing it with Open Design doubles the search surface area.

**Hook direction:** Show the terminal command extracting a well-known site's tokens, then immediately pipe them into Open Design generating a matching UI — "I just cloned Stripe's design system in 11 seconds."

**Format recommendation:** Long-form 8-10min — the pipeline has three distinct stages (extract, import, generate) that each need a beat.

---

### Rank 3 — HyperFrames: The Feature Nobody Has Explained Yet

**Angle:** Open Design's README lists "HyperFrames" as a first-class export type alongside HTML/PDF/PPTX/MP4, but there is zero documentation about what it actually is — making this the highest-novelty explainer available in the niche right now.

**Gap it fills:** The documentation gap IS the video. Any creator who figures out HyperFrames first owns the search term for months, because right now it returns zero results outside the repo.

**Audience desire:** "What is this thing and should I care?" — the question a developer asks when they see an unfamiliar term in a tool they're evaluating.

**Competitive signal:** Repos that introduce novel vocabulary in their README (HyperFrames, agent-native, surgical edits) generate disproportionate early-adopter interest. The 0 competing videos is a moat, not a red flag.

**Hook direction:** Open with the README bullet point, then say "I have no idea what a HyperFrame is — let's find out together by building one."

**Format recommendation:** Long-form 10-15min — discovery format requires showing dead ends and the eventual working demo; can be repurposed as a Short once the answer is established.

---

### Rank 4 — One Tool, 16 Different AI Coding Agents: How Open Design's Adapter Layer Works

**Angle:** Open Design maintains a daemon that normalizes output from claude-stream-json, acp-json-rpc, pi-rpc, and plain text into a single real-time UI stream — a concrete engineering pattern that any developer building multi-agent tools needs to understand.

**Gap it fills:** "Multi-agent compatibility" is discussed abstractly everywhere; nobody has walked through an actual adapter layer implementation that handles 16 different streaming formats. The `apps/daemon/src/agents.ts` file is the kind of real engineering content YouTube is starved of.

**Audience desire:** "How do I build something that works with multiple AI agents without rewriting it every time a new CLI drops?"

**Competitive signal:** The Agent Client Protocol (ACP) format used by Devin and Hermes is a standards-convergence story — first mover on explaining ACP for developer audiences has a long tail.

**Hook direction:** Show the streaming output from Claude Code vs Codex side by side — two completely different JSON formats — then show the adapter normalizing both into identical UI output.

**Format recommendation:** Long-form 12-15min — this is a technical deep dive; short-form can't convey the engineering insight.

---

### Rank 5 — Prompt → Web Prototype → MP4 Export in One Terminal Session (No Figma, No Canva)

**Angle:** A linear, no-cuts demo from a single text prompt to a working HTML prototype to a rendered MP4 export using only the terminal and an existing Claude Code install — the most concrete "does this actually work" video the niche is missing.

**Gap it fills:** AI design tool demos almost universally show the UI of a SaaS product, not the terminal. A terminal-first demo of a complete prototype-to-export pipeline has essentially no competition.

**Audience desire:** "Can I actually ship something with this, or is it just demos?" — the pragmatist's question that nobody is answering with real footage.

**Competitive signal:** MP4 as a design export target is unusual enough to generate curiosity clicks on its own. Viewers will watch just to understand what "a design tool that exports video" means.

**Hook direction:** Start the terminal session with nothing but a one-line prompt, then fast-forward to playing the MP4 at the end — "This is everything that happened between these two moments."

**Format recommendation:** Long-form 8-10min for the full walkthrough; cut a 60-second Short showing only the first prompt and the final MP4 playing.

---

### Rank 6 — Why Open Design Puts Your Design Files in `.od/projects/<id>/` (and What That Means for Your Workflow)

**Angle:** Open Design's local-first architecture means every prototype, design system, and export lives in a deterministic directory on your machine — making it version-controllable, diffable, and forkable in ways that no SaaS design tool can match.

**Gap it fills:** "Local-first" is treated as a vague philosophy in most videos. This video makes it concrete: show a `git diff` on a design change, a branch for a design variant, a `git blame` on a token decision — real developer workflows applied to design files.

**Audience desire:** "Can I treat my design work the same way I treat my code?" — a question developers have but rarely see answered with tooling.

**Competitive signal:** The local-first movement has strong search interest driven by privacy concerns and offline-first requirements. Pairing it with git workflows hits a developer audience that design content rarely serves.

**Hook direction:** Open with a `git log` showing design commits with real messages — "Your design history, your design branch, your design diff."

**Format recommendation:** Long-form 10-12min — the concept needs three concrete demos (diff, branch, fork) to land.

---

### Rank 7 — The SKILL.md Pattern: How Open Design Teaches 19 Different Design Skills to Any AI Agent

**Angle:** Open Design's skill injection system — native skill loading for Claude Code, `.cursorrules` for Cursor, prompt concatenation for others — is a transferable architectural pattern for anyone building tools on top of multiple AI CLIs.

**Gap it fills:** Skill/instruction injection for coding agents is a growing concern as teams adopt multiple AI tools. Most content treats it as a Claude-specific problem; this video abstracts the pattern across agents using Open Design as the worked example.

**Audience desire:** "How do I give my AI agent a specific skill without hardcoding it into every prompt?"

**Competitive signal:** The skill-injection pattern maps directly to how Claude Code skills (`SKILL.md`) work — which this project itself uses. Creators and developers building on top of Claude Code are a growing, underserved YouTube audience.

**Hook direction:** Show the same design skill running in Claude Code (via symlinked skill), then Cursor (via `.cursorrules`), then Codex (via stdin) — identical output, three different injection strategies.

**Format recommendation:** Long-form 10-12min — three injection strategies need side-by-side demo time.

---

### Rank 8 — Open Design vs Anthropic's Claude Design: The Fork That Puts You in Control

**Angle:** Open Design's README explicitly frames itself as an alternative to Anthropic's Claude Design — this is a direct comparison video with built-in search intent from anyone who googled "Claude Design" and found a paywall or waitlist.

**Gap it fills:** Comparison videos between the official Anthropic tool and the open-source fork do not yet exist because the fork is new. First-mover here captures both search audiences: people who found Claude Design, and people hunting for free alternatives.

**Audience desire:** "Is the free version good enough, or do I need to pay for the real thing?"

**Competitive signal:** OpenMythos (12,476 stars, 542/day) reconstructing Claude's internal architecture shows massive appetite for "open-source vs Anthropic official" content. The design tools niche is a smaller, less saturated version of the same demand.

**Hook direction:** Show both tools producing the same prototype from the same prompt — cost on screen ($0 vs $X) — "Let's find out if the free version is actually usable."

**Format recommendation:** Long-form 10-12min — a fair comparison needs both tools running; short-form risks being superficial and generating backlash.

---

### Rank 9 — How to Build a Brand Design System From Scratch Using Only a Text File and Your Terminal

**Angle:** Open Design's DESIGN.md format (brand tokens as a markdown file) means a complete design system is a text file you can write in 15 minutes — a beginner-accessible entry point that requires no design background, just a terminal.

**Gap it fills:** "Design systems" content assumes Figma or a SaaS platform. A terminal-first, text-first approach to brand tokens is essentially uncovered on YouTube — the audience it serves is developers who have always bounced off design tooling.

**Audience desire:** "I need my project to look consistent — how do I do that without learning Figma?"

**Competitive signal:** The 71 pre-built design systems in Open Design's repo signal that the maintainers already know this is a high-friction step; pre-building 71 of them is evidence of strong user demand for the shortcut.

**Hook direction:** Open a blank text file, type four lines of brand tokens (color, font, spacing, radius), run the tool — "Your design system just went from zero to prototype."

**Format recommendation:** Both — long-form 8-10min for the full system build; 60-second Short showing only the DESIGN.md → generated prototype moment.
