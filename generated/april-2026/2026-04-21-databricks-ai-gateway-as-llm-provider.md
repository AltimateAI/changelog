---
title: Databricks AI Gateway as an LLM provider
date: 2026-04-21
products: [altimate-code, databricks-app]
tag: new
emoji: 🧱
draft: true
description: Use any of 11 Databricks-hosted foundation models — Llama 3.1, Claude, GPT-5, Gemini, DBRX, Mixtral — as the backing model for Altimate Code.
---

Altimate Code now treats Databricks serving endpoints as a first-class LLM provider. Authenticate with a Databricks PAT in `host::token` format and the provider validates the workspace host for AWS, Azure, or GCP Databricks deployments, then resolves the workspace URL from the PAT or from `DATABRICKS_HOST` / `DATABRICKS_TOKEN` environment variables.

Eleven foundation models register out of the box: Meta Llama 3.1 (405B / 70B / 8B), Claude Sonnet and Opus, GPT-5 variants, Gemini 3.1 Pro, DBRX Instruct, and Mixtral 8x7B. Request bodies are normalized between `max_completion_tokens` and `max_tokens` so each model gets the parameter shape it expects.
