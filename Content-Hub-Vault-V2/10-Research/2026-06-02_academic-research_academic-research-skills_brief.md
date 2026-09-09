---
date: 2026-06-02
niche: academic research
repos_researched: 1
primary_sources_found: 7
notebook_ids: [notebook:2tw8sb5zuau234afgw3o]
---

# Research Brief — academic research
*2026-06-02 — 1 repos, each in its own notebook*

## Imbad0202-academic-research-skills
Source: https://github.com/Imbad0202/academic-research-skills  
notebook_id: notebook:2tw8sb5zuau234afgw3o  

Here is the synthesized research brief:

---

## Research Brief: `Imbad0202/academic-research-skills`

**Date:** 2026-06-02
**Source:** GitHub (25.8k stars, 2.1k forks, v3.10.0)

---

### What It Is

A Claude Code skill suite that turns academic research into a structured, multi-agent pipeline — from literature review through peer-reviewed revision. Core ethos: "AI is your copilot, not the pilot." Everything terminates at mandatory human checkpoints.

---

### Four Skills, One Pipeline

| Skill | Agents | Core Job |
|---|---|---|
| `/deep-research` | 13 | Literature discovery, PRISMA systematic review, cross-model fact-check |
| `/academic-paper` | 12 | Writing + LaTeX hardening + revision coaching |
| `/academic-paper-reviewer` | 7 | Peer review with dynamic 0-100 scoring + devil's advocate |
| `/academic-pipeline` | 10-stage orchestrator | Runs all three with integrity gates + session resumption |

---

### What Makes It Technically Interesting

**Anti-hallucination stack** — The repo's most defensible engineering. Three-index citation triangulation (Semantic Scholar + OpenAlex + Crossref), claim-faithfulness auditing, and a 7-mode failure checklist drawn from Lu et al. (2026). Optional `ARS_CLAIM_AUDIT=1` flag for full claim tracing.

**Material Passport** — JSON Schema state file enables resumption of long-running research sessions across days/sessions. This is the same pattern Content Hub V2 uses for pipeline-loop state persistence.

**Integrity gates at Stages 2.5 and 4.5** — Hard stops that block full automation. Reviewer agents include an explicit concession threshold to prevent sycophantic capitulation under author pushback.

---

### Content Gap / Opportunity

This project targets *academic researchers* with a formal writing output (LaTeX, DOCX, APA/IEEE citations). Content Hub V2's pipeline targets *video creators* — structurally similar multi-stage pipeline but the deliverable is a script, not a paper.

**Angle with genuine gap:**
> "I tested an AI research pipeline designed for academics on a YouTube research workflow — here's what broke and what actually transferred."

The citation-verification layer (three-index triangulation) has a direct analogue problem for video creators: sourcing claims that can't be fact-checked on camera. That's an underserved problem no creator-focused tool addresses seriously.

---

### Fit Assessment for Content Hub V2

- **`/researcher` skill**: The PRISMA systematic review pattern is worth examining for structured gap analysis — current `/researcher` does GitHub trending scraping, not structured literature review.
- **Material Passport pattern**: Already implemented in V2's pipeline-loop state file. No new work needed.
- **Cross-model verification**: V2 swapped Gemini out (see memory: Gemini→Claude cascade swap 2026-05-19). The cross-model verification design is architecturally interesting but irrelevant until Gemini reliability improves.

---

### Bottom Line

High-signal repo. The anti-hallucination and integrity-gate architecture is production-grade thinking applied to AI-assisted knowledge work. The strongest content angle is the *translation gap* — what academic-grade rigor looks like when you try to apply it to creator workflows, and where it falls apart.

## Raw Findings

<details><summary>Expand for full Q&A and angle battery</summary>

### Research Questions

**Core Functionality**

Based on the provided context, the tool (Academic Research Skills for Claude Code) is designed to facilitate a pipeline that follows the sequence: **research $\rightarrow$ write $\rightarrow$ review $\rightarrow$ revise $\rightarrow$ finalize** [source:lmiamo44ty9f2g4zlnl3].

While the provided context is a high-level repository description and does not list a granular feature-by-feature breakdown, the pipeline implies the following distribution of labor:

### Automated/Assisted Tasks
The tool is designed to assist in the mechanical and iterative stages of the process:
*   **Writing & Drafting:** Moving from the research phase into the "write" phase.
*   **Review & Revision:** Facilitating the "review" and "revise" cycles to refine the quality of the work.
*   **Finalization:** Helping move the document toward its final form.

### Researcher's Responsibility
The researcher remains responsible for the core intellectual contributions and decision-making:
*   **Research Initiation:** The initial "research" phase where the primary data is gathered and the core thesis is formed.
*   **Critical Oversight:** The researcher must guide the "review" and "revise" stages to ensure academic rigor and accuracy.
*   **Final Approval:** The "finalize" step implies a final sign-off by the researcher before publication.

In essence, the tool acts as an accelerant for the **execution and refinement** of the paper, while the **conceptualization, verification, and final ownership** remain the researcher's responsibility [source:lmiamo44ty9f2g4zlnl3].

**Installation and Setup**

I cannot provide the specific CLI installation commands or the prerequisite configurations for the symlink flow because the provided context does not contain technical documentation, installation guides, or setup instructions.

The current context only provides the high-level description of the research-to-publication pipeline (research $\rightarrow$ write $\rightarrow$ review $\rightarrow$ revise $\rightarrow$ finalize) [source:lmiamo44ty9f2g4zlnl3].

To get these specific technical details, I recommend checking the `README.md` or the `installation` section of the GitHub repository mentioned in the sources [source:lmiamo44ty9f2g4zlnl3].

**Preventing AI Hallucinations**

I cannot provide the specific details of how the "7-mode blocking checklist" prevents citation hallucinations and methodology fabrication because the provided context does not contain information regarding a checklist, "integrity gates," or specific mechanisms for preventing hallucinations.

The current available information is limited to the general pipeline sequence: **research $\rightarrow$ write $\rightarrow$ review $\rightarrow$ revise $\rightarrow$ finalize** [source:lmiamo44ty9f2g4zlnl3].

If this checklist is part of the documentation within the repository, please provide the relevant documents or sections so I can analyze the specific logic and safeguards used in those integrity gates.

**Workflow Integration**

I cannot provide instructions on how to integrate the "Style Calibration" feature because the provided context does not contain any information about a style calibration tool, voice mimicking capabilities, or methods for integrating previous publications into the system.

The current context is limited to the overall workflow pipeline: **research $\rightarrow$ write $\rightarrow$ review $\rightarrow$ revise $\rightarrow$ finalize** [source:lmiamo44ty9f2g4zlnl3].

If this feature is documented in a specific guide or a configuration file within the repository, please provide that content so I can explain the integration process for you.

**Performance and Validation**

[failed: Server error '500 Internal Server Error' for url 'http://localhost:5055/api/chat/execute'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500]

**Comparative Analysis**

[failed: Server error '500 Internal Server Error' for url 'http://localhost:5055/api/chat/execute'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500]

### Angle Battery

</details>

