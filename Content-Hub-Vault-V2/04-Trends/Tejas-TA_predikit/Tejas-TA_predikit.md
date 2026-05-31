# Tejas-TA/predikit

> The missing bridge between your ML models and your AI agents.

**Language:** Python · **Stars:** 30 · **Velocity:** 6.0/day · [GitHub](https://github.com/Tejas-TA/predikit)

*Captured 2026-05-31*

---

## What problem does it solve?

AI agents built with frameworks like LangChain or AutoGen can reason and plan, but they have no native way to call traditional ML models (scikit-learn, XGBoost, etc.) as tools. Developers are forced to hand-roll custom wrappers every time they want an agent to run a prediction. predikit standardizes that bridge so ML models become first-class, callable tools inside any AI agent workflow.

## How it works

predikit wraps trained ML model artifacts and exposes them as structured tool interfaces that AI agent frameworks can discover and call. Written in Python, it likely handles serialization, input/output schema generation, and the tool-calling contract so the agent receives a clean prediction response without knowing anything about the underlying model format.

## Best use cases

- An AutoGen agent that calls a churn-prediction model mid-conversation to decide whether to escalate a customer support ticket
- A LangChain pipeline that routes user queries through a topic-classification model before choosing which retrieval chain to invoke
- A data analyst agent that runs a trained regression model on uploaded CSV data and returns forecasts as part of a multi-step reasoning loop

## Getting started

Install the package via pip, wrap your trained model artifact with predikit's model tool class, then register it as a callable tool in your agent framework of choice — the library handles the schema and invocation contract automatically.