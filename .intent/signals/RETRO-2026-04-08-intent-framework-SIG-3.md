---
signal_id: RETRO-2026-04-08-intent-framework-SIG-3
title: Core/reference reusable scan directories don't exist yet
severity: medium
detected: 2026-04-05
status: open
source: retroactive-extraction
trust_score: 0.42
autonomy: L1
---
# Core Reference Directories Empty

## Observation
The 4 planned reusable scan directories (Core/reference/industries/, Core/reference/domains/, Core/reference/concepts/, Core/reference/tools/) don't exist. All research output has been engagement-scoped, never promoted to Core/reference for cross-engagement reuse.

## Context
New research skills (industry-scan, domain-scan, product-analysis, concept-exploration) specify storage to these directories for reusable scans. Agent scans of all 4 directories confirmed they don't exist.

## Implication
- First industry-scan or domain-scan execution should create the directory structure
- An automotive industry scan for Subaru is also reusable for any future automotive engagement
- The promotion pattern (engagement-specific → Core/reference) needs to be part of post-execution storage logic in the orchestrator
- Self-healing gap — will resolve naturally once research skills execute

---

## Triage note — 2026-05-28 (still open)

**Status:** still open. `Core/reference/` exists with other content (rate card, materials/brass, usage-tracker, etc.) but the four planned reusable scan directories (`industries/`, `domains/`, `concepts/`, `tools/`) do not exist. No industry-scan or domain-scan skill has been executed against the Core/reference target. The signal's own note says "self-healing gap, will resolve naturally once research skills execute", that hasn't happened yet. Still valid; low urgency per original severity: medium / trust: 0.42.

## Triage note, 2026-07-08 (still open)

Disposition: still pending. Reconfirmed directly: none of the four directories exist as of today (`ls Core/reference/industries Core/reference/domains Core/reference/concepts Core/reference/tools` all fail with "No such file or directory"). Two months after the 2026-05-28 note, the same gap persists; "self-healing" has not happened across two check-ins. Needed control: this stops being self-healing and becomes a real backlog item, either run one industry-scan or domain-scan against a live engagement to seed the first Core/reference/industries/ entry, or downgrade the research-skill specs so they stop pointing at directories nothing has ever populated.
