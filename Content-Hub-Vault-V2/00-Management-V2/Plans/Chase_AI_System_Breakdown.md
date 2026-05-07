# Chase AI Content System — Detailed Section Breakdown
*Annotated with user comments. All sections confirmed must-have unless noted.*

---

## What a "Claude Code Skill" Actually Is
Before the sections — since this comes up repeatedly:

A skill is a `.claude/skills/<name>/SKILL.md` file. When Claude Code reads it, `/name` becomes a slash command in your terminal. Optionally paired with a `skills/<name>.py` Python helper for things like API calls, file writes, or external integrations. That's the entire pattern. No framework, no server, no config file.

---

## Phase 0b — GitHub Trending Script (Fountainhead #2)
**Status: Must-have. Build this first.**

**What it is:** A daily script that surfaces fresh, trending AI/tech repos before they hit YouTube. Solves "what do I talk about today" for the tech niche in ~30 lines of Python.

**Tools:**
- Python script (Claude Code writes it once)
- GitHub public trending page or API
- Obsidian vault (output destination — markdown file)

**Flow:**
1. Script runs every morning (scheduled via cron or Windows Task Scheduler)
2. Pulls top 10 trending AI repos created in the **last 7 days**
3. For each repo: star count, star velocity, language, link, description
4. Also shows top 5 trending for the current **month**
5. Claude's daily pick — one repo flagged as most worth covering, with reasoning
6. Written as a single markdown file into Obsidian vault

**Why it's first:** No external accounts, no API keys beyond GitHub (optional — public data works), no services. One script, one file, runs daily. Gives you a fresh content feed every morning.

**User comment:** "Scraping git trending is a good call — always keeping me up to date and good fresh ideas that are up to date for video generation."

---

## Phase 0a — Twitter Scraping Web App (Fountainhead #1)
**Status: Must-have. Easiest to implement per user.**

**What it is:** A web app built with Claude Code that delivers scored, niche-relevant tweets to Telegram every 45 minutes.

**Tools:**
- Claude Code (builds the app)
- Apify tweet scraper (cheap — handles the actual scraping)
- Supabase (stores tweets + reply history + scores)
- Telegram bot (delivery to phone)
- Grok API (auto-drafts reply suggestions)
- Twitter API (enables replying from within the app)

**Flow:**
1. Randomised timer fires every ~45 minutes
2. Apify scrapes 40–90 tweets matching configured keywords + author accounts
3. Each tweet scored on: **velocity**, **authority**, **timing**, **opportunity**, **replyability**
4. All tweets written to Supabase (prevents repeats, ensures diversity)
5. Softmax converts scores to a probability distribution → selection isn't always the top scorer (deliberate randomisation)
6. Winning tweets pushed to Telegram with: text, like count, velocity score, Grok-drafted replies
7. Can reply via Telegram → Twitter API posts it
8. Reply history stored and scored in Supabase → system improves over time

**Key detail:** The softmax step is subtle but important. Always picking the highest-scored tweet would create a feedback loop of the same authors. Softmax keeps it diverse while still being signal-led.

**User comment:** "Most important and easiest to implement — this is a must have."

---

## Phase 0c — Telegram Saved Messages (Fountainhead #3)
**Status: Must-have. Personal curation feed.**

**What it is:** A Telegram bot that watches your Saved Messages for YouTube/Instagram/TikTok URLs you share to yourself, scores them, and adds them to the content idea pool.

**Background:** Instead of sharing interesting videos to Instagram DMs (no accessible API), redirect the same habit to Telegram Saved Messages — functionally identical (message yourself a link) but fully automatable.

**Tools:**
- Telegram Bot API (watches Saved Messages in real time)
- Supabase (stores URLs + scores alongside Twitter feed)
- Optional: YT Pipeline trigger (auto-queue for analysis)

**Flow:**
1. You share an interesting video link to Telegram Saved Messages (same habit, different app)
2. Bot detects new URL, extracts platform + video ID
3. Scores it (source authority, topic relevance to configured keywords)
4. Written to Supabase alongside Twitter-sourced ideas
5. Appears in your daily content idea queue for review

**User comment:** "I have a habit of sharing myself videos on Instagram about Claude Code, tools, repos — want these scored and added to the list of video ideas."

---

## Phase 1 — YT Pipeline Skill (Research)
**Status: 100% must-have.**

**What it is:** A higher-order Claude Code skill — a skill that calls other skills. One slash command that goes from "here's a topic" to "here's a full NotebookLM analysis in your Obsidian vault."

**Skill structure:**
- `SKILL.md` — the slash command instructions
- Calls `notebooklm-py` CLI as a subprocess
- Output written to Obsidian vault

**Tools:**
- `notebooklm-py` CLI tool (the bridge — install once, use everywhere)
- NotebookLM / Gemini (does all analysis on Google's servers)
- Obsidian vault (output destination)

**How notebooklm-py works (the core primitive):**
- CLI wrapper for the NotebookLM API
- Pass it any source: YouTube URL, PDF, document, article
- NotebookLM processes it on Google's compute — **zero Claude token cost**
- Returns: analysis, summaries, slide decks, video overviews, images — everything available in the NotebookLM web UI

**How the YT Pipeline skill wraps it:**
1. Type the topic in conversation with Claude Code
2. Skill finds relevant YouTube URLs for that topic (sourcing)
3. Feeds them to `notebooklm-py` (analysis)
4. Gets analysis back and writes it to Obsidian vault as markdown
5. Related notes in the vault become cross-linked automatically

**Key detail:** This skill is also how the Callaway "training" is done. See next section.

**User comment:** "100% must have."

---

## The Callaway Ingestion — How It Works
**Status: One-time setup. No moving parts.**

The transcript says Chase "did this whole setup on a bunch of Callaway's videos and then incorporated that into how I have Cloud Code approach hooks and outlines and titles." He doesn't explain the mechanism, but based on his own system it's almost certainly this:

**The method:**
1. Collect Callaway's video URLs (the ones that best demonstrate hook/outline/title craft)
2. Run the YT Pipeline skill on those URLs
3. NotebookLM analyses the videos and extracts the frameworks — hook structures, pacing patterns, title formulas, outline logic
4. That analysis lands in Obsidian as `callaway-hooks.md`, `callaway-titles.md`, etc.
5. The hook, outline, and title skills reference those Obsidian files as context when generating

**Why this is simple:** You're using the same YT Pipeline skill you already built. The system eats itself. Callaway's methodology becomes a set of reference notes in Obsidian, and every skill that needs it just reads those notes.

**No fine-tuning, no model training, no complexity.** Just: run YT Pipeline on Callaway URLs → get structured notes → reference them in skill prompts.

---

## Phase 2 — Ideation Skill
**Status: Must-have.**

**What it is:** A Claude Code slash command that reads existing Obsidian research and returns ranked video ideas placed in the competitive landscape. Strategy, not more research.

**Skill structure:**
- `SKILL.md` — instructions for the slash command
- `prompts/ideation.md` — the actual prompt (single source of truth)
- Reads from Obsidian vault, writes output back to vault

**Tools:**
- Claude (reads and reasons over Obsidian markdown files)
- Obsidian vault (input: research notes; output: ranked ideas + competitive analysis)

**Flow:**
1. Invoke `/ideation` after research is complete in Obsidian
2. Skill reads existing research notes for the topic
3. Analyses competitive landscape: what angles are saturated, what's been overdone
4. Finds open gaps — things no one's covered well
5. Identifies performance outliers — what has worked unusually well in this space
6. Maps each idea to audience desire ("why would someone want this")
7. Returns: ~9 ranked video ideas with titles, angles, formats, competitive reasoning
8. Output written to Obsidian

**Why it's separate from `/researcher`:** Research answers "what is true about this topic." Ideation answers "given what's true and what everyone else has done, what's the smartest angle?" These are different questions. Merging them skips the gap-finding step.

**User comment:** "Must have."

---

## Phase 3a — Hook Skill
**Status: Must-have.**

**What it is:** Drafts the first ~30 seconds of the video. The only part Chase fully scripts. The highest-leverage 20 seconds of the entire production.

**Skill structure:**
- `SKILL.md` — slash command
- `prompts/hook.md` — prompt built on Callaway framework (see Callaway Ingestion above)
- Reads: current video angle from conversation + Callaway notes from Obsidian

**Tools:**
- Claude (drafts the hooks)
- Obsidian vault (Callaway reference notes as context)

**Flow:**
1. Invoke `/hook` with chosen video concept
2. Skill reads Callaway framework notes from Obsidian as context
3. Generates 5 hook variations
4. Each variation has 3 components:
   - **Spoken hook** — exact words, out loud
   - **Visual hook** — what's on screen while speaking
   - **Text overlay** — on-screen text (primarily for short-form)
5. Iterate with Claude until satisfied
6. Final hook scripted verbatim before filming

**Why 5 variations:** Forces a choice — Chase says "I end up doing some variant of what it gives me, not the exact thing." Options create better outcomes than single outputs.

**User comment:** "Must have."

---

## Phase 3b — Outline Skill
**Status: Must-have.**

**What it is:** The structural skeleton of the full video. Not a word-for-word script — a map of sections, talking points, visual aids, and source references.

**Skill structure:**
- `SKILL.md` — slash command
- `prompts/outline.md` — prompt built on Callaway framework
- Reads: video concept + all related Obsidian research notes

**Tools:**
- Claude
- Obsidian vault (reads research notes; output written back to vault)

**Flow:**
1. Invoke `/outline` after hook is locked
2. Skill reads chosen angle + all related Obsidian research
3. Returns outline with per-section:
   - Target section length
   - General idea + core concept
   - Talking points
   - Potential visual aids (e.g., specific Excalidraw diagrams)
   - Source material to show on screen
   - Related Obsidian documents to reference during filming
4. Written to Obsidian

**Key detail:** The outline connects back to the vault — it surfaces which specific research notes apply to each section. During filming you can glance at the outline and know exactly what to reference.

**User comment:** "Must have."

---

## Phase 3c — YouTube Title Skill
**Status: Must-have.**

**What it is:** Generates title options calibrated to historical performance — not generic advice, but titles modelled on what has actually worked for your specific audience.

**Skill structure:**
- `SKILL.md` — slash command
- `prompts/title.md` — prompt with tier system
- Reads: current video concept + historical title + view count data (stored in Obsidian or a data file)

**Tools:**
- Claude
- Historical title/view count data (your own channel — provided once as input)

**Flow:**
1. Invoke `/title` with the video concept
2. Skill reads all historical titles + their view counts
3. Returns **Tier 1 titles** — safe bets, modelled on proven past titles with reasoning + comparable video cited
4. Returns **Tier 2 titles** — calculated risks, flagged explicitly for A-B testing
5. Returns **thumbnail text options** in the same tier format

**Key detail:** The personal historical data is what makes this skill non-generic. Without your own title history, it defaults to general patterns. With it, it's tuned to your audience specifically.

**User comment:** "Must have."

---

## Phase 4a — Content Cascade Skill
**Status: Must-have.**

**What it is:** Takes the uploaded YouTube video and generates text content for 3 platforms automatically. One command → blog + Twitter thread + LinkedIn.

**Skill structure:**
- `SKILL.md` — slash command
- `skills/cascade.py` — Python helper for: YouTube transcript extraction, blog auto-post, Twitter API post
- `prompts/cascade.md` — voice-tuned prompt

**Tools:**
- YouTube transcript API (auto-extract — no manual work)
- Website CMS / blog API (auto-posts blog)
- Twitter API (posts thread on approval)
- Claude (generates all text in creator's voice)

**Flow:**
1. Invoke `/cascade` with YouTube URL after upload
2. Skill auto-pulls transcript
3. Generates SEO blog post: embeds video, adds metadata, auto-posts to website
4. Generates Twitter thread (7 tweets + replies), posts after approval
5. Generates LinkedIn post variations for manual review

**Blog strategy (important):** Not about article quality — about compounding SEO. As the content library grows, so does Google search visibility. Each post is a permanent asset, not a one-off distribution.

**Voice training:** Fed with your own writing. Actively avoids AI-isms.

**User comment:** "Must have."

---

## Phase 4b — Short Form Skill
**Status: Must-have.**

**What it is:** Distils long-form video into scripts for 30/60/90 second vertical content. Not clipping — re-scripting for the format.

**Skill structure:**
- `SKILL.md` — slash command
- `prompts/short-form.md` — prompt for format-specific condensing

**Tools:**
- Claude
- Existing long-form transcript/outline from Obsidian (already built)

**Flow:**
1. Invoke `/short-form` pointing at the long-form transcript
2. Identifies highest-density ideas for vertical format
3. Returns scripts for 30 / 60 / 90 sec with: opening hook, caption/text overlay suggestions, condensed talking points

**Key detail:** All the work was already done for the long-form. This skill just compresses it. Combined with Content Cascade: 1 YouTube video → 6 platforms.

**User comment:** "Must have."

---

## Phase 4c — Voice Cleanup Skill
**Status: Must-have.**

**What it is:** Polish pass that removes AI-generated language patterns and rewrites in the creator's authentic voice. Run on output from any other skill.

**Skill structure:**
- `SKILL.md` — slash command
- `prompts/voice-cleanup.md` — trained on creator's writing, lists specific patterns to avoid

**Tools:**
- Claude
- Creator's writing corpus (provided once as context/examples)

**Flow:**
1. Invoke `/voice-cleanup` on any skill output
2. Removes AI-isms (the "it's not X, it's Y" pattern and similar)
3. Rewrites to match documented voice
4. Returns clean, human-sounding version

**User comment:** "Must have."

---

## Operating Philosophy — The Collaborator Model
**Status: Must-have. "The most important part — proves verification of content."**

This is the architecture of HOW you use the system, not what it does.

**The rule:** Review Claude's output at every phase boundary before advancing. Not optional — this is what prevents generic output.

**Phase boundaries (human checkpoints):**
- After Phase 0: pick a topic from Telegram/Obsidian feed
- After YT Pipeline: read the research, decide what angle to explore
- After Ideation: pick one idea from the ranked list, modify as needed
- After Hook: approve or iterate before moving to outline
- After Outline/Title: confirm before filming
- After Content Cascade: approve Twitter thread before it posts
- After Short Form: review scripts before recording

**What AI handles:** Research, competitive analysis, hooks, outlines, titles, distribution text
**What human handles:** Direction, creative judgment, filming, final approval at each step

**The result:** "90 jabs, no haymakers." Consistent, repeatable output that compounds.

---

## Build Order (all must-have)

| Priority | Skill | Reason |
|---|---|---|
| 1 | GitHub trending script | No dependencies, closes Phase 0 immediately |
| 2 | YT Pipeline + notebooklm-py | Core research primitive, needed before everything else |
| 2 | Callaway ingestion (via YT Pipeline) | One-time setup, unlocks hook/outline/title quality |
| 3 | `/cascade` + `/short-form` + `/voice-cleanup` | Distribution layer — builds fastest, proves end-to-end |
| 4 | `/ideation` | Needs research notes in vault to be useful |
| 5 | `/hook` + `/outline` + `/title` | Needs Callaway notes in vault + ideation output |
| 6 | Twitter scraping web app | External dependencies (Apify, Telegram) — last once local system is running |
| 6 | Telegram Saved Messages bot | Pairs with Twitter scraper, same Supabase pool |
