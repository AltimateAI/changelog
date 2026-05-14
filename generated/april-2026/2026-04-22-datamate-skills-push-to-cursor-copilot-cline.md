---
title: Datamate Skills push to Cursor, Copilot, and Cline
date: 2026-04-22
products: [datamates]
tag: new
emoji: 📚
draft: true
description: Skills configured on a Teammate now deliver as Cursor `.mdc`, Copilot `.instructions.md`, or Cline `.clinerules/skills/<id>/SKILL.md` files to your workspace automatically.
---

Datamate Skills are push-based markdown instructions that tell an AI agent when and how to use Datamate MCP tools. From April, the MCP server extension reads each Teammate's `skills[]` from the API and writes them as instruction files into the workspace in the right format for whichever IDE you're running.

Cursor gets `.mdc` files with conditional activation (`alwaysApply` and globs); Copilot gets `.instructions.md`; Cline picks up native `.clinerules/skills/<id>/SKILL.md` files with YAML frontmatter, matching Claude Code's layout. Custom skills slug their file names with an ID suffix so two skills with the same display name don't collide. The DatamateCard shows the custom-skill count alongside Assists and Guardrails, and `always_active` skills attach to every conversation regardless of context.
