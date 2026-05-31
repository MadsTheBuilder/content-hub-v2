---
topic: make me a idea for a 10 min video 
date: 2026-05-29
research_source: 2026-05-21_open-source-design-tools_brief.md
provider: claude/cli
---

# Video Ideas — make me a idea for a 10 min video 

---

### Rank 1 — Your Coding Agent Already Has a UI Design Layer (You Just Don't Know It)

**Angle:** Reveal that open-design doesn't bundle its own AI — it delegates the entire design loop to the coding agent already installed on your machine, making every Claude Code or Cursor user an accidental design-system owner.

**Gap it fills:** Every "open source design tool" video treats it as a Figma replacement for designers. Nobody has made the video for the developer who already has Claude Code and has no idea it can be turned into a full design engine by installing one daemon.

**Audience desire:** "Can I ship polished UIs without hiring a designer or learning Figma?" — the real question is about removing the designer bottleneck, not the tool itself.

**Competitive signal:** Open design explicitly names Claude Code as its "reference implementation" with native skill-loading support. There is zero YouTube content explaining the nexu-io architecture to Claude Code's existing fanbase, which is growing weekly.

**Hook direction:** Open with your terminal running `open-design` and Claude Code generating a branded prototype — no Figma window, no designer in the room — and say "your coding agent has had this capability for months."

**Format recommendation:** Long-form 10-12 min — needs enough time to demo the daemon spawn, the skill injection, and the live prototype output to be credible.

---

### Rank 2 — I Built a Full SaaS UI in 10 Minutes Using Only My Terminal

**Angle:** Pure speed-run demo: topic input → brand design system selected from the 71 available → Claude Code generates a working HTML prototype → exported to PDF — all from the terminal, no GUI opened.

**Gap it fills:** Existing "build a UI with AI" videos all start in a browser-based tool. Nobody has shown the pure-CLI path from idea to exportable prototype.

**Audience desire:** "How fast can I actually ship a polished UI without a designer or a Figma subscription?" — they want proof it's fast before they invest time learning the tool.

**Competitive signal:** The research notes confirm 71 brand-grade design systems and HTML/PDF/PPTX/MP4 export. That combination — more than any single feature — is the hook: "pick a design system, get export-ready output."

**Hook direction:** Open with a real-time timer on screen and the challenge stated plainly: "I'm going to ship a branded SaaS landing page using only my terminal. The clock starts now."

**Format recommendation:** Long-form 10-15 min — the demo arc requires enough time to show each phase; compressing it loses the "wait, that actually worked" moment.

---

### Rank 3 — 71 Free Design Systems You Can Use From Your Terminal Right Now

**Angle:** Catalog-style video that walks through the variety inside open-design's 71 design systems — fonts, spacing tokens, color palettes — and shows how a single command switches your entire prototype's visual identity.

**Gap it fills:** Developers building side projects consistently under-design their work because they don't know where to start. Videos about design systems assume the viewer is already a designer. This one assumes they're a developer who wants a shortcut.

**Audience desire:** "What does my app look like if I don't have taste? Can a tool give me taste?" — the underlying fear is shipping something visually embarrassing.

**Competitive signal:** 71 is a specific, large number that creates credibility and curiosity simultaneously. No existing video has catalogued these or shown the switching mechanic in action.

**Hook direction:** Open by showing the same exact prototype rendered in three different design systems back-to-back in 10 seconds, then ask: "Which one would you ship?"

**Format recommendation:** Long-form 10 min — you need enough time to show enough systems that the viewer believes the claim, plus a walkthrough of how to switch.

---

### Rank 4 — The Open-Source Tool That Runs on 16 Different AI Agents (Here's Which One Wins)

**Angle:** Benchmark-style comparison using open-design's multi-agent adapter layer — run the same design task through Claude Code, Codex, and Cursor, show the output quality and speed differences, declare a winner.

**Gap it fills:** Agent comparison videos exist but always focus on code generation. Nobody has compared coding agents on UI/design output quality using a controlled test environment.

**Audience desire:** "Which AI agent should I be paying for?" — the viewer wants justification for their tool choice, or ammunition to switch.

**Competitive signal:** The research notes confirm that open-design normalizes 16 different agent output formats (claude-stream-json, acp-json-rpc, pi-rpc, plain text). This multi-agent substrate is unique and gives you a scientific-ish testing framework other comparison videos lack.

**Hook direction:** Show the same prompt running simultaneously in Claude Code and Codex, prototypes side by side, and open with: "I ran the same design task through 16 AI agents. Here's what actually shipped."

**Format recommendation:** Long-form 12-15 min — the comparison format requires enough agents to be credible; testing 3-4 deeply beats testing 8 shallowly.

---

### Rank 5 — How Your AI Agent Learns New Skills: SKILL.md and Native Skill Injection Explained

**Angle:** Technical explainer on how open-design symlinks SKILL.md files into Claude Code's native skills directory — teaching viewers the underlying mechanism that makes agent-native tools extensible, using design as the concrete example.

**Gap it fills:** Claude Code's skill system has almost no YouTube content explaining how it actually works under the hood. Most tutorials treat skills as a black box. This video makes the mechanism visible.

**Audience desire:** "How do I teach my AI agent to do something it doesn't know how to do?" — the real question is about extensibility, not design specifically.

**Competitive signal:** The research notes detail three distinct injection strategies (native skill loading, prompt injection, file-placed workflow). That specificity is rare — most AI tooling explainers stay at the surface. The audience that wants this level of detail has no existing resource.

**Hook direction:** Open by asking "What if you could give your coding agent a new capability in 30 seconds?" then immediately show a symlink being created and the agent picking it up on the next invocation.

**Format recommendation:** Long-form 10 min — technical audience tolerates length if the signal density is high; keep every minute payoff-dense.

---

### Rank 6 — What Are HyperFrames? The Prototype Format That Might Replace iframes

**Angle:** First explainer video on HyperFrames — open-design's sandboxed preview container — what they are, why sandboxing matters for AI-generated UI, and how the HTML/PDF/PPTX/MP4 export pipeline flows out of them.

**Gap it fills:** "HyperFrames" appears in the repo description with zero explanation anywhere on YouTube. Viewers who encounter the repo have no resource to understand what it does.

**Audience desire:** "Is AI-generated UI safe to embed in my app?" — the sandboxing angle addresses a real developer concern about running agent-generated code.

**Competitive signal:** The term "HyperFrames" combined with sandboxed preview and multi-format export is architecturally novel. Naming and explaining an unknown concept before others do creates a durable first-mover SEO advantage.

**Hook direction:** Open with "Every AI design tool gives you code you're afraid to run. Open Design solved that differently" and cut immediately to the sandbox preview in action.

**Format recommendation:** Long-form 10 min — concept definition + demo + implications structure; can't be rushed below 8 min without losing credibility.

---

### Rank 7 — Why "Bring Your Own AI" Is the Only Sane Model for Dev Tools in 2026

**Angle:** Opinion/thesis video arguing that tools bundling their own AI are obsolete — using open-design's delegation architecture as proof that the right pattern is detecting what the developer already has installed and routing through it.

**Gap it fills:** Nobody has made the meta-argument video for the agent-native tool paradigm. Existing opinion content either argues for specific agents or against specific vendors; nobody is arguing for the architectural pattern itself.

**Audience desire:** "Am I making the right choice with my current AI tool stack?" — the viewer wants validation or disruption of their current setup.

**Competitive signal:** The research notes quote directly: "We delegate the entire agent loop — model calls, tool use, context management, permission handling, resume, cancel — to the user's existing code agent CLI." That's a quotable design philosophy with real engineering backing.

**Hook direction:** Open with "Every AI startup is racing to build their own model. One team just said: we don't need one. And they're right."

**Format recommendation:** Long-form 10 min — opinion format needs enough depth to hold up to pushback; under 8 min reads as hot take, not argument.

---

### Rank 8 — From Zero to Exported Prototype: The Open Design Workflow for Developers Who Can't Design

**Angle:** End-to-end workflow tutorial targeting developers who ship ugly products — covering daemon setup, agent detection, design system selection, prototype generation, and final export in one complete run-through.

**Gap it fills:** Setup tutorials for open-design don't exist. The GitHub README explains architecture but not "here's what you do in the first 15 minutes." There's a gap between the repo's ambition and any accessible onboarding content.

**Audience desire:** "I want to see the whole thing before I commit to learning it" — the viewer wants a complete workflow preview before investing setup time.

**Competitive signal:** Every new tool needs a canonical "first-run" tutorial. Whoever makes it first owns that search query for the repo's lifetime. The repo is fresh with no competition on YouTube.

**Hook direction:** Open with "I'm a developer. I can't design. Here's the tool that stopped mattering" — position the video as the honest beginner's path, not a polished product demo.

**Format recommendation:** Long-form 12-15 min — tutorial format needs completeness; leaving steps out breeds frustration and negative comments.

---

### Rank 9 — How One Tool Supports 16 AI Agents Without Breaking: The Adapter Architecture Explained

**Angle:** Deep technical breakdown of the open-design daemon's adapter layer — PATH scanning, config-dir probing, capability negotiation, and the five output format normalizers — aimed at developers building their own multi-agent tools.

**Gap it fills:** Multi-agent tool builders have no reference architecture to study. Open-design's `apps/daemon/src/agents.ts` is a working, documented example of how to abstract over heterogeneous CLI output formats — and nobody has explained it on video.

**Audience desire:** "How do I build something that works with multiple AI agents without rewriting it every time a new one comes out?" — the viewer is a builder, not a user.

**Competitive signal:** The research notes detail the exact streaming format normalizers (claude-stream-json, acp-json-rpc, pi-rpc, plain). That level of implementation specificity is rare source material and creates a video that practitioners will bookmark and share.

**Hook direction:** Open with "Most AI tools hardcode one agent. This tool works with 16. Here's the 200 lines of code that make that possible."

**Format recommendation:** Long-form 10-12 min — narrow but high-intent audience; depth is the differentiator, not breadth.
