---
title: Query analysis agent
date: 2025-12-12
products: [snowflake-app, databricks-app]
tag: new
emoji: 🗺️
authors: ["AI Agents Team:CHIP", "Studio Team:ORBIT"]
description: AI-powered deep analysis of individual queries
---

Click any query in the workload view and the analysis agent walks through it: which scans dominate the cost, which predicates are getting pruned (and which aren't), where clustering would help, and whether the same shape has been run before with different parameters.

Output lands as an inline report with a one-paragraph summary, a cost-saving estimate, and a "try this rewrite" suggestion. The agent runs on the platform's standard reasoning trace so you can audit how it reached every conclusion before acting on it.
