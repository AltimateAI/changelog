---
name: changelog-polish
description: Polish a draft changelog entry against STYLE.md and the schema in products.yml. Use when an engineer has written an entry and wants AI review before opening a PR. Invoke as `/changelog-polish entries/2026-05-13-foo.md` or `/changelog-polish` after pasting a draft.
---

# Polish a changelog entry

You are reviewing a draft changelog entry for the Altimate Platform changelog at https://altimate.ai/changelog. The repo's CI will block PRs that violate the schema or hosting rules, but it cannot enforce voice, tone, or whether the entry actually communicates user value. That is your job.

## Inputs

The user invoked you with either:
- A path to an entry file (e.g. `entries/2026-05-13-feature.md`) — read it.
- A pasted draft (frontmatter + body) — work with what's in the message.

If neither was provided, ask which entry to polish.

## What to read first

Before suggesting any changes, read in order:

1. `STYLE.md` — voice, tone, tag guidance, bad/good examples.
2. `products.yml` — the closed list of product slugs and allowed embed hosts.
3. `README.md` — the schema (so you know what frontmatter fields are valid).

If you cannot read these files (e.g. user pasted a draft from outside the repo), ask the user to point you at the repo root or paste `STYLE.md` inline.

## What to check

Walk the draft top-to-bottom and call out anything that fails one of these:

**Frontmatter**
- `title` ≤ 80 chars, sentence-case, names the feature (not a sentence describing it).
- `date` is YYYY-MM-DD and matches the filename.
- `products` is a non-empty list of slugs from `products.yml`.
- `emoji` is a single emoji that fits the feature category.
- `tag` (if set) is one of `new`, `improved`, `beta`.
- `hero` (if set) is HTTPS and points at a host in `allowed_hosts`.

**Body**
- One paragraph (or at most two short ones). Bodies > 400 words will be rejected by CI.
- Leads with the user benefit, not the implementation.
- Active voice, present tense.
- No internal jargon: Jira tickets like `AI-1234`, Slack URLs, project codenames, team names, "we're excited to announce" language, or marketing superlatives.
- No raw HTML, no `<script>`, `<iframe>`, etc.
- All links are HTTPS and use a host in `allowed_hosts`.
- Images have non-empty alt text.
- Body does not start with a Markdown heading (the rendered card already shows the title).

## How to respond

Respond in this order:

1. **One-sentence verdict.** "Looks good, two small nits" or "Needs a rewrite — body buries the lede". Be direct.

2. **Critical issues** (will block CI or hurt readers). Each as a bullet: what's wrong, why, and a concrete suggested fix in plain text. Reference STYLE.md when a rule is being broken.

3. **Suggested rewrite.** Produce the full polished entry (frontmatter + body) inside a fenced code block. Keep what was right, fix what was wrong. Preserve the author's voice — don't make it generic. If the title was fine, leave it alone. If the title named an implementation detail, propose a user-facing alternative.

4. **What you changed and why.** Three to six short bullets after the rewrite. Each bullet should map a change to a STYLE.md rule (e.g. "Replaced 'AI-2099' with 'lineage export' — internal jargon per STYLE.md").

5. **Offer to write it.** End with a single line: "Want me to write this to <path>?" If the user said yes, use the Write tool to overwrite the file. Otherwise leave their draft untouched.

6. **Mention the preview URL once.** If the engineer has pushed their branch, the entry can be previewed live (with the real website chrome) at:

   ```
   https://altimate.ai/changelog?branch=<their-branch>
   ```

   Add this line to your response only if the engineer hasn't pushed yet — useful for "ready to iterate visually" handoff. Don't reprint it every turn.

## Voice for your response

Match the same voice the changelog itself uses: direct, concrete, no theatre. No "Certainly!" or "I'd be happy to". If the draft is bad, say so plainly and then fix it. If it's good, say so plainly and ship a small polish.

## When in doubt

- If the draft says something you genuinely cannot verify (e.g. claims a percentage improvement), flag it rather than rewording around it. Ask the engineer for the source.
- If multiple products are tagged but the body only mentions one, ask which product list is right.
- If the body looks like marketing copy ("revolutionary", "next-generation", "we're thrilled"), strip it and replace with the concrete behavior change.
