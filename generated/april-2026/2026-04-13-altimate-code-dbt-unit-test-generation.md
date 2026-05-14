---
title: Generate dbt unit tests from your manifest
date: 2026-04-13
products: [altimate-code, dbt-power-user]
tag: new
emoji: 🧪
draft: true
description: A new `dbt_unit_test_gen` tool inspects compiled SQL and writes dbt unit tests with type-correct mock data, including incremental and ephemeral cases.
---

Altimate Code now generates dbt unit tests for you. Point it at a model and the new `dbt_unit_test_gen` tool reads the manifest and compiled SQL, detects scenarios (CASE branches, JOINs, GROUP BY, division-by-zero, incremental loads), and emits a `unit_tests:` block in the model's schema YAML with type-correct mock data — happy path, null variants, and boundary cases.

Incremental models get an `input: this` mock for the prior-state row; ephemeral upstream models use `format: sql` even when their column types aren't yet known. Cross-database — Snowflake, Databricks, BigQuery, Redshift, Postgres — works through the same `schema.inspect` adapter.
