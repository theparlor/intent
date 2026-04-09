---
id: SIG-052
timestamp: 2026-04-09T04:52:00Z
source: conversation
confidence: 0.8
trust: 0.75
autonomy_level: L2
status: captured
cluster: execution-posture
author: panel-review-2026-04-09
related_intents: []
referenced_by: []
parent_signal:
---
# Brien's reflex to "build more" when panels said "subtract more" — meta-failure pattern

During 2026-04-09 session, Brien's response to the panel critique was "archive what we have and build new material in as many repos as we need." The panels said the opposite: *subtraction and sharpening, not more surface area*.

Both moves are valid at different times, but the sequence matters. If you build before you subtract, you add surface area before removing noise — compounding the exact problem the panels flagged (category confusion, no target user, discovery theater).

## Why this is a signal

This is a meta-pattern about execution posture, not a one-time content issue. When receiving structural critique, the default reflex is "make more things" — but the correct first move is "delete things until the remaining thing is clear." This applies to:

- Content (delete 5 of 6 framings before writing new ones)
- Products (pick ONE wedge before shipping Intent+KE+SE as three)
- Documentation (archive the current 25-page site before drafting new pages)
- Personas (don't add operator persona until the existing 178 are catalogued for relevance to the wedge user)

## Implication

The operator-self-persona (SIG-048) should explicitly capture this reflex and its corrective. When Brien-the-operator makes the "build more" move, the self-persona should prompt: *"Rumelt says strategy is choosing what NOT to do. What are you deleting first?"*

This is exactly the kind of "self-prompt during self-directed development" use case the operator persona is for.

## Required outcome

- Operator persona captures this pattern as a known failure mode with corrective prompt
- Post-critique execution protocol: "Delete for a day before building. Return to build after the surface area has been reduced by 30% minimum."
- Panel-as-a-service primitive should flag this pattern when it detects critique-then-build cycles

## Trust Factors

- Clarity: 0.8 (pattern is observable in this session)
- Blast radius: 0.3 (affects execution posture, not architecture)
- Reversibility: 1.0 (self-correction is cheap)
- Testability: 0.7 (can measure delete-to-build ratio in each session)
- Precedent: 0.9 (Rumelt, Porter, Perri all prescribe subtraction-first)
