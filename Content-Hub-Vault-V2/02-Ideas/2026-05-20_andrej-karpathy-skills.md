---
topic: Andrej Karpathy skills
date: 2026-05-20
research_source: research.md
provider: claude/cli
---

# Video Ideas — Andrej Karpathy skills

---

### Rank 1 — I Rebuilt Karpathy's "micrograd" in 150 Lines — Here's What Backprop Actually Is

**Angle:** Code along with Karpathy's 150-line autograd engine line-by-line, but stop every 20 lines to draw the computation graph on screen so viewers see backprop as a *data structure*, not a formula.

**Gap it fills:** Every "neural networks from scratch" video either dumps the math (MIT-lecture style) or hand-waves the autograd part ("PyTorch handles this"). Nobody walks through the DAG construction visually while typing the code.

**Audience desire:** "I've used `.backward()` a thousand times. What is it actually doing under the hood?" — they want the *mechanical* answer, not the calculus refresher.

**Competitive signal:** micrograd is explicitly designed by Karpathy as the teaching artifact (150 LOC, builds a DAG, used as the entry point of his "Zero to Hero" series). His own video on it is the most-viewed in the series — proves the appetite, and a tighter 12-min remix targets viewers who bounced off the 2.5-hour original.

**Hook direction:** "Karpathy's most-watched video is 2 hours 25 minutes long. I'm going to give you 80% of it in 12 minutes — starting with the one line of code that *is* backpropagation."

**Format recommendation:** Long-form 12-15min — needs screen-share code walkthrough; doesn't compress to shorts.

---

### Rank 2 — Karpathy Quit OpenAI Twice. Here's What He Built Each Time He Left

**Angle:** Treat Karpathy's career as a sequence of *bets* — OpenAI v1 → Tesla → OpenAI v2 → independent — and decode what each transition tells you about where AI is actually going.

**Gap it fills:** Existing Karpathy content is either tutorial (his repos) or hagiography ("AI legend"). No video maps his *job changes* as a leading indicator — and his moves have historically predicted the field's center of gravity (vision → autonomy → midtraining → education).

**Audience desire:** "Where should *I* be focusing if I want to be 18 months ahead?" — viewers use Karpathy as a proxy for "what matters next in AI."

**Competitive signal:** Research notes flag his 2023 return to OpenAI to build a "midtraining and synthetic data" team — a term most viewers haven't heard but will Google. That term alone is a SEO + curiosity-gap goldmine. His 2024 departure to do education full-time is also under-analyzed on YT.

**Hook direction:** "In 2017 Karpathy left OpenAI for Tesla. Six months later, every AI lab pivoted to autonomy. In 2024 he left OpenAI to teach. I think that's the signal."

**Format recommendation:** Long-form 10-12min — narrative + timeline graphics; the career-arc angle doesn't work in 60s.

---

### Rank 3 — What "Midtraining" Actually Is (and Why Karpathy Built a Team for It)

**Angle:** Define the unsexy middle stage of LLM training — between pretraining and RLHF — that almost no public explainer covers, using Karpathy's 2023 OpenAI team as the framing device.

**Gap it fills:** "Pretraining" and "RLHF" have 500 explainer videos each. "Midtraining" has near-zero. The research notes literally say the sources don't define it — that's the gap, audibly.

**Audience desire:** "I keep seeing terms like continued pretraining, instruction tuning, midtraining — what's the actual order and what does each one do to the model?" They want the org chart of LLM training, not a lecture.

**Competitive signal:** The research notes specifically call out that this term appears in Karpathy's bio but is undefined in available sources. A topic that's *named by a famous person* but *not yet explained on YouTube* is the rarest gap pattern there is.

**Hook direction:** "Karpathy went back to OpenAI in 2023 to build a team for something called 'midtraining.' Nobody on YouTube has explained what that is. Here's the answer."

**Format recommendation:** Both — 8min long-form for the full stack walkthrough, 60s short pulling just the one-sentence definition + the OpenAI hiring detail as the hook.

---

### Rank 4 — I Read Every Karpathy Repo So You Don't Have To (Ranked by What You'll Actually Learn)

**Angle:** A ranked tour of Karpathy's 6 educational repos (micrograd → makemore → nanoGPT → llama2.c → llm.c → char-rnn), scored on three axes: how much you learn per hour, how hard it is to follow, and what concept it unlocks.

**Gap it fills:** Viewers know "Karpathy has good repos" but don't know the *order* to do them in or which ones are obsolete (char-rnn) vs. still cutting-edge (llm.c). Existing content reviews individual repos in isolation.

**Audience desire:** "I have 20 hours this month to get serious about understanding LLMs. Where do I start, and what's the path?"

**Competitive signal:** The research notes list 6 repos by name with explicit LOC counts and stated educational intent — this is a topic where the source material is unusually well-structured for a ranked-list format, and "learning path" videos consistently overperform in the AI niche.

**Hook direction:** "Karpathy has six teaching repos. Five of them are great. One of them you should skip entirely. Here's the order."

**Format recommendation:** Long-form 10min — needs the comparison table on screen; shorts version would lose the ranking payoff.

---

### Rank 5 — Karpathy's "Software 2.0" Essay Predicted Cursor, Copilot, and Claude Code in 2017

**Angle:** Re-read the 2017 "Software 2.0" essay with 2026 hindsight and show which specific paragraphs predicted the agentic-coding tools that now dominate. Read the essay on screen; pause to point at modern equivalents.

**Gap it fills:** "Software 2.0" gets cited constantly but almost no one has done a line-by-line walk-through of *what the essay actually claimed* vs. what shipped. Most references are name-drops.

**Audience desire:** "Is the 'AI replaces code' thesis hype or has it actually played out?" — viewers want a scorecard, not another opinion.

**Competitive signal:** The research notes explicitly flag Software 2.0 as one of his most influential posts. Essays that have aged well are evergreen YouTube — they generate views for years because every new AI tool resurfaces the citation.

**Hook direction:** "Nine years ago Karpathy wrote a 2,000-word essay that called every AI coding tool we use today. I'm going to read it with you and point at the parts that came true."

**Format recommendation:** Long-form 12min — needs the on-screen essay; pairs well with a 90s short pulling the single most prophetic paragraph.

---

### Rank 6 — Why Karpathy Writes Everything in 700 Lines of C (And Why You Should Care)

**Angle:** Use llama2.c (a full LLM in one 700-line C file) and llm.c (pretraining in pure C/CUDA) to argue Karpathy's actual *skill* — and the one most engineers miss — is **aggressive simplification**, not ML expertise.

**Gap it fills:** Tutorials show *what* his repos do; nobody examines *why* he keeps stripping away frameworks. The meta-skill of "delete dependencies until the algorithm is visible" is the real takeaway and it's never the headline.

**Audience desire:** "How do I think more clearly about systems I don't fully understand?" — disguised as a Karpathy video.

**Competitive signal:** Research notes show llama2.c was described by Karpathy himself as a "weekend project" and called out for its 700-LOC compactness — that exact framing is a hook. The "single-file" aesthetic (also seen in nanoGPT, micrograd) is a recurring pattern with strong story potential.

**Hook direction:** "Karpathy's entire LLaMA implementation is one C file. 700 lines. No PyTorch, no NumPy, nothing. That's not a flex — it's a philosophy. Here it is."

**Format recommendation:** Long-form 8-10min — philosophy + code visual; doesn't need to be longer.

---

### Rank 7 — I Asked Karpathy's char-rnn From 2015 to Write Code in 2026. Here's What Happened

**Angle:** Resurrect char-rnn (his 2015 character-level RNN, the one from "Unreasonable Effectiveness of RNNs"), train it on modern code, and benchmark it against a modern 1B transformer. Visceral demonstration of what 10 years of architecture progress actually bought us.

**Gap it fills:** Every "RNN vs Transformer" video is theoretical. Nobody has done the *actual head-to-head* using Karpathy's own historical artifact as the baseline.

**Audience desire:** "How much of the LLM revolution was scale vs. architecture?" — the most debated question in AI, answerable empirically.

**Competitive signal:** char-rnn is the artifact behind one of the most-cited AI blog posts ever ("The Unreasonable Effectiveness of Recurrent Neural Networks"). Reviving it has built-in nostalgia + clickability. Comparison-experiment videos consistently overperform explainer videos in this niche.

**Hook direction:** "In 2015 Karpathy trained a tiny neural net on Shakespeare and it stunned the AI world. I just trained the same model on Python code. The result is... not what I expected."

**Format recommendation:** Long-form 10-12min — needs the experiment setup and result reveal; shorts version captures only the punchline.

---

### Rank 8 — Karpathy Taught the First Deep Learning Class at Stanford. Here's the Free Replacement in 2026

**Angle:** Walk through how to replicate the CS231n experience for free in 2026 using Karpathy's own YouTube series + 3 specific newer resources, with a week-by-week study plan.

**Gap it fills:** "How do I learn deep learning" videos are oversaturated but generic. A *specific* Karpathy-anchored curriculum with a calendar is rare and high-utility.

**Audience desire:** "I want a structured, free, no-bullshit path from zero to actually understanding modern LLMs. Tell me exactly what to do for 8 weeks."

**Competitive signal:** Research notes confirm CS231n grew from 150 to 750 students in 2 years — that demand signal is durable, and the audience that wanted CS231n is now adults on YouTube. "Zero to Hero" series view counts also validate the curriculum-style format.

**Hook direction:** "Stanford charges $60,000 a year for the class Karpathy invented. The whole thing is now on YouTube for free — but in the wrong order. Here's the order."

**Format recommendation:** Long-form 8min — needs the week-by-week graphic; works as evergreen lead-magnet content.

---

### Rank 9 — Building a Mini-Karpathy: The 5 Skills That Make Him Uncopyable

**Angle:** Reverse-engineer Karpathy as a *skill stack* — not a genius — and break down the 5 specific learnable skills (live-coding while explaining, single-file architectures, distillation writing, framework-agnostic teaching, public-build cadence) any engineer can adopt.

**Gap it fills:** "Why is Karpathy great" content is fan-service. A practitioner-to-practitioner breakdown of the *transferable* skills — written for engineers who want to develop those same skills — doesn't exist on YouTube.

**Audience desire:** "I admire this person. What do they do that I could start doing on Monday?"

**Competitive signal:** Across the entire research brief, the recurring pattern is *minimalism + clarity + public artifacts* — micrograd, llama2.c, nanoGPT, blog posts, YouTube. That pattern is the actual story and no existing video tells it as a skill framework.

**Hook direction:** "Karpathy isn't a 1-in-a-million talent. He just stacked five skills almost nobody bothers with. Here's the stack — and how to start building it this week."

**Format recommendation:** Both — 10min long-form for the full breakdown, 60s short on just the #1 skill as a teaser.
