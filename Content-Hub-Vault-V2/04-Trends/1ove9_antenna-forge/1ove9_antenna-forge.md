# 1ove9/antenna-forge

> AI-driven inverse antenna design with real NEC2 + openEMS in the loop. Try the live in-browser playground.

**Language:** Python · **Stars:** 64 · **Velocity:** 10.7/day · [GitHub](https://github.com/1ove9/antenna-forge)

*Captured 2026-05-31*

---

## What problem does it solve?

Designing antennas traditionally requires deep RF engineering expertise and slow manual iteration — you tweak geometry, run simulations, interpret results, and repeat. antenna-forge inverts this: you specify the performance you want and let AI search the design space. It closes the loop with real electromagnetic simulators (NEC2 and openEMS) rather than surrogate models, so the results are physically grounded.

## How it works

The system frames antenna design as an optimization problem where the AI proposes geometry parameters and NEC2/openEMS evaluate them with full-wave EM simulation. This inverse design loop runs iteratively — the AI learns from simulation feedback to converge on geometries that meet the target spec. A live in-browser playground wraps the pipeline so users can experiment without a local install.

## Best use cases

- RF engineers who need to rapidly prototype antenna geometries for a target frequency band and radiation pattern without manual trial-and-error in simulation software
- Researchers exploring novel antenna topologies — the AI can search unconventional geometry spaces that human intuition would never try
- Makers and hobbyists building custom antennas for SDR, LoRa, or drone applications who lack formal antenna design background

## Getting started

Clone the repo, install Python dependencies, and ensure NEC2 or openEMS is available on your PATH — then either run the local pipeline with a target spec or hit the live in-browser playground linked in the repo to explore without any setup.