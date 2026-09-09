# heygen-com/hyperframes

> Write HTML. Render video. Built for agents.

**Language:** TypeScript · **Stars:** 48,072 · **Velocity:** 555.1/day · [GitHub](https://github.com/heygen-com/hyperframes)

*Captured 2026-09-09*

---

## What problem does it solve?

AI agents that generate video content today are stuck stitching together clips or wrestling with rigid templating tools not built for programmatic use. Hyperframes lets an agent (or developer) express a video declaratively as HTML and get rendered video out, closing the gap between 'write markup' and 'ship a video.'

## How it works

It takes HTML/CSS as the authoring layer for scenes, layouts, and animations, then renders that markup into video frames/output using a TypeScript-based pipeline — essentially treating a browser-like rendering model as the source of truth for each frame instead of a traditional video-editing timeline. This lets structured, code-driven layout (flexbox, CSS animations, text, images) become video without manual editing software.

## Best use cases

- AI agents auto-generating explainer or highlight videos from structured data or text
- Programmatic creation of personalized video ads or social clips at scale
- Turning HTML dashboards/reports into shareable video summaries
- Automated video generation pipelines for content teams (e.g. batch-producing short-form clips)

## Getting started

Clone the repo, install the TypeScript/Node dependencies, and check the README/examples for the HTML markup conventions the renderer expects, then write an HTML file and run the render command to produce a video output.