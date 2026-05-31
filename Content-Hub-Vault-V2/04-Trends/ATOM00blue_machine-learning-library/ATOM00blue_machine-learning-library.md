# ATOM00blue/machine-learning-library

> A hand-curated, topic-organized library of the best ML education — 923 docs (391 arXiv papers, 474 Stanford/MIT/Karpathy/fast.ai lectures, 58 explainer articles), normalized to Markdown with full provenance. Open it in Obsidian or point your agent at it. A clean ML corpus for learning, RAG & fine-tuning.

**Language:** Python · **Stars:** 107 · **Velocity:** 35.7/day · [GitHub](https://github.com/ATOM00blue/machine-learning-library)

*Captured 2026-05-31*

---

## What problem does it solve?

ML practitioners waste hours hunting for high-quality learning materials scattered across arXiv, university course sites, and personal blogs — most of which are PDFs or HTML that don't play well with agents or RAG pipelines. This repo solves that by hand-curating 923 of the best ML education resources and normalizing them all to clean Markdown with full source provenance.

## How it works

The library is a static collection of 923 Markdown files organized by topic, sourced from arXiv papers, Stanford/MIT/Karpathy/fast.ai lectures, and explainer articles. A Python pipeline handles the normalization — converting raw PDFs and HTML into consistent Markdown — and each document retains metadata about its original source.

## Best use cases

- Use it as a RAG corpus: point a vector DB or agent at the Markdown files to build a domain-specific ML question-answering system
- Open it in Obsidian to navigate 923 interconnected ML concepts as a personal knowledge base for self-study
- Use it as a fine-tuning dataset: the clean, normalized Markdown with provenance metadata makes it ready to feed directly into LLM training pipelines

## Getting started

Clone the repo and either open the folder in Obsidian for browsing, or point a tool like LlamaIndex or LangChain at the Markdown files to build a RAG pipeline over the full 923-document corpus.