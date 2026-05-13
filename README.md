# Altimate Platform Changelog

Source of truth for `https://www.altimate.ai/changelog`.

Each shipped feature, improvement, or beta launch becomes one Markdown file in `entries/`. The website fetches this repo at request time (no rebuild required), so a merged PR here is live on the site within ~5 minutes.

## Add an entry in 3 steps

1. **Create a file** under `entries/` named `YYYY-MM-DD-kebab-slug.md`.
2. **Fill in the frontmatter and body** (see template below).
3. **Open a PR.** CI validates the schema; once green and merged, the entry appears on the site.

## Template

```markdown
---
title: One-line feature name (≤80 chars, becomes the bold heading)
date: 2026-05-13
products: [dbt-power-user]   # one or more — see products.yml for the list
tag: new                     # optional: new | improved | beta
emoji: 🚀                    # one emoji
hero: https://loom.com/share/...   # optional: video/image shown above the fold
---

One short paragraph (or a few) describing what shipped and why a user cares. Links, code blocks, lists, and images are fine. [Demo video](https://loom.com/share/...).

Keep it under 400 words. If you need more, the feature probably deserves a blog post that the entry links to.
```

## Claude Code skills (recommended path)

This repo ships two Claude Code skills under `.claude/skills/`. They auto-load when you run Claude Code from the repo root.

**`/changelog-add`** — draft a new entry from scratch.

```
/changelog-add Lineage now exports to PNG in one click
```

Claude reads `STYLE.md` + `products.yml`, asks which products it affects (closed list), generates a properly-named file with valid frontmatter and body, shows you the draft, and writes it after you confirm. Always finishes by running the validator so what lands on disk is already CI-clean.

**`/changelog-polish`** — review an existing draft.

```
/changelog-polish entries/2026-05-13-your-slug.md
```

Claude walks the draft, flags voice/jargon/structure issues, and proposes a polished rewrite. CI enforces the schema; the skill enforces what CI can't — voice, lede, internal jargon, marketing-speak.

## Run the validator before committing (recommended)

The same Python validator that gates merges in CI can run as a git pre-commit hook so failures surface before you push.

**Option A — native git hook (no external tooling):**

```bash
git config core.hooksPath .githooks
```

That's it. The hook in `.githooks/pre-commit` runs the validator on every commit that touches `entries/`, `products.yml`, or the validator itself. Skip with `git commit --no-verify` if you really need to.

**Option B — pre-commit framework (if you already use it):**

```bash
pip install pre-commit
pre-commit install
```

Uses `.pre-commit-config.yaml`. Runs both the schema validator and `markdownlint-cli2`.

The hook needs Python 3.10+ and PyYAML on `$PATH`. If PyYAML is missing it prints the install command and fails the commit.

## What's enforced by CI

Three workflow jobs run on every PR. All three must pass before merge.

**1. Schema + content rules** (`.github/scripts/validate.py`)

- Filename matches `YYYY-MM-DD-kebab-slug.md` and the date matches frontmatter.
- `title` (≤80 chars), `date`, `products`, `emoji` present and well-formed.
- `description` (optional one-line preview) is ≤200 chars if set.
- `products` values are all in `products.yml`; no duplicates.
- `tag` (if set) is one of `new`, `improved`, `beta`.
- Date is not in the future and not before 2020.
- Body is ≤400 words, not empty, doesn't start with a Markdown heading.
- No internal jargon: Jira tickets (`AI-XXXX`), Slack URLs, or `TODO`/`FIXME`/`XXX` markers.
- No raw `<script>`, `<iframe>`, `<style>`, `<object>`, `<embed>`, `<link>`, or `<meta>` tags.
- All links and `hero` URLs are HTTPS and use a host in `products.yml` → `allowed_hosts`.
- Images have non-empty alt text.
- No CRLF line endings, no tabs, no trailing whitespace.

**2. Markdown formatting** (`markdownlint-cli2`)

Config in `.markdownlint-cli2.jsonc`. Enforces consistent list markers, single h1, alt text on images, no multiple consecutive blank lines, trailing newline.

**3. Link health** (`lychee`, advisory on PRs)

Each external link in the diff is HEAD-checked. Advisory — a transient 503 from Loom won't block your PR. A separate weekly cron (`.github/workflows/link-check-weekly.yml`) re-checks every entry on `main` and opens an issue with the rotted URLs.

To extend (new product, new allowed embed domain): PR `products.yml`. New product additions also need a UI change in `altimate-website`.

## Style

See [STYLE.md](./STYLE.md) for tone, voice, and what makes a good entry. The `/changelog-polish` skill is built around it.

## Drafts

Set `draft: true` in frontmatter. The website skips draft entries from the published `/changelog` page. Drafts **are** visible in branch preview mode (see below).

## Preview your entry before merging

You don't need to run the website locally. The live site supports a `?branch=` query param that loads entries from any branch of this repo.

1. Push your work to a branch in this repo (e.g. `feat/lineage-export-png`).
2. Open the live site with that branch as the query param:

   ```
   https://altimate.ai/changelog?branch=feat/lineage-export-png
   ```

3. You'll see exactly how your entry renders — same v2 chrome, same card layout, same `// SHIPPED BY` footer — with a yellow banner at the top reminding you that you're previewing a non-main branch.
4. Iterate with more commits to the same branch. The site fetches fresh from GitHub on every page load (no CDN cache), so a hard refresh is enough to see your latest push.
5. Once the PR merges, drop the `?branch=` and the entry is live at `/changelog`.

**Notes:**

- Drafts (`draft: true`) are visible in preview mode but hidden on the main `/changelog`.
- The branch name must match `^[a-zA-Z0-9/_.\-]+$` — anything weird falls back to `main`.
- This works on the live `altimate.ai` site and on any Amplify branch preview of the website (e.g. `https://feat-changelog-v2.<app-id>.amplifyapp.com/changelog?branch=…`).

## How the website consumes this repo

The React Router app in `altimate-website` fetches this repo's `entries/` directory via the GitHub API at request time and caches the result for ~5 minutes. The rendering layer (`react-markdown` + `remark-gfm`) does **not** allow raw HTML, so even if a malicious entry slipped through CI, the browser would render its HTML as escaped text rather than executing it.
