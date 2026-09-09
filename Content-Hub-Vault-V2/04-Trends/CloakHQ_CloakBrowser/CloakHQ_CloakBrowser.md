# CloakHQ/CloakBrowser

> Stealth Chromium that passes every bot detection test. Drop-in Playwright replacement with source-level fingerprint patches. 30/30 tests passed.

**Language:** Python · **Stars:** 22,845 · **Velocity:** 705.3/day · [GitHub](https://github.com/CloakHQ/CloakBrowser)

*Captured 2026-06-01*

---

## What problem does it solve?

Modern websites use sophisticated bot detection to block automated browsers, making web scraping and browser automation unreliable. Standard tools like Playwright leave detectable fingerprints — browser signatures, canvas hashes, WebGL data — that anti-bot systems like Cloudflare and DataDome flag immediately. Developers either pay for expensive proxy services or constantly chase cat-and-mouse patches that break with every browser update.

## How it works

CloakBrowser ships a patched build of Chromium itself, fixing fingerprint leaks at the source rather than injecting JavaScript overrides that can themselves be detected. Because it's a drop-in Playwright replacement, existing automation scripts work without rewriting — you just swap the browser target. Passing 30 out of 30 bot-detection tests means it covers the full surface area that detection services actually check.

## Best use cases

- Web scraping and data collection from sites that aggressively block headless browsers
- QA and end-to-end testing in environments that gate content behind bot detection
- Competitive intelligence and price monitoring workflows that must run reliably at scale

## Getting started

Since it's a drop-in Playwright replacement written in Python, a developer would install it via pip and point their existing Playwright scripts at CloakBrowser's patched Chromium binary instead of the default browser. No API changes are required — the swap is largely transparent to existing automation code.