# anthropics/knowledge-work-plugins

> Open source repository of plugins primarily intended for knowledge workers to use in Claude Cowork

**Language:** Python · **Stars:** 18,418 · **Velocity:** 791.1/day · [GitHub](https://github.com/anthropics/knowledge-work-plugins)

*Captured 2026-06-01*

---

## What problem does it solve?

Knowledge workers using Claude Cowork lack a standardized way to extend the platform with domain-specific workflows and integrations. Every team builds their own one-off automations, leading to duplicated effort and inconsistent quality. This repo provides a curated, open-source plugin ecosystem so teams can share and reuse high-quality extensions instead of reinventing them.

## How it works

The repository is a Python-based collection of plugins that hook into Claude Cowork's extension points. Each plugin is a discrete, installable unit that adds new capabilities — likely following a shared interface or manifest convention so Cowork can discover and load them. Being open source means the community can contribute, audit, and fork plugins to fit their specific needs.

## Best use cases

- A legal team installs a contract-review plugin that surfaces clause summaries and risk flags directly inside their Cowork workspace
- A software engineering org adds a code-review plugin that routes PRs through Claude with project-specific standards baked in
- A content team uses a research-synthesis plugin to pull structured briefs from long documents without leaving their existing workflow

## Getting started

Clone the repo from github.com/anthropics/knowledge-work-plugins, browse the available plugins, and follow the individual plugin's README to install it into your Claude Cowork instance — likely a pip install plus a config entry pointing Cowork to the plugin.