# Helvesec/rmux

> Universal Rust multiplexer with a typed SDK — drive any CLI or TUI app from code. Native on Linux, macOS, and Windows.

**Language:** Rust · **Stars:** 1,355 · **Velocity:** 90.3/day · [GitHub](https://github.com/Helvesec/rmux)

*Captured 2026-05-31*

---

## What problem does it solve?

Automating CLI and TUI applications programmatically is notoriously brittle — most tools rely on fragile shell scripts or expect/pexpect hacks that break across platforms. rmux solves this by providing a typed SDK that lets you drive any terminal application from code as if it were a first-class API. This is especially painful on Windows where POSIX-based automation tools simply don't work.

## How it works

rmux acts as a multiplexer layer that sits between your code and a terminal application, capturing and injecting input/output through a typed interface rather than raw strings. The Rust-based SDK gives you structured, type-safe handles to send keystrokes, read output, and react to terminal state changes. Because it's native Rust, it compiles to platform-specific binaries that work uniformly on Linux, macOS, and Windows without a compatibility shim.

## Best use cases

- Automating TUI-based tools like database clients, file managers, or `lazygit` in CI/CD pipelines without needing a real terminal
- Building integration tests for CLI applications that require interactive input, such as setup wizards or REPL-based tools
- Scripting complex multi-step workflows across terminal apps — for example, orchestrating a sequence of commands across `ssh`, `vim`, and a custom TUI dashboard from a single Rust program

## Getting started

Add rmux as a dependency in your `Cargo.toml`, then use the typed SDK to spawn a CLI or TUI process and interact with it programmatically via the provided handle API. Since it's cross-platform native, no additional runtime or compatibility layer is needed on Linux, macOS, or Windows.