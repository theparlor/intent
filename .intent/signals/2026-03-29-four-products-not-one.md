---
id: SIG-009
timestamp: 2026-03-29T20:00:00Z
source: conversation
author: brien
confidence: 0.85
trust: 0.15
autonomy_level: L0
status: resolved
cluster:
parent_signal:
related_intents: [product-strategy, roadmap]
upstream_control_path: "DEC-INTENT-008; spec/product-roadmap.md; CLAUDE.md Four Products section"
catch_mechanism: "DEC-INTENT-008 ratified the four-product framing the same day; intent-status roadmap renders the per-product maturity view directly from spec/product-roadmap.md"
verification_command: "cat /Users/brien/Workspaces/Core/frameworks/intent/.intent/decisions/DEC-INTENT-008.md"
---
# Intent is four products (Notice, Spec, Execute, Observe), not one — each needs its own roadmap

The loop phases aren’t just conceptual stages — they’re distinct product surfaces with different users, different maturity levels, and different investment needs. Notice has tooling now (MCP, CLI, GitHub Action). Spec has methodology but no tooling. Execute is deliberately thin (agents do the work). Observe has an event schema but no dashboard.

Treating them as four products within one value stream means each can move at its own pace, and we can see where we're strong vs. where we're starving.

## Triage, 2026-07-08

Disposition: control exists now. DEC-INTENT-008 ratified this framing on 2026-03-28 with an explicit ratification action (spec/product-roadmap.md, intent-status roadmap command), so the ask here was already answered by a same-session decision atom.
