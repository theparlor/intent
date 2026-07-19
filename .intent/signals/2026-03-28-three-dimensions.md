---
id: SIG-004
date: 2026-03-28
source: cowork-session
confidence: high
related_intents: []
status: open
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

Brien's framing: "build the right things at the right time in the right way and make this flow of work visible at all times" - this is the Intent product's core value proposition stated as a design requirement.

## Triage, 2026-07-08

Disposition: still pending, partial. Right Things and Right Time are operationalized: .intent/intents/ carries discovery status, the intent-intent CLI has a --priority flag, and specs can declare dependencies. Right Way stays informal. There is no .intent/tech-radar.md and no permit-level (play/build/operate) tagging anywhere in the repo; decisions.md and the DEC-INTENT-NNN atoms cover architectural precedent but not a radar-style forward view. Needed control: either author .intent/tech-radar.md with permit levels as this signal specified, or fold a permit_level field into the DEC-INTENT frontmatter schema so Right Way rides the same mechanism as the other two dimensions.

Reconciliation note, 2026-07-19: the remote-side 2026-07-02 hygiene pass batch-classified all five founding 2026-03-28 signals as status: incorporated (terminal). The 2026-07-08 per-file triage above found this one is the exception: Right Things and Right Time are operationalized but Right Way has no control (no .intent/tech-radar.md, no permit-level tagging). Status set to open, the hygiene pass's own vocabulary for un-built items, because the per-file evidence is stronger than the batch classification. The other four founding signals stay terminal.
