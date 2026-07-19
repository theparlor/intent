---
id: SIG-2026-04-13-approval-gate-ceremony-tax
type: signal
category: architecture-risk
severity: high
source: brien-statement
detected: 2026-04-13
topic: approval-gate-ceremony-tax
related:
  - SPEC-APPROVAL-GATE
  - RETRO-2026-04-12-humanlayer-approval-DEC-1
  - RETRO-2026-04-13-codelayer-pivot-SIG-1
status: promoted
---

# Uniform L0 Gate Reintroduces Ceremony Tax

## Signal

Brien flagged: uniform L0 gating on all external actions reimposes the overhead Intent was designed to eliminate. "I still believe that there are likely to be some signals that self-elevate and that if all go through gates regardless of how they evaluate we are slowing down process again and demanding human in the loop for loops that it is overhead and not full weight."

This is the Agile ceremony tax problem applied to governance. If every Slack message gets the same gate friction as the first email to a new client, the system creates friction proportional to communication volume, not proportional to risk.

## Evidence

- Brien's direct statement (session 2026-04-13)
- CodeLayer's pivot from per-tool-call approval to per-phase gates validates that tool-level gates are too granular
- Intent's own trust model already handles this gradient at the spec level (L0-L4) — the approval gate should use the same pattern at the action level
- Brien communicates daily with the same 3-5 people across 2-3 Slack channels — these are routine, low-risk actions

## Architecture: Contextual Action Trust

Actions within L0 are not binary in risk. Introduce contextual trust scoring per action instance:

### Trust Factors

| Factor | Weight | Measures |
|--------|--------|----------|
| Precedent | 0.35 | Brien approved N similar actions (same target + similar payload) with low modification rate |
| Familiarity | 0.25 | Target is a channel/person Brien communicates with regularly |
| Novelty | 0.20 | Payload divergence from previously approved payloads to this target |
| Blast radius | 0.20 | Audience size, formality, reversibility (thread reply vs. channel broadcast) |

### Three Friction Tiers

| Tier | Contextual Trust | Behavior | Brien's Experience |
|------|-----------------|----------|-------------------|
| **Full gate** | < 0.3 | Block, present, decide | Current SPEC-APPROVAL-GATE: full approval entity lifecycle |
| **Preview** | 0.3 - 0.6 | Show summary, 1-tap confirm | Lightweight: sees it, taps approve, no comment required |
| **Log-only** | ≥ 0.6 | Record and proceed | Brien reviews async; action executes immediately |

### Circuit Breaker

If Brien retroactively flags or modifies a log-only or preview action, trust for that pattern resets to 0. Self-elevation is earned and revocable. This prevents trust from drifting into unsafe territory.

### Learning Loop

Every approval decision (approve, modify, deny) updates the contextual trust model:
- Approve without modification → trust for this pattern increases
- Approve with modification → trust stays flat (system was close but not right)
- Deny → trust for this pattern decreases significantly
- Retroactive flag → trust resets to 0 (circuit breaker)

## Implication

SPEC-APPROVAL-GATE as currently shaped treats all L0 actions uniformly (full gate). This is correct for the initial implementation (safe default), but the spec must include the gradient design as a planned evolution — otherwise the gate will create enough friction that Brien routes around it, defeating the purpose.

## Recommended Action

1. Update SPEC-APPROVAL-GATE to include the three-tier friction model as Phase 2
2. Phase 1 ships with full gate for all L0 actions (safe default, collects training data)
3. Phase 2 introduces contextual trust scoring once enough approval records exist to compute precedent/familiarity/novelty
4. The approval entity already captures the data needed (action_type, action_target, original_payload, approved_payload, modification_detected) — Phase 2 reads from Phase 1's audit trail

## Key Principle

**The gate should create friction proportional to risk, not proportional to communication volume.** This is the same principle that drives Intent's L0-L4 gradient at the spec level — now applied within L0 at the action level.

## Triage, 2026-07-08

Disposition: still pending. This signal's Phase 2 (contextual trust scoring, three friction tiers) presupposes Phase 1 (typed IntentApproval entities, full gate). Phase 1 itself is not built: no `.intent/approvals/` records exist on disk (see the sibling SPEC-SEED triage note, same date). What actually governs L0 today is a SessionStart posture injection plus a Stop-hook lexical check, not the approval-entity audit trail this signal's Phase 2 would read precedent/familiarity/novelty from. Needed control: same as the SPEC-SEED signal (Phase 1 entity + PreToolUse gate) before Phase 2's friction-tier design has anything to compute against.
