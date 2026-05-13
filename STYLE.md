# Style guide

The changelog is read by customers, prospects, and analysts. It is not internal release notes. Write for the reader, not the team.

## What makes a good entry

- **One feature per entry.** If your PR shipped three things, write three entries.
- **Lead with the user benefit, not the implementation.** "Export lineage to PNG in one click" beats "Added a new export handler to the lineage service."
- **Title is a feature name, not a sentence.** Bold, concrete, ≤ 80 chars.
- **Body is one short paragraph (or two).** Anything longer probably wants a blog post that this entry links to.
- **Show, don't tell.** A 20-second Loom or a labelled screenshot is worth more than two paragraphs.

## Tag guidance

- `new` — net-new functionality the user couldn't do before.
- `improved` — an existing feature got faster, smarter, or easier.
- `beta` — available behind a flag, opt-in, or limited rollout. Set expectations honestly.
- Omit the tag for genuinely small things (copy changes, bug fixes worth mentioning).

## Voice

- Active voice, present tense: "Lineage now exports to PNG", not "PNG export has been added to lineage".
- No internal jargon (project codenames, Jira IDs, team names). Translate before publishing.
- No "we" theatre. Skip "we're excited to announce" and "delighted to share". Just say what shipped.
- No marketing superlatives ("revolutionary", "game-changing", "next-generation"). Let the feature speak for itself.

## Links and media

- **Loom and YouTube** are the preferred video hosts. Both are in `products.yml` → `allowed_hosts`.
- **Screenshots** should be hosted in this repo (an `assets/` directory works) or on `raw.githubusercontent.com`. Hot-linking from a vendor's CDN breaks when they rotate URLs.
- **Internal links** should point to `altimate.ai`, `docs.altimate.ai`, or `github.com/AltimateAI/...`.
- **No raw HTML** in the body. If you need an embed beyond Loom/YouTube/Vimeo, propose adding the host to `products.yml` in a separate PR.

## Bad → good examples

> ❌ "Improved query performance in the dbt extension."
>
> ✅ "Long-running dbt queries now stream results as they arrive, so you see the first rows in seconds instead of waiting for the full result set."

> ❌ "AI-1234: Added new visualization for column lineage."
>
> ✅ "Column-level lineage now renders inline in the model view — click any column to see exactly where its data came from."

> ❌ "We're excited to announce a brand-new release of our Snowflake App with revolutionary cost insights."
>
> ✅ "The Snowflake App now flags warehouses that are over-provisioned by more than 50% over the trailing 30 days, with a one-click resize suggestion."
