---
title: "UNDETECTABLE SCRAPER"
date: 2026-06-01
youtube_url: "[VIDEO_LINK]"
tags: [ai-tools, build-in-public]
---

# Build an Undetectable Scraper: CloakBrowser + Python Full Stack

Your scraper works perfectly in testing. Then it hits production and gets blocked in 30 seconds.

## The Real Reason Your Scraper Gets Blocked

The block isn't your code. It's your browser fingerprint.

Modern anti-bot systems — Cloudflare, DataDome, PerimeterX — don't check your IP first. They check your TLS handshake, your canvas hash, your WebGL renderer string, your hardware concurrency count. All of this runs before your first request lands. One mismatch and you're flagged before any page logic fires.

If you're running price monitoring, lead enrichment, or research automation at scale, you hit this wall constantly. You're not fighting a firewall. You're fighting a classification model trained on hundreds of millions of real browser sessions.

## Why the Standard Fixes Don't Work

Rotating proxies are the default first move — different IP per request, clean slate every time. Here's what actually happens: fifty different IPs, all carrying an identical headless Chrome fingerprint. Same user-agent string. Same missing WebGL entropy. Same zero canvas noise. Anti-bot systems don't need your IP when the browser shape is a known signature.

Headless Playwright and Puppeteer have documented fingerprints. Detection vendors keep exact attribute pattern lists. The `playwright-extra` stealth plugin patches the most obvious leaks — but the underlying environment that generated those leaks is unchanged.

The obvious next answer is: use a real browser. But a real Chromium binary on a cloud VM still fails. The fingerprint includes GPU renderer strings, system font inventory, screen DPI, and hardware concurrency — all of which resolve wrong on a headless server. The problem isn't the browser type. It's the environment it's running in.

## How CloakBrowser Fixes This at the Kernel Level

[CloakBrowser](https://github.com/CloakHQ/CloakBrowser) takes a different approach. It's a Chromium fork with source-level fingerprint patches — not flags stripped at runtime, but the browser itself rebuilt to synthesize fingerprint attributes from scratch.

Each browser profile gets a consistent, internally coherent set of values: canvas hash, WebGL vendor string, timezone, system fonts, screen geometry, hardware concurrency — all matched to a specific real device profile. The result is a browser that presents as a distinct physical machine. It passed 30/30 bot detection tests on sites like bot.sannysoft.com.

The beauty of this approach is that the fingerprint is generated, not masked. You're not in a constant cat-and-mouse with plugin updates.

## The Python Integration

CloakBrowser exposes a Chrome DevTools Protocol endpoint on localhost — typically port 9222. That port is your Python entry point and no special SDK is required.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.new_page()
    page.goto("https://target-site.com")
```

Enable remote debugging in the profile settings, grab the port, and connect Playwright directly to the running CloakBrowser instance. Your existing Playwright code works without changes — it's a drop-in replacement at the connection layer, not the automation layer.

The fingerprint profile stays consistent across the session. Canvas hash doesn't change mid-scrape. WebGL vendor string doesn't rotate. The browser behaves like a specific person on a specific machine — which is exactly what detection systems are checking for.

## What This Actually Changes for Your Stack

If you're building any data pipeline that touches scraping at scale, fingerprint consistency is the layer you're probably missing. IP rotation is table stakes. Fingerprint coherence is what actually passes the classification model.

The reason for that is simple: create isolated profiles per use case, enable CDP, connect Python through standard Playwright. Your existing automation logic stays intact. The browser layer handles the detection surface.

---

Watch the full setup walkthrough — profile creation, CDP connection, and a live scrape against a Cloudflare-protected target — in the video: [VIDEO_LINK]
