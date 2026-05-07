# /marketing-brain

Loads Kallaway's extracted marketing knowledge and answers questions about hooks, storytelling, content strategy, personal brand, titles, thumbnails, and retention.

## Trigger
User types `/marketing-brain` or asks about Kallaway's frameworks, hook formulas, storytelling systems, or content strategy.

## What This Skill Does
Reads `Content-Hub-Vault/01-Knowledge/marketing_brain.md` and uses it to:
- Answer questions about specific hook formulas or storytelling frameworks
- Generate hooks for a given topic using the 6-Power-Word Stack or other formulas
- Audit a title or thumbnail concept against Kallaway's principles
- Explain a specific framework (Dopamine Ladder, Creator Moat, etc.)

## Usage Examples
- `/marketing-brain` → overview of all available frameworks
- `/marketing-brain hooks` → list all hook formulas with examples
- `/marketing-brain write a hook for [topic]` → generate a hook using the formulas
- `/marketing-brain audit this title: [title]` → score a title against Kallaway's principles
- `/marketing-brain dopamine ladder` → explain the framework in detail

## Execution
1. Read `Content-Hub-Vault/01-Knowledge/marketing_brain.md`
2. Identify which section(s) are relevant to the user's request
3. Answer directly from the extracted knowledge — do not hallucinate frameworks not in the file
4. If generating content (hooks, titles), apply the formulas explicitly and show your work

## Source
Extracted from Kallaway's top 10 videos (921K–105K views) via NotebookLM.
NotebookLM notebook: `Kallaway Marketing Brain` (66ee5515-aa64-49ec-881e-ac28218eb5f9)
Knowledge file: `Content-Hub-Vault/01-Knowledge/marketing_brain.md`
