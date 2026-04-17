---
decision_id: RETRO-2026-04-11-intent-site-2
title: "Product Team Operating Model for Site Maintenance"
date: 2026-04-11
status: accepted
source: retroactive-extraction
---

## Context

The site sync revealed that ad-hoc site updates inevitably fall out of sync with the product repo. Without a defined process, every architectural change creates a hidden debt of site content that needs updating.

## Decision

Adopted a product team operating model for site maintenance with explicit Definition of Ready and Definition of Done:

**Definition of Ready:** Every site change must trace to a source-of-truth change in the product repo via `content-map.md`. No site change is ready for implementation unless the corresponding product repo change is already landed and documented.

**Definition of Done:** A site change is done when ALL of the following are true:
1. `content-map.md` updated with traceability entry
2. All 10 site contracts pass
3. Governance docs reflect the change
4. CHANGELOG updated

## Consequences

- Site maintenance becomes a downstream pipeline from product development
- Drift between site and product repo is structurally prevented, not culturally managed
- The 10 site contracts serve as automated regression tests
