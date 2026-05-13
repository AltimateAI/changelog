---
title: New changelog, updated without a redeploy
date: 2026-05-13
products: [dbt-power-user, snowflake-app, databricks-app, altimate-code, datamates]
tag: new
emoji: 📜
authors: ["Anand Gupta:ROBOT", "Claude Opus 4.7:CHIP"]
description: A new GitHub-backed source for the changelog — any engineer can ship an entry by opening a PR.
---

The changelog at [altimate.ai/changelog](https://altimate.ai/changelog) is now sourced from a separate public repo at [github.com/AltimateAI/changelog](https://github.com/AltimateAI/changelog). Any engineer can ship an entry by opening a PR. No website redeploy required — new entries appear on the page within a few minutes of merge.

## How to add an entry

Three options, in order of friction:

1. **`/changelog-add`** — run Claude Code in the repo and let it draft the entry from a one-line description.
2. **Hand-write** the markdown using the template in [the README](https://github.com/AltimateAI/changelog).
3. **`/changelog-polish`** — paste a draft you wrote, get a STYLE.md-aware rewrite back.

CI validates the schema on every PR — frontmatter, body length, link allowlist, no internal jargon. A pre-commit hook runs the same checks locally so you catch failures before pushing.

## What you can put in an entry

Everything you'd want to share with a customer: links, screenshots, embedded Loom or YouTube videos, code snippets, and a `// SHIPPED BY` footer crediting the engineers who built it. Each author picks a pixel-art avatar that flips in place when the page loads.
