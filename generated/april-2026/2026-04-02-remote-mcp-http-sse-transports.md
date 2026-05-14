---
title: Remote MCP setup with HTTP and SSE transport options
date: 2026-04-02
products: [datamates, altimate-code]
tag: improved
emoji: 🔌
draft: true
description: The remote MCP setup screen now offers Streamable HTTP and SSE transport tabs, each pre-filled with the right config and auth headers.
---

The remote MCP setup screen now lets you pick between two transports. The Streamable HTTP tab uses `type: "http"` with the `/mcp` endpoint and is the default for Claude and most clients; the SSE tab uses `type: "sse"` with the `/sse` endpoint for clients that don't speak streamable HTTP — Cursor users in particular.

Each tab fills in the matching config snippet and auth headers, so it's a copy-paste away from a working connection.
