---
title: Table-level lineage now exports to CSV
date: 2026-04-06
products: [datamates]
tag: new
emoji: 🔗
draft: true
description: Download upstream or downstream table lineage as CSV — same export contract as column lineage, one row per edge.
---

Table-level lineage now exports to CSV alongside the existing column-level export. Pick any table, choose upstream or downstream, and download the full BFS traversal as a CSV with Source DB / Schema / Table → Target DB / Schema / Table columns — one row per edge.

The lineage modal also got a z-index fix so it renders above the sidebar backdrop, and long resource keys in the export dialog no longer overflow.
