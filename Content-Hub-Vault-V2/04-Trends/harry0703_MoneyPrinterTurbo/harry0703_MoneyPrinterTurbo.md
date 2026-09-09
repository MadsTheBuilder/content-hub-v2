# harry0703/MoneyPrinterTurbo

> 利用AI大模型，一键生成高清短视频 Generate short videos with one click using AI LLM.

**Language:** Python · **Stars:** 73,977 · **Velocity:** 1992.6/day · [GitHub](https://github.com/harry0703/MoneyPrinterTurbo)

*Captured 2026-06-01*

---

## What problem does it solve?

Creating short-form video content at scale requires significant time, money, and technical skill — scripting, voiceover, video editing, and captioning are all separate bottlenecks. MoneyPrinterTurbo eliminates this multi-step manual process by automating the entire pipeline from text prompt to finished short video using AI.

## How it works

The system uses LLMs to generate scripts from a topic, then chains together text-to-speech for voiceover, automated stock footage selection, subtitle generation, and video composition into a single pipeline. It exposes this via a web UI and API, supporting multiple AI providers for each stage so users can swap in different models.

## Best use cases

- Faceless YouTube/TikTok channel automation — generate daily niche content (finance tips, news summaries) without manual editing
- Marketers rapidly prototyping video ads from product descriptions without a video production team
- Developers building content generation SaaS products using MoneyPrinterTurbo as the video rendering backend

## Getting started

Clone the repo, install Python dependencies via pip, configure your API keys for the LLM and TTS providers in the config file, then launch the web UI with `python main.py` and submit a topic to generate your first video.