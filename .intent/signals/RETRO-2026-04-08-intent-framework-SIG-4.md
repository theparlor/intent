---
signal_id: RETRO-2026-04-08-intent-framework-SIG-4
title: Zero existing artifacts have 3-finding compression or depth guarantee audits
severity: medium
detected: 2026-04-05
status: open
source: retroactive-extraction
trust_score: 0.48
autonomy: L1
---
# Pre-Depth-Guarantee Artifacts Lack Compression and Audits

## Observation
All 20 artifacts in the registry pre-date the depth guarantee methodology. None has a 3-finding compression section. None has a depth guarantee audit table. F&G's dossier (densest at 35KB, depth_score 6) is closest to the new standard but still lacks formal structure.

## Context
Depth guarantees, compression forcing function, and audit tables were built in this session. They're forward-looking — encoding what future research should produce. The existing corpus was built without these standards.

## Implication
- Temporal refreshes should add new sections (compression, depth guarantee audit) rather than just appending data
- The context resolver can handle missing metadata gracefully but the gap will be visible
- First refresh execution should serve as the retrofit template
- Not urgent: the resolver adapts. Important: first new execution sets the standard.

## Triage note, 2026-07-08

Disposition: still pending, partial. The forward-looking half of this signal landed: the depth guarantee methodology module is built (Core/frameworks/methodology-library/research/depth-guarantees.md) and CLAUDE.md records "depth guarantee retrofits to company-dossier + individual-research" among April's work, so at least those two artifact types got the new structure going forward. What was not verified is a retrofit pass against the specific 20 pre-existing registry artifacts this signal named; no audit trail confirms the original backlog got the compression section and audit table added. Needed control: a one-time retrofit pass over the named 20, or, if the resolver's graceful-degradation behavior is now accepted as sufficient, an explicit decision saying so instead of leaving this open by default.
