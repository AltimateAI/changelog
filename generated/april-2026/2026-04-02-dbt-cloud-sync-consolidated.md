---
title: dbt Cloud sync, 5x faster
date: 2026-04-02
products: [dbt-power-user, datamates]
tag: improved
emoji: 🧰
draft: true
description: dbt Cloud sync consolidates ~1000 daily tasks per project/environment into a single ingestion run, cutting sync time from ~250 min to under 50.
---

dbt Cloud sync no longer creates one ingestion task per dbt Cloud run. The sync now consolidates to one task per `(project, environment)` per cycle — so a project firing 1000 runs a day produces one ingestion run instead of 1000 redundant ones.

Manifest parsing, health checks, and PostgreSQL upserts each happen once per node per cycle instead of ~20 times, dropping a typical 4-worker sync from ~250 min to under 50.
