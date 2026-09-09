---
date: 2026-05-31
niche: Design
repos_researched: 1
primary_sources_found: 4
notebook_ids:
  - c0b15c4b-8f06-4996-ba31-3519224f6b9f
---

# Research Brief — Design
*2026-05-31 — 1 repos, each in its own notebook*

## Manavarya09-design-extract
Source: https://github.com/Manavarya09/design-extract  
notebook_id: c0b15c4b-8f06-4996-ba31-3519224f6b9f  

[Synthesis failed]

## Sources

- **A Tool for Efficiently Reverse Engineering Accurate UML Class ...**
- **Design Extractor | Extract Any Website's Design for AI Agents ...**
- **DesignAssets - Extract Any Website's Design - Chrome Web Store**
- **Engineering Synthesis of Design Extraction: Methodology, Mechanics, and Mathematical Paradigms across Technical Disciplines**
- **Extract Images from Any Website - TestingBot**
- **GitHub - Manavarya09/design-extract: Extract any website's complete design system with one command. DTCG tokens, semantic+primitive+composite, MCP server for Claude Code/Cursor/Windsurf, multi-platform emitters (iOS SwiftUI, Android Compose, Flutter, WordPress), Tailwind v4, Figma variables, shadcn/ui, CSS health audit, WCAG remediation, Chrome extension. MIT, Playwright, Node 20+. · GitHub**
- **GitUML**
- **How to Extract Colors, Typography & Assets from Any Website ...**
- **Reverse Engineering - Software Engineering - GeeksforGeeks**
- **UML/Code Generation Software | Visual Paradigm**
- **Website Asset Extractor — Bulk Download Images, Videos & SVGs | MiroMiro**
- **https://raw.githubusercontent.com/Manavarya09/design-extract/main/CONTRIBUTING.md**
- **https://raw.githubusercontent.com/Manavarya09/design-extract/main/README.md**
- **https://raw.githubusercontent.com/Manavarya09/design-extract/main/docs/LAUNCH.md**
- **https://raw.githubusercontent.com/Manavarya09/design-extract/main/docs/MCP-REGISTRY.md**


## Raw Findings

<details><summary>Expand for full Q&A and angle battery</summary>

### Research Questions

**How can I extract design systems from live websites?**

### Briefing Document: Extracting Design Systems from Live Websites

#### **Executive Summary**
Design extraction is a "fundamental inverse engineering problem" focused on the systematic reconstruction of abstract, high-level blueprints from live web implementations [1]. Modern front-end engineering has moved beyond manual inspection toward automated tools—including web crawlers, browser-runtime inspectors, and AI-driven engines—that map aesthetic properties into structured design tokens such as colors, typography, and layout patterns [2].

---

#### **1. Technical Methodologies**
The extraction process typically operates through three primary technical channels:

*   **Runtime CSS Inspection:** Tools interact directly with the Document Object Model (DOM) and computed CSS values of a live site [3]. This allows the extraction of actual rendered styles, bypassing obfuscated or minified code [3].
*   **Browser Automation (Headless Crawling):** Advanced CLI tools like **designlang** utilize headless Chromium (via Playwright) to "read the design system off the live DOM" [4, 5]. This process involves:
    1.  **Crawling:** Waiting for network idle and font loading [5].
    2.  **Extraction:** Walking up to 5,000 DOM elements to collect 25+ computed properties [5, 6].
    3.  **Processing:** Using specialized modules to parse, deduplicate, and cluster raw data [5, 6].
*   **Computer Vision:** When source code is inaccessible, AI-driven extractors use localized focus algorithms to isolate UI layers or logos from flat raster images, resolving them into vector paths (SVGs) [7].

---

#### **2. Comprehensive Extraction Ecosystems**
The most advanced tool in the sources, **Manavarya09/design-extract (designlang)**, provides an end-to-end ecosystem that goes beyond basic "paint" extraction to read architectural intent [4, 8].

**Headline Outputs from Extraction:**
| File Type | Purpose |
| :--- | :--- |
| **DTCG Tokens** | W3C-compliant JSON (primitive, semantic, and composite layers) [9, 10]. |
| **Framework Configs** | Drop-in Tailwind CSS configs and shadcn/ui globals [9, 10]. |
| **Component Anatomy** | Typed React stubs (.tsx) for detected components and variants [9, 10]. |
| **Motion Tokens** | Captures durations, easings, and spring detection [9, 10]. |
| **Brand Voice** | Analyzes tone, pronoun posture, and CTA verb inventory [8, 11]. |

**Quotes on Innovation:**
> "Other tools give you the paint. designlang reads the architecture: Layout system... Responsive... Interaction states... Motion language." [8, 12]

---

#### **3. Specialized Extraction Tools**
Several other tools offer targeted extraction capabilities:

*   **Design Extractor:** Specifically built for AI coding agents, it produces a `DESIGN.md` file containing YAML front matter for machine-readable tokens and a markdown body for design rationale [13].
*   **DesignAssets (Chrome Extension):** A consumer-friendly tool that extracts color palettes (HEX, RGB, HSL), typography (font-family stacks), and bulk-downloads images and SVGs [14].
*   **MiroMiro:** Combines asset extraction with a live CSS inspector, allowing users to edit values in real-time and export them as production-ready code [15].
*   **TestingBot Image Extractor:** Uses browser automation to find images that are "dynamically loaded, set as CSS background images, or embedded as SVG elements" [16].

---

#### **4. Advanced Analytics and Compliance**
Modern extraction is no longer limited to visual values; it now includes health audits and accessibility checks:

*   **WCAG Remediation:** Tools like designlang score every foreground/background pair for contrast and suggest the "nearest palette color passing AA / AAA for every failing pair" [17, 18].
*   **Layout and Drift Detection:** Advanced systems can perform "drift checks against a live source-of-truth" and "visual-diffs" to identify design regressions during CI/CD pipelines [4, 19].
*   **Design Scoring:** Automated systems can provide a "Design Report Card" (letter grades A-F) based on dimensions like consistency, accessibility, and complexity [9, 17, 20].

---

#### **5. AI and Agent Integration**
A major trend in design extraction is the creation of "machine-readable design systems" for AI coding assistants [13].
*   **MCP Servers:** By running an MCP (Model Context Protocol) server, extracted design data—including tokens, regions, and components—is exposed directly to AI agents like Claude Code, Cursor, and Windsurf [8, 21].
*   **Prompt Packs:** Extraction outputs often include "paste-ready prompt packs" specifically formatted for tools like v0, Lovable, or Claude Artifacts to recreate UI with pixel-perfect accuracy [4, 9].

---

#### **6. Key Challenges in Extraction**
Developers should be aware of technical hurdles identified in the sources:
*   **Heuristics vs. Reality:** Early extractors often misidentified "brand colors" by simply counting the most-used color (often a gray). Advanced logic now weights interactive elements (CTAs, buttons) and saturation to correctly identify the "Primary" brand color [22, 23].
*   **Authentication:** Extracting from protected pages requires tools that can load cookies or headers (JSON, Playwright storageState, or Netscape formats) to access the UI [17, 24].
*   **Dynamic Content:** Standard scrapers fail on Single Page Applications (SPAs). Extraction tools must use "real browser rendering" to ensure JavaScript-loaded content is captured [25, 26].

**Follow-up: DOM Walk Limits and Extraction Fidelity**

Based on the provided sources, here is what happens when **designlang** encounters large element counts or dynamic content, and the documented figures regarding its accuracy:

### Handling Large Element Counts
The tool is documented to walk **up to 5,000 DOM elements** during its extraction phase [1, 2]. The sources do not explicitly state the behavior for websites that exceed this count, such as whether it truncates the walk or prioritizes specific regions. However, it does allow users to target specific areas using the `--selector <css>` flag, which restricts extraction to elements matching a specific CSS selector (e.g., `".pricing-card"`) [3].

### Lazy-Loaded and Virtualized Content
To address content that is not immediately present in the DOM, such as lazy-loaded or virtualized elements, the tool employs several mechanisms:
*   **Wait for Idle:** The crawl phase utilizes Headless Chromium via Playwright and "waits for network idle and fonts" before starting extraction [1, 2].
*   **Auto-Interaction Pass:** The `--deep-interact` (or `--full`) flag triggers a pass that programmatically scrolls the page, opens menus, modals, and accordions, and hovers over CTAs before extraction begins [4-6].
*   **Dynamic Image Detection:** Its underlying browser automation is designed to discover images that are "dynamically loaded, set as CSS background images, or embedded as SVG elements" [7, 8].

### Accuracy and Coverage Figures
There is no single global "coverage percentage" for the tool, but accuracy is measured through **calibrated design scores** against specific "ground-truth sites" [9, 10]:
*   **Calibration Targets:** The scoring rubric is recalibrated to target scores of **85+ for Stripe**, **80+ for Apple**, and **70+ for Linear** [10].
*   **Remediation and Refinement:** Recent updates (v8) focused on closing "credibility gaps," such as ensuring the extractor correctly identifies real brand colors instead of the most frequently used grays [10, 11].
*   **Accessibility Precision:** The tool's WCAG scoring was improved to filter out decorative glyph spans that previously skewed results; for example, a previous "count-everything" approach incorrectly dropped Linear's accessibility score to 25% [12].

The tool prioritizes reading the "architecture" of a design—including layout patterns, responsive behavior across four breakpoints, and interaction states—rather than just collecting raw "paint" values [13-15].

**Follow-up: DTCG Token Output Completeness**

Based on the project documentation, **designlang** (the CLI for `design-extract`) reconstructs the hierarchy of W3C DTCG-compliant tokens by moving beyond raw data scraping and applying architectural analysis to the live DOM [1, 2]. It categorizes tokens into **primitive, semantic, and composite layers** using a combination of heuristic weighting, clustering, and semantic region classification [3-5].

### Inference of Token Tiers
The tool infers design intent from computed CSS values through several automated processes:

*   **Primitive Tokens:** These represent the raw building blocks (colors, typography, spacing). The tool uses a `page.evaluate()` script to walk up to 5,000 DOM elements, collecting 25+ computed properties which are then deduplicated and classified by 17 extractor modules [6, 7].
*   **Semantic Tokens:** To move from a raw hex code to a "primary" or "action" token, the tool uses a weighted heuristic engine. Rather than simply counting the most frequent color, it weights interactive elements—such as `<button>`, `role="button"`, and CTAs—**100x higher** than static elements [8, 9]. It also weights saturation (2x) and uses a `log(usage)` scale to identify true brand colors versus neutrals or grays [8, 9]. Additionally, it auto-classifies "semantic regions" (e.g., `hero`, `pricing-table`, `cta`) to contextually label tokens [4, 10].
*   **Composite Tokens:** These are inferred through "component anatomy" detection. The tool performs **style-vector clustering** on DOM subtrees to identify reusable components [4, 11]. It programmatically interacts with elements (hovering and focusing) to capture deltas, which allows it to generate **variant × size × state matrices** emitted as typed React stubs (`*.tsx`) [2, 10, 12].

### Reliability and Quantification
The sources do not provide a single percentage for "hierarchy reconstruction accuracy," but they do quantify reliability through **recalibrated design scores** against "ground-truth" sites [13, 14].

*   **Ground-Truth Calibration:** The scoring rubric was specifically recalibrated using industry-leading sites as benchmarks. For instance, Stripe is targeted for a score of **85+**, Linear for **70+**, and Apple for **80+** [9].
*   **Credibility Improvements:** Previous versions of the tool suffered from "credibility gaps," such as misidentifying grays as primary colors or giving top-tier sites like Linear a failing grade (F) due to a11y count errors [8, 14]. Following v8 updates to the heuristic engine (filtering decorative glyphs and weighting interactive elements), these sites now receive scores that align with professional assessments (e.g., Linear moving from an F to a C+/B) [8, 14].
*   **Validation Tools:** The project includes a "design-score badge" and a "shareable graded report card" (A-F) across seven categories to provide a quantifiable evidence-based grade for every extraction [3, 4, 15].

**Follow-up: Design Score Scale and What It Measures**

In the `design-extract` project, design scores are calculated on a **100-point scale** [1]. These scores are used to provide a "7-category quality rating" (A–F) and a shareable "Design Report Card" that evaluates the site across **eight specific dimensions** [2, 3].

### Dimensions of Measurement
While the sources do not explicitly list all eight dimensions by name, they identify the following core metrics and categories that contribute to the final grade:
*   **Accessibility (A11y):** Measured primarily through WCAG 2.1 contrast ratios for all foreground/background color pairs [1, 2, 4].
*   **Color System:** Evaluates the extraction of palettes, including brand, background, and text colors, as well as gradients [2, 5].
*   **Typography:** Analyzes font families, weights, sizes, and the overall type scale [5, 6].
*   **Layout System:** Assesses grid patterns, flex usage, container widths, and gap values [2, 7].
*   **Motion Language:** Examines durations, easings, and interaction transitions [1, 8].
*   **CSS Health:** Audits specificity, the use of `!important`, unused CSS, and keyframes [2].
*   **Interaction States:** Captures deltas for hover, focus, and active states [2, 8].
*   **Component Anatomy:** Evaluates the structural complexity and reuse of detected UI components [8, 9].

### Ground-Truth Calibration and Derivation
A "ground-truth" score is derived by testing the extraction engine against industry-standard design systems known for high quality, such as Stripe, Apple, and Linear [10, 11]. The project recalibrated its scoring rubric in version 8 to ensure these sites received scores reflecting their actual design quality rather than raw technical counts [11, 12].

The difference between a **70 (Linear)** and an **85 (Stripe)** reflects specific technical nuances in how the tool perceives design quality:
*   **Fidelity vs. Raw Data:** Prior to v8, a "count-everything" path penalized sites like Linear (dropping it to 25% WCAG) because it incorrectly included decorative elements in accessibility audits [11, 13]. The current 70+ target for Linear reflects a shift toward **semantic fidelity**, where the tool filters for meaningful text and interactive elements [13].
*   **Weighting and Heuristics:** The score reflects the tool's ability to correctly identify design intent. For example, v8 introduced a heuristic that weights interactive backgrounds (like CTA buttons) 100 times more than other elements to accurately identify "Primary" brand colors [12, 13].
*   **Actionable Issues:** A lower score (like the 68/100 "D" grade in the Vercel example) is often the result of "actionable issues" identified during extraction, such as failing WCAG contrast pairs or excessive CSS specificity [1, 2].

Ultimately, these scores are intended to measure **design quality and compliance** rather than just the volume of data extracted, acting as a "design regression guard" during development [10, 14].

**Follow-up: Quantification of Hierarchy Reconstruction Accuracy**

While the source material for the `design-extract` project (also referred to as `designlang`) does not provide a single percentage for "hierarchy reconstruction accuracy," it outlines several ways reliability is currently quantified and hints at future developments regarding accuracy.

### Current Accuracy Metrics and Calibration
The project currently relies on a **7-category quality rating (A-F)** and a shareable **"Design Report Card"** to quantify design extraction reliability [1-3]. Rather than a single percentage, reliability is demonstrated through:
*   **Ground-Truth Recalibration:** In version 8, the scoring rubric was specifically recalibrated against high-quality "ground-truth" sites such as Stripe, Linear, Apple, and GitHub [4, 5]. For instance, the update ensured that if a site like Linear previously received an "F," it now correctly receives a "C+/B," while Stripe maintains an "A" [5].
*   **Heuristic Improvements:** The project has moved toward more "defensible" scores by refining its internal logic. This includes weighting interactive backgrounds (like CTAs and buttons) 100× more than other elements to correctly identify brand colors and using a `hasText` boolean to filter decorative glyphs from accessibility scoring [6].
*   **Structural Audits:** The tool performs "drift checks" against a live source-of-truth and "linting" of extracted tokens to ensure consistency, which serves as a functional measure of accuracy in a CI/CD pipeline [7-9].

### Future Plans for Accuracy and Metrics
Regarding future research and documentation updates:
*   **Impending Accuracy Upgrade:** The documentation explicitly states that a **"major accuracy upgrade is coming"** along with new capabilities, though it does not specify if this will include a new statistical metric for hierarchy reconstruction [10].
*   **Documented Roadmap:** The project's `CONTRIBUTING.md` lists several "good first issues" and planned features, but these currently focus on expanding technical reach—such as supporting extra cookie formats, proxy support, a DevTools panel, and additional CSS-in-JS emitters—rather than establishing new mathematical accuracy benchmarks [11, 12].
*   **Evolutionary Tracking:** The sources suggest a move toward "multi-version analysis" and "history tracking" to monitor how designs change over time, which may eventually provide more data points for reconstruction consistency [2, 13].

In summary, while there is no specific plan mentioned to provide a "reconstruction percentage," the project is actively moving toward higher "credibility" by refining its scoring rubrics and heuristics against industry-standard benchmarks [4, 5].

**Follow-up: Comparison to Alternative Methods**

[failed: Chat request was rate limited or rejected by the API. Wait a few seconds and try again.]

### Angle Battery

</details>

