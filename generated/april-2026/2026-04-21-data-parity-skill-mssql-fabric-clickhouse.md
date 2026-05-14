---
title: Data-parity diffs across SQL Server, Fabric, and ClickHouse
date: 2026-04-21
products: [altimate-code]
tag: new
emoji: 🔁
draft: true
description: Altimate Code can now diff data across SQL Server / Azure Fabric and ClickHouse with partition-aware execution and seven Azure AD auth flows.
---

Altimate Code's `data_diff` tool now handles three more warehouses end-to-end. SQL Server and Azure Fabric drop in with full T-SQL support — `TOP` injection, `sys.*` catalog queries, `DATETRUNC()` and `CONVERT(DATE, …, 23)` for date partitioning. Azure AD authentication covers seven flows (`default`, `password`, `access-token`, `service-principal-secret`, `msi-vm`, `msi-app-service`), with shorthand aliases (`cli`, `msi`, `service-principal`) for the common cases.

The orchestrator that drives the diff is now a TypeScript layer that runs SQL tasks produced by the Rust state machine and feeds results back — so the algorithm and the database access stay independently swappable, and partitioned diffs run independently per partition before merging outcomes.
