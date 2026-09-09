# blader/humanizer

> Agent skill that removes signs of AI-generated writing from text

**Language:** Python · **Stars:** 45,618 · **Velocity:** 827.1/day · [GitHub](https://github.com/blader/humanizer)

*Captured 2026-09-09*

---

## What problem does it solve?

AI-generated text often carries detectable tells (repetitive phrasing, overuse of em dashes, hedging language, generic transitions) that readers and detection tools can spot, undermining trust and authenticity in written content. This skill addresses that gap by systematically rewriting text to remove those AI fingerprints.

## How it works

It's implemented as a Python-based agent skill that scans input text for known patterns of AI-generated writing (drawing on documented style markers like Wikipedia's 'Signs of AI writing' guide) and rewrites flagged passages to sound more natural. The skill likely runs as a callable module within an agent pipeline, taking text in and returning a humanized version out.

## Best use cases

- Content creators polishing AI-drafted blog posts or scripts before publishing
- Students or professionals editing AI-assisted writing to sound more personal and natural
- Marketing teams cleaning up AI-generated copy to avoid a robotic tone
- Developers building content pipelines that need a final 'humanization' pass before output

## Getting started

A developer would clone the repo and integrate it as a skill/module in their Python-based agent or content pipeline, feeding it AI-generated text and calling its humanize function to get cleaned-up output.