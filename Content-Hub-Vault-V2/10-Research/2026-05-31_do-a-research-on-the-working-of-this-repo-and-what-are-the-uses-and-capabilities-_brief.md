---
date: 2026-05-31
niche: do a research on the working of this repo and what are the uses and capabilities 
repos_researched: 1
primary_sources_found: 7
notebook_ids: [4977a6d4-2fab-439a-9de9-9fc207176a4e]
---

# Research Brief — do a research on the working of this repo and what are the uses and capabilities 
*2026-05-31 — 1 repos, each in its own notebook*

## UditAkhourii-adhd
Source: https://github.com/UditAkhourii/adhd  
notebook_id: 4977a6d4-2fab-439a-9de9-9fc207176a4e  

[Synthesis failed]

## Sources

- **GitHub - UditAkhourii/adhd: ADHD — a skill for coding agents. Tree-of-thought with pruning, built on the Claude & Codex Agent SDK. Fans out parallel divergent thoughts under different cognitive frames, scores, prunes traps, deepens the survivors. The no-brainer skill for creative and interdisciplinary work. · GitHub**
- **https://raw.githubusercontent.com/UditAkhourii/adhd/main/CONTRIBUTING.md**
- **https://raw.githubusercontent.com/UditAkhourii/adhd/main/README.md**
- **https://raw.githubusercontent.com/UditAkhourii/adhd/main/documentation/api.md**
- **https://raw.githubusercontent.com/UditAkhourii/adhd/main/documentation/evals.md**
- **https://raw.githubusercontent.com/UditAkhourii/adhd/main/documentation/frames.md**
- **https://raw.githubusercontent.com/UditAkhourii/adhd/main/documentation/how-it-works.md**
- **https://raw.githubusercontent.com/UditAkhourii/adhd/main/documentation/install.md**


## Raw Findings

<details><summary>Expand for full Q&A and angle battery</summary>

### Research Questions

**How does ADHD diverge from standard Chain-of-Thought reasoning?**

### Briefing Document: ADHD vs. Standard Chain-of-Thought (CoT)

#### Overview of the ADHD Framework
ADHD is defined as an architectural solution designed to address the issue of "premature convergence" inherent in standard autoregressive reasoning models [1, 2]. While traditional methods follow a linear progression, ADHD "fans out parallel divergent thoughts under different cognitive frames, scores, prunes traps, and deepens the survivors" [3, 4]. It is specifically optimized for creative and interdisciplinary engineering tasks such as API design, strategy, and "fuzzy debugging" [5, 6].

#### Limitations of Linear Chain-of-Thought (CoT) and Tree-of-Thought (ToT)
The project identifies significant structural flaws in existing reasoning patterns:
*   **Anchoring in CoT:** Linear Chain-of-Thought is restricted because it "anchors on whatever it says first" [1, 2].
*   **Shared Context in ToT:** While Tree-of-Thought (ToT) expands the search space, it "still walks a single shared context," which allows anchoring to persist across its various branches [1, 2].
*   **Premature Convergence:** These methods often lead the model to settle on an obvious or initial idea rather than exploring unconventional but viable solutions [1, 2, 7].

#### Core Divergence: The Two-Phase Loop with a "Hard Wall"
ADHD diverges from standard reasoning by enforcing a "two-phase loop with a hard wall between the phases" to prevent the critic from "strangling" the generator [7-9].

**Phase 1: Divergence through Cognitive Frames**
Instead of a single reasoning path, ADHD spawns $N$ parallel and isolated agent calls [7-9].
*   **Cognitive Frames:** Each branch is assigned a "vantage operator," which is a system-prompt payload that forces the model to re-pose the problem from a specific, distorted position, such as a "10-year-old," a "hardware engineer," or a "competitor trying to break it" [7, 10, 11].
*   **Absolute Isolation:** Branches operate with "zero shared context during divergence," meaning the "regulator" branch never sees what the "speedrunner" branch has produced [1, 2, 12]. 
*   **Forbidden Evaluation:** During this phase, the system prompt explicitly "forbids evaluation, ranking, or hedging" to ensure pure, uninhibited generation [7, 12, 13].

**Phase 2: Mechanical Focus and Pruning**
Once divergence is complete, a separate critic pass is initiated [8, 12, 14].
*   **Mechanical Split:** The split between the generator and the critic is "mechanical," meaning they are "separate LLM calls with opposite system prompts" rather than being handled within a single prompt [8, 13, 14].
*   **Scoring and Trap Detection:** Every idea is scored based on "novelty, viability, and fit," and the critic "flags traps with reasons" to prune "seductive-but-broken ideas" that single-shot baselines often miss [8, 14-16].
*   **Clustering by Angle:** Unlike standard keyword clustering, ADHD groups ideas by their "underlying angle," such as "remove-the-server plays" or "cache-shaped plays," to surface the actual shape of the design space [12, 17, 18].

#### Architectural Differences
| Feature | Standard CoT / ToT | ADHD Framework |
| :--- | :--- | :--- |
| **Context** | Shared across steps or branches [1, 2]. | Zero shared context during divergence [1, 2, 12]. |
| **Reasoning Path** | Linear or linked tree [1, 2]. | Isolated parallel "vantage" branches [8, 9, 19]. |
| **Critic Integration** | Often interleaved or in-context [2, 13]. | Mechanical split via separate API calls [8, 13, 14]. |
| **Inference Cost** | Often quadratic as context grows [19]. | Scales linearly ($O(N \times \text{per branch})$) [19]. |

#### Evidence-Based Results of Divergence
Head-to-head evaluations against single-shot baselines demonstrate the effectiveness of this divergent approach [20-22].
*   **Trap Detection:** ADHD shows a 5.2$\times$ improvement in detecting traps, as baselines rarely identify broken but attractive ideas [15, 20, 21].
*   **Novelty and Breadth:** The framework produces 2.9$\times$ more novel ideas and 1.9$\times$ more breadth in its solutions compared to standard models [15, 20, 21].
*   **Success Rate:** ADHD won 5 out of 6 open-ended engineering problems in controlled trials judged by an independent LLM [15, 20, 23, 24].

**Follow-up: ToT 'Shared Context' Claim**

The sources distinguish ADHD from what they categorize as **"in-context Tree-of-Thought" (ToT)** [1]. The specific distinction made is that while standard ToT widens the search, it often "still walks a single shared context," leading to anchoring that persists across branches [2, 3].

### Comparison to "In-Context" Tree-of-Thought
The sources argue that many ToT implementations rely on a "promised in-prompt" split within the same session [1]. In contrast, ADHD treats anchoring as an **architectural problem** rather than a prompting one [2, 3]. Key structural differences mentioned include:
*   **Mechanical Isolation:** ADHD spawns $N$ parallel, isolated agent calls, each being a fresh, stateless session with no shared message history or KV-cache [4, 5].
*   **Hard Walls:** There is a "hard wall" between the Diverge and Focus phases [4, 6]. Branches never see each other during the divergence phase, ensuring no anchoring or convergence pressure from other ideas [1, 6, 7].
*   **System Prompt Split:** The generator-critic split in ADHD is mechanical—using separate LLM calls with opposite system prompts—rather than requesting both generation and evaluation in a single prompt or session [1, 6, 8].

### Benchmarks and Experiments
The sources do not explicitly name a specific external experiment or paper that measures anchoring in ToT branches. Instead, they provide a reproducible eval suite comparing ADHD head-to-head against a **single-shot baseline** [9].

While not a direct comparison to ToT in the provided data, the benchmarks demonstrate the impact of ADHD's architecture on preventing premature convergence:
*   **Trap Detection:** This is the dimension with the largest gap, where ADHD scored 9.50 vs. the baseline's 1.83 (a 5.2× ratio) [10-12]. The sources state that baselines "rarely name the seductive-but-broken ideas," which is attributed to the "mechanical" critic pass routinely flagging these traps [12, 13].
*   **Novelty:** ADHD significantly outperformed the baseline (7.83 vs. 2.67), suggesting the "isolated reasoning processes under deliberately distorted cognitive frames" successfully overcome the anchoring found in linear or shared-context reasoning [3, 10, 11].

The documentation notes that the academic diversity literature typically measures at $K=100$ branches, while ADHD's current evals run at $K=5$, a gap the project aims to bridge [14]. Furthermore, the author acknowledges a CHI 2025 study which found no significant benefit from LLM problem-reframing for human designers, though they maintain ADHD's LLM-to-LLM context is different [15].

**Follow-up: Premature Convergence — Quantified Evidence**

The project provides empirical evidence comparing ADHD against a **single-shot baseline** (standard Chain-of-Thought style) across **six open-ended engineering problems**, demonstrating significantly higher divergence and idea quality [1-3]. While the sources provide structured comparisons against ToT, the numerical benchmarks specifically target a single-shot baseline to highlight the architectural advantage of the ADHD loop [4, 5].

### Empirical Results (ADHD vs. Single-Shot Baseline)
Across 6 problems, ADHD was judged by an independent LLM with a "skeptical-staff-engineer" prompt, using a randomized A/B order to balance positional bias [2, 3]. The results show that ADHD produces more "breadth" and "novelty," which are the primary indicators of reduced convergence:

| Dimension | ADHD Score | Baseline Score | Improvement (Δ) | Ratio |
| :--- | :---: | :---: | :---: | :---: |
| **Breadth** | **9.00** | 4.83 | **+4.17** | 1.9× |
| **Novelty** | **7.83** | 2.67 | **+5.17** | 2.9× |
| **Trap Detection** | **9.50** | 1.83 | **+7.67** | 5.2× |
| **Actionability** | **9.50** | 6.50 | **+3.00** | 1.5× |
| **Builder Usefulness**| **7.67** | 6.83 | **+0.83** | 1.1× |

Source: [1, 2, 6]

### Task Conditions and Benchmarks
The evaluation was conducted under the following conditions:
*   **Problem Type:** "Open-ended engineering problems" where multiple viable solutions exist [1, 3].
*   **Specific Examples:**
    *   Designing a rate limiter that survives a leader election [7, 8].
    *   Determining retry/UX strategies for a CLI that hangs on LLM calls [8].
    *   Naming complex functions or sharding queues under bursty load [9].
    *   One specific problem ID cited is `lru-100ms` [10].
*   **Scale:** Evals typically run at $K=5$ parallel branches [11].
*   **Hardware/Environment:** The results are reproducible locally via `npm run evals`, which generates an `EVALS.md` report [10].

### Addressing Convergence in ToT vs. ADHD
The sources frame **premature convergence** as an architectural failure of shared context [4, 12].
*   **CoT/ToT Failure:** Linear CoT "anchors" on its initial output, while Tree-of-Thought (ToT) is criticized because it "still walks a single shared context," allowing anchoring to persist across its branches [4, 12].
*   **ADHD Solution:** ADHD enforces "zero shared context during divergence" by spawning isolated reasoning processes under different cognitive frames [4, 13]. The generator branches are mechanically forbidden from seeing each other's output, preventing the "convergence pressure" found in in-context ToT [5, 14].

### Limitations and Context
The project notes several limitations regarding these empirical findings:
*   **Baseline Selection:** The primary numerical baseline is "single-shot," not an explicit "ToT" implementation, though the architecture is designed to address ToT's specific convergence flaws [3-5].
*   **Judging Bias:** The judge is from the same model family as the generator, which may introduce familiarity bias [11].
*   **Small Sample Size:** The current data relies on only six engineering-focused problems [11].
*   **Scale Gap:** While ADHD measures diversity at 5 branches, academic literature often uses 100, a gap the project aims to bridge in future roadmaps [11].

**Follow-up: Which ToT implementation is 'in-context ToT'?**

The provided sources do not explicitly name the Yao et al. 2023 paper or any other specific implementation as the target of their "in-context Tree-of-Thought" characterization [1-3]. Instead, the documentation presents this as a general architectural critique of how such reasoning is typically implemented [1, 4].

According to the project's documentation, the author frames the situation as follows:

*   **Definition of "In-Context" ToT:** The sources characterize "in-context Tree-of-Thought" (ToT) as a method that "widens the search but still walks a single shared context," which causes anchoring to persist across various branches [1, 4].
*   **The "Mechanical" Split:** ADHD distinguishes itself by using a "mechanical" generator-critic split [2, 3]. This means it uses "separate LLM calls with opposite system prompts" and "different API calls" rather than a "promised in-prompt split within the same session" [2, 3].
*   **Architectural vs. Prompting:** The project explicitly frames the issue as "an architectural problem, not a prompting one" [1, 4]. The author argues that without a "hard wall" between divergent reasoning processes, premature convergence is inevitable due to the nature of autoregressive reasoning [4, 5].
*   **Missing Deep Dive:** The most specific comparison, including what the author calls "the three load-bearing differences," is located in a document titled `documentation/vs-cot-and-tot.md` [3, 6, 7]. However, the full contents of that specific document are not included in the provided source material.
*   **Academic Context:** While not naming Yao et al., the sources mention that the project is based on a preprint titled *"ADHD: Parallel Divergent Ideation for Coding Agents"* by Udit Akhouri [8, 9]. This suggests the characterization of existing ToT work as "in-context" may be the author's own academic framing developed for that paper.

The documentation also notes that academic diversity literature generally measures diversity at much higher scales ($K=100$) than the default ADHD settings ($K=5$), indicating an awareness of broader academic work in this field [10].

**Follow-up: Anchoring-in-ToT claim is unverified by any cited experiment**

The sources present the claim that anchoring "persists across branches" in Tree-of-Thought (ToT) primarily as a **theoretical architectural argument** based on the first principles of autoregressive reasoning [1, 2]. 

The rationale for this assertion is as follows:

*   **Shared Context Mechanism:** The sources argue that while ToT widens the search space compared to linear Chain-of-Thought (CoT), it fundamentally "still walks a single shared context" [1, 2]. Because the branches share this history, the author asserts that the initial reasoning steps act as an anchor that influences all subsequent branches [1, 2].
*   **Structural Isolation vs. Prompting:** ADHD is framed as an "architectural fix" for this problem [1, 2]. The author explicitly distinguishes ADHD from "in-context Tree-of-Thought" by making the isolation "mechanical"—meaning it uses separate LLM calls with zero shared context during the divergence phase [3].
*   **Preventing Convergence Pressure:** The sources state that in ADHD, branches "do not see each other" (e.g., a "regulator" branch never sees a "speedrunner" branch) specifically to ensure there is "no anchoring, no shared context, no convergence pressure" [3, 4].

While the project references an **independent evidence-based research review** with 11 sources and a **preprint** titled "ADHD: Parallel Divergent Ideation for Coding Agents," the provided excerpts do not contain specific citations or experimental data measuring anchoring in ToT specifically [5-7]. The internal benchmarks only compare ADHD against a "single-shot baseline," not a ToT implementation [8, 9]. Consequently, within the provided material, the ToT comparison remains a **structural argument** used to justify ADHD's "hard wall" between reasoning phases [3, 10, 11].

**Follow-up: ToT Comparison Numbers**

The provided sources do not contain numerical scores for a direct head-to-head comparison between ADHD and Tree-of-Thought (ToT). While the documentation mentions "structured comparisons" against ToT, these are explicitly described as **structural comparisons** regarding architecture rather than quantitative scoring [1-3].

The numerical results reported across the five dimensions (Breadth, Novelty, Trap Detection, Actionability, and Builder Usefulness) compare ADHD exclusively against a **single-shot baseline** using the same model [4-6].

### Reported ADHD vs. Single-Shot Baseline Scores
The scores provided for the "Results" section are as follows:

| Dimension | ADHD | Baseline |
| :--- | :--- | :--- |
| **Breadth** | 9.00 | 4.83 |
| **Novelty** | 7.83 | 2.67 |
| **Trap Detection** | 9.50 | 1.83 |
| **Actionability** | 9.50 | 6.50 |
| **Builder Usefulness** | 7.67 | 6.83 |
[4, 5, 7]

### Comparison Context and Tasks
The architectural distinction provided is that while ToT "widens the search," it still "walks a single shared context," leading to persistent anchoring across branches [8, 9]. ADHD, by contrast, spawns isolated reasoning processes with zero shared context during divergence [3, 9].

The comparisons (against the baseline) were run on **six open-ended engineering problems** [4, 5, 7]. While the full list of tasks is not detailed in the excerpts, the following specific tasks or IDs are mentioned:
*   **lru-100ms:** A specific problem involving an LRU cache with a 100ms constraint [10].
*   **"Design a rate limiter that survives a leader election"** [11-13].
*   **"Name this function"** [13, 14].
*   **"How should we shard this queue under bursty load?"** [14, 15].
*   **"UX/retry strategy for a CLI that hangs for 90s on LLM calls"** [13].

The evaluation used an independent LLM-as-judge with a "skeptical-staff-engineer" prompt to declare winners across these categories [4, 6].

**Follow-up: Statistical Validity of N=6 Evals**

The sources do not report any confidence intervals, variance, or statistical significance metrics for the performance results of the ADHD skill [1-3]. The findings are presented as mean scores across the six evaluated problems [1, 4, 5].

However, the documentation explicitly acknowledges several limitations regarding the statistical rigor and generalizability of these results:

*   **Small Sample Size:** The authors explicitly list the "Small set" of six engineering-shaped problems as a known limitation [3].
*   **Scale Gap:** The documentation notes a "Scale gap," pointing out that while these evals run at $K=5$ branches, academic diversity literature typically measures at $K=100$ [3].
*   **Judging Bias:** It acknowledges "Same-model judging" as a limitation, where the judge belongs to the same model family as the generator, potentially introducing familiarity bias [3].
*   **Human Applicability:** The sources also reference a CHI 2025 study as "honest counter-evidence," which found no significant benefit from LLM problem-reframing for human designers, though it notes that ADHD's LLM-to-LLM context is different [6].

While the sources highlight that ADHD "wins 5 of 6 problems" with significant ratios in dimensions like trap detection ($5.2\times$), these are presented as headline figures from a local, small-scale evaluation suite rather than a statistically generalized proof [3, 4, 7, 8].

**Follow-up: Contents of `documentation/vs-cot-and-tot.md`**

I have initiated a search for the document `documentation/vs-cot-and-tot.md` using a fast research mode on the web. Once the search completes, the results will appear in your sources panel. 

Please review any pending results there to import or delete them so you can access the new information. Once the source is added, I will be able to provide the specific "three load-bearing differences" and architectural distinctions you are looking for.

**Follow-up: Akhouri preprint — does it cite Yao et al. 2023?**

[failed: Chat request failed: ]

**Follow-up: Preprint Empirical Scope on ToT**

Based on the provided excerpts, the evidence-based benchmarks for ADHD are conducted against a **single-shot baseline**, while the comparison to Tree-of-Thought (ToT) remains a **structural and architectural argument** in the prose [1-3].

According to the "Headline results" and the eval suite documentation, the performance of ADHD is measured head-to-head against a "single-shot baseline at the same model" across six open-ended engineering problems [3-5]. The results table specifically tracks dimensions like breadth, novelty, and trap detection for "ADHD" versus "Baseline," with no mention of a ToT baseline in the experimental data [4-6].

The distinction from Tree-of-Thought is framed as a solution to an architectural problem:
*   **Structural Argument:** The sources argue that while ToT widens the search, it still "walks a single shared context," which allows anchoring to persist across branches [1, 2].
*   **Architectural Fix:** ADHD is presented as a fix for this by enforcing a "hard wall" between divergent branches, ensuring they have zero shared context and do not see each other during the ideation phase [7-10].

The "Known limitations" section of the evaluation documentation mentions gaps such as "same-model judging" and a "small set" of problems, but it does not list the absence of a ToT benchmark as a limitation, further suggesting the primary experimental focus is the comparison to single-shot reasoning [11]. Because the full preprint is not provided in its entirety, I cannot confirm if it contains additional unpublished experiments; however, the summaries and "Headline results" in the source materials do not contain a benchmark against ToT [3, 4, 6].

**Follow-up: Missing Sixth Engineering Problem**

The sources identify the sixth task as **lru-100ms**, which is explicitly mentioned as a specific problem ID within the evaluation suite [1, 2]. This task is likely a coding challenge involving the design of an LRU cache with a specific performance constraint (100ms), as it is grouped with "leader election" as an example of a specific constraint that rewards non-obvious thinking [2].

Regarding the per-task dimension scores:

*   **Detailed Breakdown is Missing:** The provided sources do not include the specific score breakdown for the **lru-100ms** task or any of the other five individual tasks. The sources state that "full per-problem verdicts" are located in the `EVALS.md` file, which is mentioned as the output of the evaluation run but is not included in the provided excerpts [1, 3].
*   **Aggregate Performance:** The sources only provide the **mean scores** across all six engineering problems. These results show that ADHD significantly outperforms single-shot baselines in every dimension, with the most dramatic improvement in **trap detection** (a 5.2× ratio over the baseline) [4-6].
*   **A Single Loss:** It is explicitly noted that while ADHD wins on the mean scores, it **wins 5 of the 6 problems** head-to-head [6-8]. The sources do not specify which of the six tasks ADHD failed to win or how the individual dimension scores for that specific task differed from the others.

**Follow-up: LLM-as-Judge Rubric Specificity**

The evaluation framework for ADHD utilizes an LLM-as-judge configured with a **"skeptical-staff-engineer"** system prompt to compare ADHD's output against a single-shot baseline [1]. While the sources provide the names of the five dimensions, the exact textual rubric for each is not explicitly detailed; however, their focus is defined as follows:

### Evaluation Dimensions
*   **Breadth:** Measuring the range of different angles or perspectives explored [1, 2].
*   **Novelty:** Assessing how unique or unconventional the suggested ideas are [1, 2].
*   **Trap Detection:** This is the project's most significant differentiator. It focuses on identifying "seductive-but-broken ideas" and providing "mechanistic reasons" for why they are traps (e.g., noting that a specific library is not thread-safe under certain loads) [2, 3].
*   **Actionability:** Evaluating how feasible it is to implement the suggested steps [1, 2].
*   **Builder Usefulness:** Determining the overall value of the output to a developer [1, 2].

### Consistency and Validation Measures
The framework includes specific mechanical checks to maintain judge consistency and mitigate bias, though it acknowledges certain limitations:

*   **A/B Randomization:** To prevent positional bias, the order of the ADHD and baseline outputs is randomized before being presented to the LLM judge [1].
*   **Same-Model Judging Limitation:** The documentation identifies a known limitation where the judge often belongs to the same model family as the generator, potentially leading to "familiarity bias" [4]. Implementing cross-model judging is currently on the project roadmap [4, 5].
*   **External Review:** The method has undergone an independent "evidence-based research review" involving 11 sources and 8 validation rounds, though this was a review of the underlying method rather than a recurring inter-rater calibration for the daily eval suite [6-8].
*   **Small Sample Size:** The current evaluation is restricted to a small set of six engineering-focused problems, which the maintainers acknowledge as a scale gap compared to academic diversity literature [4].
*   **Human-in-the-loop:** The project notes that human-in-the-loop applicability remains unproven, citing external research that found no significant benefit from LLM problem-reframing for human designers [9].

**Follow-up: K=100 Diversity Benchmark Source**

The provided sources do not specify the names of the papers or studies from the "academic diversity literature" that set the **K=100** benchmark [1]. 

The sources mention this benchmark in the context of a "scale gap" in the project's evaluation methodology [1]. While the project's current evals run at **K=5** branches, it notes that the academic literature on diversity typically measures at K=100 [1]. The sources do not clarify whether this is a consensus standard or the methodology of a specific paper, though they track the effort to bridge this gap in the project's issue tracker as **issue #18** [1].

If you would like me to find the specific academic papers or studies that define the K=100 diversity benchmark, I can use a search tool to look for this information. Would you like me to do that?

**Follow-up: Same-Model Judging Bias Magnitude**

Based on the sources, the same-model judging limitation is listed purely as an **unquantified concern** [1].

While the documentation acknowledges that using a judge from the same model family as the generator introduces "familiarity bias," it does not provide an estimate or a quantified figure for how much this bias might inflate reported ratios, such as the **5.2× trap-detection** advantage [1, 2].

The project addresses this limitation by:
*   **Listing it explicitly:** It is categorized under "Known limitations" to provide transparency for reviewers [1].
*   **Using mitigation techniques:** To reduce other forms of bias, the evaluation methodology employs a "skeptical-staff-engineer" system prompt for the judge and randomizes the A/B order of responses to balance positional bias [3].
*   **Planning future improvements:** Implementing cross-model judging to formally address and potentially quantify this bias is currently on the project's roadmap (tracked as issue #6) [1, 4].

**Follow-up: Same-Model Judging Validity**

The project's documentation acknowledges "same-model judging" as a known limitation, defining it as the judge being from the **same model family** as the generator [1]. While the sources refer to the judge as an "independent LLM," this refers to a separate model call using a "skeptical-staff-engineer prompt" rather than a different architecture [2, 3].

Regarding the quantification of score inflation:

*   **Quantification:** The provided sources **do not quantify** how much this familiarity bias might specifically inflate scores for novelty or trap detection [1]. They acknowledge that this setup can lead to "familiarity bias" but do not provide comparative data against an independent judge from a different model family [1].
*   **Contextual Findings:** The sources do highlight that ADHD shows a massive gap in trap detection (9.50 vs. 1.83 for the baseline), which is the dimension with the largest performance difference [4, 5]. However, they treat the potential inflation of these numbers as an open issue to be addressed in the roadmap through "cross-model judging" [1, 6].
*   **Counter-Evidence:** While not directly quantifying judging inflation, the documentation notes that a controlled human-in-the-loop study (CHI 2025) found no significant benefit from LLM problem-reframing with human designers, which serves as a piece of "honest counter-evidence" regarding the method's real-world impact [6].

### Angle Battery

</details>

