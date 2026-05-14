---
title: Chat panel polish — instant open, title bar icon, token usage indicator
date: 2026-04-11
products: [datamates]
tag: improved
emoji: ⚡
draft: true
description: The Altimate MCP chat panel opens with no perceptible delay, lives on the editor title bar, and shows live token usage in the header.
---

Opening the Altimate MCP chat panel used to wait for an `isInstalled()` check before rendering. The panel now appears immediately and runs the install check on the webview-ready handler, so there's no perceptible delay between clicking and seeing the panel.

A new Altimate icon lands on the editor title bar (right after the run button) for one-click access without the command palette. The header also picks up a compact token usage indicator pulled from `/payment/token-usage` — usage percentage color-coded blue / orange / red against your monthly threshold, or "Unlimited" on unlimited plans. Click it for a detailed popover with allowance, grants, overage, billing period, and wallet balance.
