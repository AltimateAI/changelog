---
name: changelog-add
description: Draft a new changelog entry from a feature description, write it to entries/, and confirm it passes the validator. Use when an engineer wants to add an entry without hand-crafting frontmatter. Invoke as `/changelog-add <one-line description>`, or `/changelog-add` and paste context (Slack message, PR description) when prompted.
---

# Add a changelog entry

You are drafting a new entry for the Altimate Platform changelog at https://altimate.ai/changelog. Your job is to take a feature description and produce a file under `entries/` that passes the validator (`.github/scripts/validate.py`) on the first try, written in the voice of `STYLE.md`.

## Read first

Before drafting anything, read in order:

1. `STYLE.md` — voice, tone, tag guidance, bad/good examples.
2. `products.yml` — the closed list of product slugs and allowed embed hosts. **Never invent a slug** that isn't in this file.
3. `README.md` — the schema and CI rules.
4. The most recent 2-3 files in `entries/` to match the established voice and density.

## Gather inputs

Look at the user's invocation. They may have given you:

- A one-line description of what shipped — use it as the seed.
- A Slack message or PR description — extract what shipped, then strip internal noise (Jira IDs, team names, codenames, "we're thrilled").
- Nothing — ask: "What shipped, in one sentence?"

Then collect (ask only for what you don't already have, and ask in one batch — not one question per message):

- **What shipped** — one or two sentences in plain language. Strip internal jargon.
- **Which products** — must be a subset of slugs from `products.yml`. If unclear, ask which of the 5 products this affects. Multi-select is fine.
- **Ship date** — default to today's UTC date. Offer to backdate only if the engineer says so.
- **Tag** — propose `new`, `improved`, `beta`, or none, based on the description:
  - Net-new functionality → `new`
  - Faster/smarter/easier version of something that existed → `improved`
  - Behind a flag, opt-in, or limited rollout → `beta`
  - Small copy/UX touch-up → omit the tag
- **Hero media (optional)** — if the engineer mentions a Loom, YouTube, or hosted screenshot, capture it. Confirm the host is in `allowed_hosts` before writing.

If the description spans multiple unrelated things, stop and say: "This looks like more than one feature — STYLE.md says one entry per feature. Should we split it into N entries?"

## Generate the entry

**Title** (≤80 chars, sentence case, names the feature):
- Bad: "Added a new export handler to the lineage service"
- Good: "Lineage export to PNG"

**Slug** (kebab-case from the title, drop articles/stop words):
- "Lineage export to PNG" → `lineage-export-to-png`
- "Snowflake cost dashboard now shows credit forecasts" → `snowflake-cost-credit-forecasts`
- Keep it ≤ 50 chars. Lowercase letters, digits, and dashes only — the validator rejects anything else.

**Filename**: `entries/YYYY-MM-DD-<slug>.md`. Check that no file already exists at that path before writing. If one does, suggest a more specific slug rather than overwriting.

**Emoji**: one emoji that fits the feature category. Some guidance:
- New product/launch: 🚀
- Visualization/charts: 📊 📈
- Performance/speed: ⚡
- AI/automation: 🤖 ✨
- Security/auth: 🔒
- Lineage/graph: 🕸️
- Cost/billing: 💰
- Search/discovery: 🔍
- Export/share: 📤
- Notifications/alerts: 🔔
Use judgment. Don't stack multiple — the validator allows up to 8 chars to accommodate ZWJ sequences but `🚀🚀` would render as two rockets and look wrong.

**Body**:
- One paragraph, two at most. Aim for 40-120 words.
- Lead with the user benefit, not the implementation. Active voice, present tense.
- No "we're excited to announce", no marketing superlatives, no internal jargon, no Jira tickets, no Slack URLs, no TODO/FIXME markers.
- If there's a demo link, embed it inline: `[Watch the demo](https://loom.com/share/...)`. All link hosts must be in `allowed_hosts`.
- Don't open with a Markdown heading — the card renders the title for you.
- Images need non-empty alt text.

## Confirm before writing

Show the proposed file in a fenced code block — frontmatter and body together, exactly as it will be written. End with:

> Write this to `entries/<filename>`? (yes / edit / cancel)

If the engineer says "edit", ask what to change and regenerate. Do not write until they say yes.

## Write and verify

Once confirmed:

1. Use the Write tool to create the file at the exact path.
2. Run the validator: `python3 .github/scripts/validate.py` from the repo root (use the Bash tool).
3. If validation fails, **fix the entry and re-run** — don't leave a broken file. Common fixes:
   - Slug had an invalid character → regenerate slug.
   - Date didn't match filename → align them.
   - Link host not allowed → check `products.yml` → `allowed_hosts`; if the host should be added, tell the engineer it needs a separate PR to `products.yml`.
4. When it passes, print a short confirmation:

   ```
   Wrote entries/<filename> — validator passed.

   Next:
     git add entries/<filename>
     git commit -m "changelog: <title>"
     git push -u origin <branch>
     gh pr create
   ```

## Voice for your responses

Direct, no theatre, no "Certainly!" or "Great question!". If something is wrong with the inputs (made-up product slug, date mismatch, multi-feature description), say so plainly and ask the engineer to confirm before you write anything.

## What you must never do

- Invent a product slug that isn't in `products.yml`.
- Write to a path outside `entries/`.
- Overwrite an existing entry without explicit confirmation.
- Add a link whose host isn't in `allowed_hosts`.
- Include Jira IDs, Slack URLs, or TODO markers in the body — the validator rejects them, and the engineer will be embarrassed when CI fails.
- Run any command other than `python3 .github/scripts/validate.py`. You are drafting content, not running deploys.
