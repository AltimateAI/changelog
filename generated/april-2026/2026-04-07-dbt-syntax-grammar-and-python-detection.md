---
title: dbt SQL+Jinja syntax highlighting and "Detect Python from terminal"
date: 2026-04-07
products: [dbt-power-user]
tag: improved
emoji: 🎨
draft: true
description: Proper TextMate grammars for dbt SQL+Jinja and YAML+Jinja, plus a one-click way to fix mismatched Python interpreters.
---

dbt Power User ships dedicated TextMate grammars for dbt SQL+Jinja and YAML+Jinja. `ref`, `source`, `config`, SQL aggregates, window functions, Jinja `{{ }}`/`{% %}`/`{# #}` blocks, and operators each get distinct scopes — schema YAML files highlight Jinja inline alongside YAML, and SQL files no longer fall back to a generic grammar that mis-colored half the keywords.

The most-reported onboarding bug — dbt works in the terminal but not in the extension because the Python extension picked a different interpreter — gets a dedicated **Detect Python from terminal** action. It spawns a login shell to find where `dbt` actually lives and writes that path to `dbtPythonPathOverride`. The button appears on every Python/dbt error dialog and in the onboarding prerequisites step.
