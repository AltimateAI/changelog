---
title: SSO inactivity timeout (per-tenant)
date: 2026-04-22
products: [snowflake-app, databricks-app, datamates]
tag: new
emoji: 🔐
draft: true
description: Auto-log-out SSO users after N minutes of inactivity, configured per tenant.
---

Tenants can now set a hard inactivity timeout for SSO users. The new `ssoUserRefreshMins` tenant setting, when positive, logs SSO users out after that many minutes of inactivity — either when the tab is closed and reopened, or when the cursor leaves the window long enough.

The control is per-tenant: tenants with stricter compliance requirements can pick a tight window without affecting tenants that don't need one. Default behavior is unchanged (no forced timeout) when the setting is unset.
