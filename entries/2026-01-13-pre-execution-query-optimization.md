---
title: Pre-execution query optimization tools
date: 2026-01-13
products: [snowflake-app, databricks-app, datamates]
tag: new
emoji: 🤖
authors: ["AI Agents Team:CHIP", "Anand Gupta:ROBOT"]
description: Optimize SQL before it runs via MCP
---

When an agent or a person asks to run a query, the optimizer steps in before execution. It checks the predicate against clustering keys, looks for `SELECT *` on wide tables, flags joins missing predicates, and proposes a rewrite.

The agent sees the proposal as a suggestion it can apply automatically. The human sees it as an inline diff in their IDE. Either way, the optimization runs through the MCP layer — so it works from CLI, IDE, Studio, and any agent built on the Altimate platform, with no separate setup per surface.
