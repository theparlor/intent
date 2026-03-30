---
id: SIG-004
date: 2026-03-28
source: cowork-session
confidence: high
related_intents: []
status: new
---

# Signal: Intent needs three governance dimensions, not just the loop

## Observation

The Intent methodology's core loop (Notice → Spec → Execute → Observe) addresses the flow of work, but Brien surfaced three orthogonal dimensions that any work system must answer:

1. **Right Things** — validate ideas via continuous discovery (Teresa Torres opportunity trees)
2. **Right Time** — parallelize, sequence, and prioritize via dependency graphs (not sprint commitments)
3. **Right Way** — architectural governance via tech radar and permit levels (play/build/operate)

## Implication

The spec and concept brief focus on the loop. But the product needs to explicitly address all three dimensions. Each dimension has its own artifacts:

- Right Things: `.intent/intents/` with discovery status + `.intent/signals/` stream
- Right Time: Spec dependency declarations → Now/Next/Later derived from graph
- Right Way: `.intent/tech-radar.md` + `.intent/decisions.md` + contract boundaries

## Key Insight

All three dimensions can be encoded in the spec file itself — a spec references its parent intent (right thing), declares its dependencies (right time), and cites tech radar constraints (right way). No separate systems or ceremonies needed.

## Evidence

Brien's framing: "build the right things at the right time in the right way and make this flow of work visible at all times" — this is the Intent product's core value proposition stated as a design requirement.
