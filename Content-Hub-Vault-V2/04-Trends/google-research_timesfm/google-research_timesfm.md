# google-research/timesfm

> TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting.

**Language:** Python · **Stars:** 32,063 · **Velocity:** 480.7/day · [GitHub](https://github.com/google-research/timesfm)

*Captured 2026-09-09*

---

## What problem does it solve?

Time-series forecasting (demand planning, capacity, finance metrics) traditionally requires training a bespoke model per dataset. TimesFM provides a single pretrained foundation model that forecasts new time series out of the box with little or no fine-tuning, cutting the cost and expertise needed to get usable forecasts.

## How it works

It's a decoder-only transformer pretrained on a large corpus of diverse real-world and synthetic time-series data, using patched inputs so it can generalize across different domains, frequencies, and horizons. At inference time it takes a context window of historical values and autoregressively generates future points in a zero-shot manner.

## Best use cases

- Zero-shot demand and inventory forecasting for retail/supply chain without training a custom model per SKU
- Quick baseline forecasts for finance/business metrics (revenue, traffic, churn) before investing in custom modeling
- Rapid prototyping and benchmarking of forecasting pipelines for data science teams evaluating foundation-model approaches

## Getting started

Install the `timesfm` Python package from the repo, load the pretrained checkpoint via the provided API, and call the forecast function with a numpy/pandas array of historical values to get zero-shot predictions.