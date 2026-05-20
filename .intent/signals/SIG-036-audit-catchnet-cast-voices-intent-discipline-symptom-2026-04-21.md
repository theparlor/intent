---
id: SIG-036
title: Cast/Voices malformation is Intent framework write-through discipline symptom — audit-as-catchnet anti-pattern at architectural scale
date: 2026-04-21
status: open
category: framework-discipline
severity: high
related:
  - memory/feedback_audit_vs_writethrough.md (canonical policy 2026-04-19)
  - SIG-028 (original find-and-fix memory layer gap)
  - SIG-006 (related propagation gap)
  - SIG-034 (entire.io partial landing — parallel write-through gap)
  - SIG-035 (security posture reframe — prevented by same upstream rigor)
  - Core/products/cast/ (downstream — malformed each run)
  - Core/products/voices/ (downstream — dissent-preservation conservation law)
  - Core/frameworks/intent/spec/signal-stream.md (has DoD but enforcement is advisory)
  - Core/frameworks/intent/knowledge-engine/templates/dor-dod-library.md
---

# SIG-036 — Cast/Voices malformation is Intent discipline symptom

## Origin

Session opened 2026-04-21 as routine Cast + Voices status check. Status revealed Cast/Voices running but **malformed after each run, relying on audit to catch drift**. Brien's direct read:

> "the raw signals above indicate significant gaps in this product operating as intended. there is clearly a missing set of discipline and operational sustainable rigor in its execution leaving it malformed after every run and relying on audit to catch drift and misses."

This is not a Cast bug. It is not a Voices bug. It is the **Intent framework's write-through discipline manifesting at architectural scale**.

## Pattern identification

Third tracked instance of the **audit-as-catchnet** anti-pattern — using retrospective audit/cleanup passes as the primary integrity mechanism, instead of write-through gates that prevent malformation at creation time.

| Instance | Layer | Fix attempted | Effective? |
|---|---|---|---|
| SIG-028 (2026-04-15) | Memory layer find-and-fix | Retrospective scans | No — drift kept recurring |
| Cast intake pipeline | 6-stage persona-intake (SPEC-002) | Stage outputs still malformed | Partial — DoR/DoD not enforced per stage |
| Voices dissent preservation | Conservation-law-level concern | Treated as audit observation | No — needs creation-time assertion |

All three share the same shape: **policy exists, enforcement is advisory**.

## Root cause: Intent framework discipline is advisory, not write-through

Cast and Voices are **downstream** of Intent. They inherit whatever rigor the framework actually enforces. Current state of Intent:

- Defines Notice → Spec → Execute → Observe lifecycle ✓
- Defines signal-stream DoD (`Core/frameworks/intent/spec/signal-stream.md`) ✓
- Defines DoR/DoD library (`knowledge-engine/templates/dor-dod-library.md`) ✓
- Defines quality-baseline inviolability policy (memory) ✓
- **Enforces these as gates?** No — advisory.

Without write-through enforcement (hooks, CI, skill-level gates, stage-gates), the discipline is a memorable policy. Downstream products re-experience the same malformation every run. Audit is the catch-net. Audit is not infrastructure.

## Why the fix is upstream, not at Cast/Voices

Tempting fix: *"add an audit step to Cast, add a validation pass in Voices."* Both are **more audit**, compounding the anti-pattern.

**Correct fix:** sub-project #1 (Intent framework rigor audit) — identify where Notice/Spec/Execute/Observe has write-through gates vs. advisory policy, then install the missing gates. Cast and Voices inherit the result.

This is why #1 is sequenced after #2 (coding practices propagated), #5 (observability landed), and #6 (posture understood) — the rigor audit needs:
- Current practices in hand (#2) to audit against
- Clean observability substrate (#5) to measure against
- Posture clarity (#6) to decide which enforcement needs which trust tier

## Concrete upstream vs downstream

| Layer | Fix location | Type | Don't |
|---|---|---|---|
| Cast malformation | NOT at Cast | — | Add more Cast-side audit |
| Voices dissent drift | NOT at Voices | — | Add more Voices validation |
| Intent DoR/DoD gates | Intent framework | Write-through hook/CI | — |
| Persona-intake stage gates | Cast intake skill | Per-stage DoD assertion | — |
| Signal-stream DoD | Intent framework | Enforced on `status: resolved` transitions | — |

## Compounding fact — three sub-projects, one root

Sub-projects #5 (SIG-034), #6 (SIG-035), and this (#1 foundation, SIG-036) all trace to the **same** discipline root at different altitudes:

| Sub-project | Altitude | Same symptom |
|---|---|---|
| #5 entire.io | Observability substrate | "Enabled" ≠ "Capturing" — no write-through verification |
| #6 Security posture | Data stance | Advisory schema ≠ enforced classifier |
| Cast/Voices (origin) | Product output | Intake pipeline ≠ enforced stage-gates |

All three recur because the framework they depend on has not yet codified write-through as non-negotiable.

## Recommended action

1. **Sub-project #1 Intent rigor audit** (sequenced 4th in the program, not 1st — needs preconditions)
2. **Specific deliverable:** enforcement-map.md at `Core/frameworks/intent/spec/` — each Intent lifecycle stage mapped to its enforcement mechanism (hook / CI / skill-gate / manual), with **advisory-only stages flagged as gaps**
3. **Rule of thumb going forward:** every new Intent primitive (DoR/DoD, DDR, signal DoD, quality baseline, aliasing) requires an enforcement-location declared at creation — no more "add policy, trust the reader"
4. **Until #1 closes:** Cast/Voices should NOT redesign their internal audit — it compounds the pattern. Accept the malformation as a known symptom; fix upstream.

## Follow-up

- Journal entry `Core/products/org-design-tooling/journal/JRN-20260421-intent-framework-rigor-audit-pivot.md` captures the session arc
- Tie-in to `feedback_audit_vs_writethrough.md` — promote this SIG to the canonical architectural example
- Cross-link from Cast and Voices product READMEs (when they exist) to this SIG until #1 resolves
