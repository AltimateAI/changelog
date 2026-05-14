---
title: LLM Guard blocks prompt injection and poisoning
date: 2026-04-02
products: [snowflake-app, databricks-app, datamates]
tag: improved
emoji: 🛡️
draft: true
description: Studio's agent gateway now blocks nine new injection categories — instruction override, role hijacking, system-prompt extraction, payload obfuscation, multi-turn poisoning, and more.
---

The agent gateway used by Studio's `/chat/completions` now blocks nine new categories of prompt-injection and prompt-poisoning attempts before they reach the model: instruction override, role hijacking, system-prompt extraction, security bypass, fake system tokens, payload obfuscation, indirect injection (via tool output or documents), social engineering, and multi-turn poisoning.

Existing AI-model-identification detection continues to work. The added checks run in front of the same agent endpoint, so all Studio surfaces get the upgraded coverage automatically.
