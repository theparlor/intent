---
decision_id: RETRO-2026-04-09-intent-rebuild-1
title: Subtract-before-build is the operator protocol after any panel critique
date: 2026-04-09
status: accepted
source: retroactive-extraction
session_date: 2026-04-09
references:
  - theparlor/intent:.intent/signals/2026-04-09-subtract-before-build-reflex.md (SIG-052)
  - Core/personas/operators/brien.yaml (known failure mode #1)
---
# Subtract-before-build is the operator protocol after any panel critique

## Context

After the 2026-04-09 panel review flagged 10 cross-cutting findings (no target user, category confusion, discovery theater, etc.), Brien's initial response was: *"archive what we have and build new material in as many repos as we need to hit the code and architecture changes."* The panels had said the opposite — subtraction and sharpening, not more surface area. Agent pushback (backed by the panel findings) corrected the sequence.

This pattern is general: when receiving structural critique, the default human reflex is to make more things. The correct first move is to delete things until the remaining thing is clear. The sequence matters because building new content before removing old noise compounds the exact problems the critique flagged.

## Decision

Adopt a protocol: after any substantive panel-review critique, the operator (and any agent acting on the operator's behalf) must subtract before building. Specifically:

1. Identify the specific content/artifacts the critique flagged as wrong or redundant
2. Archive (not delete) those artifacts with a clear "v[N] of the framing" label
3. Delete the content inline from any active pages
4. Measure: target 30% surface-area reduction before writing any new content
5. Only then begin the rebuild

## Alternatives Considered

1. **Trust the builder's instinct** — rejected because Brien's own instinct in this session was build-more, and the panels were right that subtract-more was the correct move. The instinct is the failure mode, not the safeguard.

2. **Parallel subtract + build** — rejected because subtraction informs what the build should be. Building in parallel tends to reproduce the old structure with new words.

3. **Formal change-control for every deletion** — rejected because it adds friction to the corrective action at the exact moment friction is the enemy. Archive (not delete) preserves rollback without blocking the corrective.

## Consequences

- Brien-operator persona (`Core/personas/operators/brien.yaml`) explicitly captures this as a known failure mode with a corrective prompt: *"Rumelt says strategy is choosing what NOT to do. What are you deleting first?"*
- Panel-review skill's output should include an explicit "what to subtract first" section for any critique it produces, not just "what's wrong."
- Session-extraction should flag sessions where the delete-to-build ratio is below 1:1 as a signal of potential pattern repeat.
- The archive/ directory pattern used in intent-site/docs/archive/v1.2-multi-framing/ becomes the reference implementation for this protocol.
