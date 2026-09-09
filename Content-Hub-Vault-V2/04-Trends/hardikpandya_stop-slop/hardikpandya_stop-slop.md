# hardikpandya/stop-slop

> A skill file for removing AI tells from prose

**Language:** — · **Stars:** 7,715 · **Velocity:** 506.1/day · [GitHub](https://github.com/hardikpandya/stop-slop)

*Captured 2026-06-01*

---

## What problem does it solve?

AI-generated text is increasingly detectable by its overuse of certain phrases, sentence structures, and filler patterns — 'delve into', 'it's worth noting', 'tapestry of', etc. This makes AI-assisted writing feel hollow and erodes trust with readers. Creators who use AI in their workflow need a way to strip these tells before publishing.

## How it works

It is a skill file — a structured prompt or instruction set designed to be invoked as a command in an AI coding or writing assistant. When run against a piece of prose, it applies a set of trained rules to identify and rewrite AI-characteristic phrasing, replacing it with more natural, human-sounding language. Because it is a skill file rather than compiled code, it is portable and model-agnostic.

## Best use cases

- Cleaning up AI-drafted blog posts or newsletters before publishing so they pass both human and automated AI-detection scrutiny
- Post-processing script output or documentation written with AI assistance to match a human author's voice
- Running as a final step in a content pipeline (e.g., after /cascade or /voice-cleanup) to catch residual AI tells before a video script or article goes live

## Getting started

Clone the repo, drop the skill file into your AI assistant's skills directory (e.g., .claude/skills/ for Claude Code), then invoke it against any draft prose you want to clean up.