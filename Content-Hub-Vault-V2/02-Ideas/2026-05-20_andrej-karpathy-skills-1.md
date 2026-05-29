---
topic: andrej-karpathy-skills_1
date: 2026-05-20
research_source: research.md
provider: claude/cli
---

# Video Ideas — andrej-karpathy-skills_1

---

### Rank 1 — Karpathy's 2% Rule: Why He'd Reject Your Pull Request

**Angle:** Frame the 2% Rule as a concrete decision filter every engineer can apply tomorrow, not a philosophical quote — walk through real PRs (yours or open-source) and judge them against it.

**Gap it fills:** Existing Karpathy content quotes the rule but never operationalizes it. Viewers leave inspired but don't change how they review code.

**Audience desire:** "How do I know when 'cleaner' is actually better than 'faster'?" Engineers want a defensible heuristic for fighting complexity in code reviews.

**Competitive signal:** The 2% Rule is explicitly called out as a follow-up question in the research — meaning the surface-level Karpathy explainers leave viewers asking exactly this. The llm.c README itself is the source, which most videos don't reference.

**Hook direction:** Open on a side-by-side: 500 lines of optimized CUDA vs. 50 lines of readable C — "One of these is 2% faster. Karpathy ships the other. Here's why that decision will save your codebase."

**Format recommendation:** Long-form 8-15min. The rule needs worked examples (PR walkthroughs, before/after diffs) to land — too dense for short-form.

---

### Rank 2 — I Tried Karpathy's "Manual Backprop" Drill. It Broke My Mental Model.

**Angle:** First-person execution of the Zero-to-Hero manual backprop exercise — show the moment intuition clicks, with the specific scalar-to-tensor transition that trips everyone up.

**Gap it fills:** Most Zero-to-Hero reaction videos summarize the curriculum. Nobody films themselves *doing* the drill and showing what changed in their understanding of gradient flow.

**Audience desire:** "Will this actually teach me something PyTorch hides, or is it just academic?" Viewers want proof the exercise pays off before investing 6 hours.

**Competitive signal:** Research notes explicitly cite "backpropagate manually without using PyTorch autograd" as a core Karpathy pedagogy. Zero-to-Hero has millions of views but reaction/execution content is thin.

**Hook direction:** "I thought I understood backprop. Then I tried to do it without autograd for the first time and realized I'd been bluffing for three years."

**Format recommendation:** Both. Long-form for the full exercise walkthrough; 60s short pulled from the "aha" moment for top-of-funnel.

---

### Rank 3 — minGPT vs nanoGPT vs llm.c: Which Karpathy Repo Should You Actually Read?

**Angle:** A decision tree based on what you're trying to learn — not a feature comparison, but a "if you want X, read Y, skip Z" guide with reading order.

**Gap it fills:** Existing videos treat the three repos as a chronological evolution. Nobody answers the actual viewer question: which one do I open first as someone with my background?

**Audience desire:** "I have 4 hours. Where do I get the highest learning ROI?" Self-taught ML engineers want a sequencing strategy, not a comparison chart.

**Competitive signal:** Research notes flag the explicit minGPT (300 lines, education) → nanoGPT (teeth) → llm.c (raw C) progression as a distinct Karpathy theme. The "teeth vs education" distinction is in the source material and rarely surfaced.

**Hook direction:** "Karpathy has three repos that teach GPT from scratch. Reading them in the wrong order will waste your weekend. Here's the sequence."

**Format recommendation:** Long-form 8-15min. Needs code on screen and side-by-side file structure — short-form can't carry it.

---

### Rank 4 — Karpathy's "Allergy to 500-Pound Websites" Explains Why Modern Codebases Are Broken

**Angle:** Use the personal-website quote as the entry point to a wider thesis: framework bloat is a values problem, not a tooling problem — then apply the lens to ML stacks.

**Gap it fills:** The quote gets shared as a meme. No video has used it as a serious frame for evaluating PyTorch, LangChain, or modern ML infrastructure.

**Audience desire:** "Am I crazy for thinking the tooling is over-engineered?" Senior engineers want validation and a vocabulary for pushing back on stack bloat.

**Competitive signal:** Research notes pull the "seriously allergic to 500-pound websites" quote and link it directly to his preference for raw C/CUDA in llm.c. The values-to-code thread is undeveloped in existing content.

**Hook direction:** "Karpathy's personal website is one HTML file. His LLM training code is one C file. This isn't aesthetic — it's a thesis about software, and most of us have it backwards."

**Format recommendation:** Long-form 8-15min. Opinion essays need room to build the argument.

---

### Rank 5 — "Don't Tell It What to Do. Give It Success Criteria." — Karpathy's One Rule for Coding With LLMs

**Angle:** Take the verifiable-goals principle and apply it to Claude Code / Cursor workflows in real time — show the same task with imperative vs. goal-driven prompts and the difference in output.

**Gap it fills:** LLM coding tutorials default to imperative prompts. The verifiable-goals shift is in Karpathy's writing but nobody's filmed the A/B.

**Audience desire:** "Why does my AI coder go off the rails on tasks longer than 10 minutes?" Engineers want a prompt structure that scales beyond toy examples.

**Competitive signal:** Research notes explicitly extract "Don't tell it what to do, give it success criteria and watch it go" as a Karpathy engineering principle. This maps directly onto current AI-coding pain points with strong search intent.

**Hook direction:** "I gave Claude the same task two ways. One produced 400 lines of garbage. The other passed every test on the first run. The difference is one sentence Karpathy wrote."

**Format recommendation:** Both. Long-form for the demo; 60s short showing the prompt diff and outcome — perfect for AI-coding feed clips.

---

### Rank 6 — The Tesla Years: What Karpathy Learned About Data That Most ML Engineers Never Will

**Angle:** Zoom in on the in-house data labeling + synthetic data pivot — what production-scale data pipelines teach you that research code never can.

**Gap it fills:** Karpathy retrospectives focus on Autopilot architecture. The data-centric lessons (labeling org design, synthetic data tradeoffs) are rarely the topic.

**Audience desire:** "Why do FAANG ML engineers keep saying 'data > model'?" Mid-level engineers want the concrete reason, with examples.

**Competitive signal:** Research notes flag "in-house data labeling" at Tesla and "midtraining and synthetic data generation" at OpenAI 2023-2024 as a distinct through-line. This is one of the least-covered angles in Karpathy content.

**Hook direction:** "Karpathy left OpenAI for Tesla, then went back. The reason he gave wasn't about models. It was about data — and it explains everything wrong with how you train networks."

**Format recommendation:** Long-form 8-15min. Needs storytelling and timeline structure.

---

### Rank 7 — Read Activations Like a Doctor Reads X-Rays: Karpathy's Network Diagnosis Method

**Angle:** A tutorial on forward-pass activation statistics and backward-pass gradient inspection — the specific signals Karpathy looks at and what each one means when it goes wrong.

**Gap it fills:** "How to debug training" videos focus on loss curves. The activation/gradient statistics layer is in Karpathy's lectures but never extracted as a standalone diagnostic skill.

**Audience desire:** "My loss is going down but the model is bad — what do I check?" Practitioners want a debugging checklist beyond "lower the learning rate."

**Competitive signal:** Research notes specifically cite "statistics of the forward pass activations" and "backward pass gradients" and "pitfalls when [activations] are improperly scaled" as a Karpathy diagnostic philosophy. High utility, low coverage.

**Hook direction:** "If your model trains but doesn't work, you're not reading the right signal. Karpathy has a 4-statistic checklist he runs every time — and almost nobody copies it."

**Format recommendation:** Long-form 8-15min. Code-on-screen tutorial format.

---

### Rank 8 — "Interpretable Cells": The Karpathy Paper That Predicted Mechanistic Interpretability

**Angle:** Revisit the RNN visualization work (cells tracking quotes, brackets, line lengths) and trace the line from there to today's circuits / SAE interpretability research.

**Gap it fills:** Modern interpretability content starts with Anthropic / OpenAI 2024 work. Almost nobody connects it back to Karpathy's 2015-era visualizations as the lineage.

**Audience desire:** "Where did mechanistic interpretability actually come from?" Curious engineers want the intellectual history, not just the latest paper.

**Competitive signal:** Research notes cite the specific "line lengths, quotes and brackets" interpretable-cell finding. This is a deep cut that ties to one of the hottest current research threads.

**Hook direction:** "In 2015, Karpathy found a single neuron in an RNN that was counting quote marks. Ten years later, that finding became a field. Here's the line from there to here."

**Format recommendation:** Long-form 8-15min. Historical narrative needs runtime.

---

### Rank 9 — Why Karpathy Writes LLMs in Raw C in 2026 (And You Probably Shouldn't)

**Angle:** Honest take on the llm.c project — what it teaches, what it doesn't, and when "drop the framework" is genuinely useful vs. when it's larping.

**Gap it fills:** llm.c content is hagiographic. No video honestly assesses when raw-C reimplementation actually changes your engineering skill vs. when PyTorch is the right answer.

**Audience desire:** "Should I actually do this exercise or just watch the lecture?" Viewers want the cost-benefit before committing weeks.

**Competitive signal:** Research notes explicitly describe llm.c as bypassing "the heavy overhead of PyTorch or Python" with cuBLAS/cuDNN setting an "expert upper bound." The nuance (educational kernels in `dev/`, production kernels in mainline) is rarely surfaced.

**Hook direction:** "Karpathy is rewriting LLMs in raw C. Half the internet thinks you should too. After 30 hours inside llm.c, here's who actually benefits — and who's wasting their weekend."

**Format recommendation:** Long-form 8-15min. Opinion + walkthrough requires room.
