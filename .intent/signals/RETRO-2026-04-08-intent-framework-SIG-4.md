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
