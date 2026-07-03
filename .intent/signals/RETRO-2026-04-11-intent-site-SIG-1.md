---
signal_id: RETRO-2026-04-11-intent-site-SIG-1
title: "Site-Product Drift Requires Structural Prevention, Not Cultural Discipline"
date: 2026-04-11
severity: medium
status: resolved
resolution: Product team operating model with Definition of Ready/Done adopted
upstream_control_path: ".intent/decisions/RETRO-2026-04-11-intent-site-2.md (accepted DoR/DoD operating model) + intent-site/content-map.md (139 traceability rows as of 2026-07-03)"
catch_mechanism: "intent-site/site-contracts.md (14 contracts, run after any docs/ change) + intent-site/.github/workflows/freshness-check.yml (daily scheduled drift check vs product repo, files issues on divergence)"
pipeline_survival: "content-map.md maturity final and maintained through IA v3 (2026-06-05); contract set grew from 10 to 14 while staying the commit gate; freshness workflow runs on cron independent of anyone remembering"
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

## Remediation note (2026-07-03)

Closure-DoD keys added retroactively; this April signal predates the key convention. Resolution verified against repo state 2026-07-03: the operating-model decision is accepted at .intent/decisions/RETRO-2026-04-11-intent-site-2.md; content-map.md in theparlor/intent-site carries 139 traceability rows (maturity final, updated through IA v3 on 2026-06-05); site-contracts.md grew from 10 to 14 contracts and stayed the run-after-any-change gate; .github/workflows/freshness-check.yml runs a daily scheduled drift check against the product repo and files issues on divergence. The structural prevention this signal called for exists and has operated since adoption. Status resolved stands.
