# anthropics/financial-services

> 

**Language:** Python · **Stars:** 29,060 · **Velocity:** 704.5/day · [GitHub](https://github.com/anthropics/financial-services)

*Captured 2026-06-01*

---

## What problem does it solve?

Financial services teams want to leverage large language models for tasks like document analysis, compliance review, and customer support, but lack practical, production-ready examples tailored to the regulatory and data-sensitivity constraints of the industry. Generic AI demos don't address the nuances of finance — auditability, accuracy, and risk. This repo bridges that gap with Anthropic's Claude API.

## How it works

It's a Python-based reference implementation that uses the Anthropic Claude API to demonstrate financial services workflows — likely covering document parsing, Q&A over financial data, summarization of reports, and agentic task patterns. The code provides reusable patterns and prompt templates tuned for financial contexts, wiring Claude's tool use and structured output capabilities into realistic finance scenarios.

## Best use cases

- Automated analysis of earnings reports, SEC filings, or loan documents
- Compliance and risk document review with cited reasoning
- Customer-facing financial Q&A assistants backed by internal knowledge bases

## Getting started

Clone the repo, install dependencies via pip, set your ANTHROPIC_API_KEY environment variable, and run the example scripts — each likely maps to a specific financial workflow you can adapt to your own data.