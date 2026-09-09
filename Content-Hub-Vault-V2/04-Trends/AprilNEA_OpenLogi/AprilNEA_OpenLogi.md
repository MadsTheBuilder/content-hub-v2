# AprilNEA/OpenLogi

> ⚡️A native, local-first alternative to Logitech Options+, written in Rust 🦀 — remap buttons, DPI, and SmartShift over HID++. No account, no telemetry.

**Language:** Rust · **Stars:** 20,228 · **Velocity:** 396.5/day · [GitHub](https://github.com/AprilNEA/OpenLogi)

*Captured 2026-09-09*

---

## What problem does it solve?

Logitech Options+ requires an account, phones home telemetry, and only runs on Windows/macOS, which is a dealbreaker for privacy-conscious users and Linux users who own Logitech mice/keyboards with HID++ features like DPI switching and SmartShift. OpenLogi gives that hardware full local functionality without any cloud dependency or data collection.

## How it works

It's written in Rust and communicates directly with Logitech peripherals over the HID++ protocol, the same proprietary protocol Logitech's own software uses to read device capabilities and push configuration changes. It exposes remapping for buttons, DPI levels, and SmartShift wheel behavior as native local settings with no background service phoning home.

## Best use cases

- Linux users running Logitech mice/keyboards who currently have no official first-party configuration tool
- Privacy-focused users who want to remap buttons and DPI without creating a Logitech account or sending telemetry
- Power users scripting or version-controlling their device configs since it's a native, local-first tool rather than a GUI-locked SaaS app
- Anyone replacing bloated Options+ background processes with a lightweight native Rust alternative

## Getting started

Clone the repo and build it with `cargo build --release` (standard Rust toolchain), then run the binary to detect connected Logitech HID++ devices and configure buttons/DPI/SmartShift locally.