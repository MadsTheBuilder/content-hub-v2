# ruvnet/RuView

> π RuView turns commodity WiFi signals into real-time spatial intelligence, vital sign monitoring, and presence detection — all without a single pixel of video.

**Language:** Rust · **Stars:** 69,469 · **Velocity:** 616.4/day · [GitHub](https://github.com/ruvnet/RuView)

*Captured 2026-06-01*

---

## What problem does it solve?

Traditional presence detection and vital sign monitoring requires cameras or dedicated sensors, raising privacy concerns and hardware costs. RuView solves this by repurposing ordinary WiFi signals already present in most spaces to detect people, monitor breathing/heart rate, and map spatial occupancy — no cameras, no specialized hardware. This makes non-invasive monitoring accessible without the surveillance footprint of video.

## How it works

RuView analyzes Channel State Information (CSI) from standard WiFi adapters — subtle perturbations in the radio signal caused by movement, breathing, and physical presence in a space. It processes these signal variations in real-time using signal processing algorithms implemented in Rust to extract spatial and physiological data. The result is presence detection, room-level mapping, and vital sign estimation from hardware most buildings already have.

## Best use cases

- Eldercare monitoring — detect falls or irregular breathing in a room without installing cameras in private spaces
- Smart building occupancy tracking — know which rooms are occupied for HVAC and lighting automation without video infrastructure
- Security and intrusion detection — identify presence in a space using existing WiFi access points as passive sensors

## Getting started

Clone the repo, ensure you have a WiFi adapter that exposes CSI data (common on certain Atheros/Intel chipsets), and follow the Rust build instructions via `cargo build`. The README likely covers supported adapter models and platform requirements since CSI access is OS and driver dependent.