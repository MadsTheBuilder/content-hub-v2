# microsoft/markitdown

> Python tool for converting files and office documents to Markdown.

**Language:** Python · **Stars:** 134,739 · **Velocity:** 950.3/day · [GitHub](https://github.com/microsoft/markitdown)

*Captured 2026-06-01*

---

## What problem does it solve?

Developers and AI engineers constantly need to feed document content into LLMs, but formats like PDF, Word, Excel, and PowerPoint are binary blobs that models can't read directly. Converting these to plain text loses structure, while custom parsers for each format are expensive to build and maintain. markitdown solves this by providing a single unified tool that converts virtually any file format into clean, structured Markdown that LLMs can consume.

## How it works

markitdown is a Python library that routes each input file to a format-specific converter (PDF, DOCX, XLSX, PPTX, images, audio, HTML, ZIP, and more), then normalizes the extracted content into Markdown with preserved structure like headers, tables, and lists. It uses existing Python parsing libraries under the hood for each format and exposes a single MarkItDown class with a convert() method that abstracts all the routing. The output is a MarkdownConverter result object containing the Markdown string ready for downstream use.

## Best use cases

- Preprocessing enterprise documents (contracts, reports, spreadsheets) into Markdown before sending to an LLM for summarization or Q&A
- Building RAG pipelines where source documents in mixed formats need to be chunked and embedded into a vector store
- Automating documentation ingestion — converting legacy Word/PDF docs into Markdown for a static site or knowledge base

## Getting started

Install with 'pip install markitdown' (or 'pip install markitdown[all]' for all format support), then call 'from markitdown import MarkItDown; md = MarkItDown(); result = md.convert("file.pdf"); print(result.text_content)' to get Markdown output from any supported file.