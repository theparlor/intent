---
signal_id: RETRO-2026-04-11-intent-site-SIG-1
title: "Site-Product Drift Requires Structural Prevention, Not Cultural Discipline"
date: 2026-04-11
severity: medium
status: resolved
resolution: Product team operating model with Definition of Ready/Done adopted
source: retroactive-extraction
sessions: [local_83d2e42b]
---

## Signal

The intent-site sync revealed that 10 HTML pages and 5 governance docs had drifted from the product repo state. Multiple architectural decisions (D7-D12), the three-layer architecture, Knowledge Engine separation, fourth MCP server, spec-shaping protocol, and federated KB had all been implemented but not propagated to the site.

The drift accumulated invisibly — no one noticed until a deliberate sync was attempted. This is the classic "documentation debt" pattern: each individual change seems small, but the cumulative effect is a site that tells a fundamentally different story than the product.

## Root Cause

No structural mechanism to flag when product changes create site debt. The content-map.md existed but wasn't used as a diff tool.

## Resolution

Adopted a product team operating model:
- Definition of Ready: every site change must trace to a source-of-truth change in the product repo via content-map.md
- Definition of Done: content-map updated, all 10 site contracts pass, governance docs reflect change, CHANGELOG updated
- 51+ new traceability entries added to content-map.md

## Pattern to Watch

This same drift pattern applies to ANY documentation surface — CLAUDE.md files, engagement handoffs, persona registries. The countermeasure is always: structural traceability links + automated contract validation, not "remember to update it."
