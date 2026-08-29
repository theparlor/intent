---
title: Human in the Loop
type: spec
maturity: active
confidentiality: internal
reusability: adaptable
created: 2026-08-29
purpose: States where the human sits in Intent's autonomy architecture, in one page instead of four.
related:
  - spec/autonomy-grant-enforcement.md
  - spec/SPEC-INTENT-FORMATION-GOVERNANCE-001.md
  - .intent/config/approval-rules.yml
  - knowledge/decisions/DDR-009-externally-authored-verification.md
  - spec/autonomy-flight-model-v1-DRAFT.md
  - Core/products/_intake/2026-08-28-knowledge-operating-system/intent-hitl-interaction-2026-08-29.md
---
# Human in the Loop

## Purpose

Until now, the answer to "where does the human sit in Intent's autonomy architecture"
had to be reconstructed from four separate artifacts: `spec/autonomy-grant-enforcement.md`
(the 4-gate check), `spec/SPEC-INTENT-FORMATION-GOVERNANCE-001.md` (the formation
governance matrix), `.intent/config/approval-rules.yml` (the lambda-zero surfaces), and
`knowledge/decisions/DDR-009-externally-authored-verification.md` (why the checker is
not a human). This page is the single statement. The four artifacts stay authoritative
for their own mechanics; nothing here supersedes them.

## The doctrine in brief

The human is the gate, never the checker. Human approval exists at exactly one row of
the formation governance matrix: L0.

L0 is pinned by lambda (the blast-radius throttle that scales a seam's autonomy band up
or down; lambda zero means a cross-human surface that formation never raises), not
drifted into. Every cross-human surface (Slack, email, PR, calendar) is lambda zero,
locked, `no_exceptions: true` in `.intent/config/approval-rules.yml`. Formation cannot
compute its way past this lock; the matrix pins it regardless of measured trust.

Verification intensity rises with autonomy and stays mechanical:

| Band | Verification |
|---|---|
| L1 | Spot-check |
| L2 | Coherence-gate Stage A (a gate check that runs against the Mission Brief at synthesis time) |
| L3 | Stage A plus `audit_chain` |
| L4 | Stage A plus `audit_chain` plus an adversarial Voices panel (a critique instrument that renders multiple personas against the work and preserves disagreement rather than averaging it) |

More autonomy buys more machine checking, never more Brien.

## The three slots the human holds

Per Brien's 2026-08-29 ruling, the human's individual-decision role survives in exactly
three places. Everywhere else, the slot his judgment would occupy is filled by
instruments (see the next section).

1. **The lambda-zero lane.** Per-action approval of cross-human sends: Slack, email,
   PR creation and comment, issue comment, calendar change. TTL expiry (the approval
   window closing without a decision) triggers revalidation, never silent denial: the
   originating skill re-checks whether the action is still needed and re-submits with a
   fresh window.
2. **Meta-governance of the enforcement mechanisms themselves.** Promoting, retiring, or
   ratifying the hooks, matrices, and thresholds is `decision_owner: Brien`. Brien
   adjusts the model and its thresholds, not individual decisions the model produces.
3. **The shadow-audit sample.** Brien samples the loop's output at a rate the evidence
   sets; the sampling rate decays as measured agreement holds. This is the
   shadow-autonomy protocol, `spec/autonomy-flight-model-v1-DRAFT.md` section 9, in
   four steps: the agent operates one autonomy band hotter than its live grant, in
   dry-run; Witness (the event-anchor recorder) logs what the agent would have done;
   that log is diffed against the human-approved decision once it lands; once enough
   runs accumulate, if the agreement rate clears a threshold, the live grant promotes to
   the hotter band.

A fourth surface is a standing escape hatch rather than a slot Brien occupies by default:
the typed-verdict override, a per-verdict override any reviewer can invoke on a specific
ratified atom without touching the mechanism that ratified it.

## What occupies the review slot instead of the human

The ruling names three substitutes. Each maps to instruments that already exist in this
repo.

**Proxy logic** (a deterministic stand-in for the judgment call):
- The 4-gate check (`spec/autonomy-grant-enforcement.md`): reversible, local blast,
  precedent, no info gap. All four pass means execute and signal, never propose.
- The `.intent/config/approval-rules.yml` action-type table.
- The autonomy-grant and closure-discipline hook fabric.
- Coherence-gate Stage A.

**Derivation** (the answer computed from ratified canon instead of asked):
- The precedent gate (gate 3 of the 4-gate check: a prior ruling or explicit grant
  satisfies it).
- Externally authored closure criteria (`criteria_origin: derived`) rather than
  self-graded closure.
- Supersession chains.
- Judge-against-ratified-canon: find the precedence anchor before evaluating anything
  against it.

**Eval** (verification after the fact, feeding Observe):
- `chain_audit` invariants.
- The no-self-graded-closure invariant.
- The DDR-009 independence ladder, I0 through I3.
- Adversarial Voices panels at high lambda.

## Why the checker is not a human

DDR-009 considered and rejected human-only verification of high-lambda work as an
alternative to the independence ladder. Its stated reason: human-only verification
"doesn't scale; defeats the point of an autonomous coherence gate; Brien becomes the
bottleneck the whole system exists to remove." The decision closes with the load-bearing
line: "humans stay the gate via approval, not the checker."

Independence of verification comes from not sharing weights, the I0 to I3 ladder running
from same-model self-check (I0, forbidden as a sole gate) through different-provider,
different-model, blind verification (I3, required at high lambda). It does not come from
human eyes. A verifier earns trust by not sharing the builder's training priors, not by
being a person.

## The graded seal

This is how the doctrine lands on a single decision atom (a typed, ratifiable unit of
captured knowledge):

- **Template refusal without drivers** is mechanical and always on: an atom missing its
  required fields never reaches a status decision at all.
- **A 4-gate pass yields `status: ratified` with no human transaction.** The seal is the
  check plus the signal, not a person's approval.
- **A human seal appears only on a named gate failure**: client-facing, external
  surface, contradicts a stated position, relationship-involving, or financial. The atom
  carries a `gate_failure` field naming why Brien is the gate for that specific atom.
- **Verification then scales with autonomy per the formation ladder, not with human
  reads.** An L4-sealed atom gets `audit_chain` plus an adversarial panel; it does not
  get a human read in place of those checks.

## The two costs the doctrine owns

Stated as owned costs, not hedges.

**1. Derivation-path freshness.** The human used to be the freshness detector: a person
skimming an atom would notice if the canon behind it looked stale. Derivation reads
canon instead of asking a person, and a stale canon chain propagates staleness with no
eyes on it. The owned control: the precedence chain consulted at seal time carries a
staleness check. A derivation from an artifact past its freshness window fails the gate
rather than sealing silently.

**2. The proxy is not yet proven.** DDR-009 is `status: proposed` by its own admission:
"accepted by being run, not by being written." The Voices-panel-as-checker has not yet
earned its record. The bridge is shadow autonomy: atoms seal mechanically now, Brien
spot-audits a sample, and the sampling rate decays as measured agreement holds. The human
does not sit in the loop; he samples the loop's output at a rate the evidence sets.

## The appeal path

When the human disagrees with a mechanically ratified atom, the remedy is never an
in-place edit. Disagreement is a superseding atom filed via the `supersedes` edge, a
first-class ledger event like any other. The ledger keeps both atoms; the disagreement
itself becomes typed knowledge rather than a silent correction.

## Sources

- `spec/autonomy-grant-enforcement.md`: the 4-gate check, execute-and-signal discipline,
  forbidden proposal-framing patterns.
- `spec/SPEC-INTENT-FORMATION-GOVERNANCE-001.md`: the formation governance matrix, the
  L0 lambda pin, the verification-intensity ladder.
- `.intent/config/approval-rules.yml`: the lambda-zero action types, TTL and revalidation
  behavior, `no_exceptions: true`.
- `knowledge/decisions/DDR-009-externally-authored-verification.md`: the independence
  ladder I0 through I3, the rejection of human-only verification.
- `spec/autonomy-flight-model-v1-DRAFT.md` section 9: the shadow-autonomy protocol.
- `Core/products/_intake/2026-08-28-knowledge-operating-system/intent-hitl-interaction-2026-08-29.md`:
  Brien's 2026-08-29 ruling that this page folds in.
