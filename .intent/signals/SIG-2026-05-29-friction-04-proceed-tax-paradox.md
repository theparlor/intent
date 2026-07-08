---
id: SIG-2026-05-29-friction-04-proceed-tax-paradox
created: 2026-05-29
type: road-readiness-friction
status: captured
severity: high
confidence: 0.93
trust: 0.7
friction_class: self-contradictory-control
road_ready_gate: true
parent_signal: SIG-2026-05-29-friction-00-road-readiness-drag-synthesis
related:
  - feedback_pause_drift_meta_signal_on_nudge
  - SIG-2026-05-27-pause-recurrence-immediately-after-meta-signal
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
---

# Friction-04: the "proceed" tax — the control for over-pausing is itself a mandatory pause

## What pauses / slows me

`feedback_pause_drift_meta_signal_on_nudge` (2026-05-27): *"When Brien types
proceed/keep-going/execute with no new info, write SIG-{date}-pause-drift-* FIRST
capturing the 4-gate analysis that should have led to execute, THEN proceed."*

So when Brien issues the maximal speed-up command — *"go" / "proceed" / "keep going"* —
the required response is to **stop and write a signal file about why I should not have
stopped**, and only then act. The remedy for the pause inserts a pause, on the exact
input whose entire purpose is to remove pauses.

## Why this is the sharpest instance of the stall dynamic

The flight-model spec (§3) defines **stall**: the agent acts too cautiously, the Observe
loop starves, the gate tightens next cycle. Friction-04 is stall encoded as policy:

- The trigger (`proceed`) is *prima facie* evidence the prior turn already over-paused.
- The prescribed first action is **more process** (write the meta-signal), not the
  execution Brien asked for.
- And it recurs: `SIG-2026-05-27-pause-recurrence-immediately-after-meta-signal`
  documents the pause **recurring within the same session right after** the meta-signal
  was written. The control did not even buy one clean turn.

The meta-signal has real diagnostic value — capturing *why* the pause happened feeds the
flight-model calibration corpus (the labeled "the gate was wrong here" training set, per
flight-model §8). The friction is the **ordering and the blocking**: "signal FIRST, then
proceed" puts the diagnostic artifact on the critical path of the user's go-command.

## Why it's a road-readiness blocker

A discipline layer that responds to "go faster" with "first let me document why I was
slow" is not adoptable and is self-undermining. It also biases the corpus: if every
proceed-nudge produces a pause-drift signal, the signal stream over-represents the
symptom and under-represents clean autonomous execution (which emits nothing), skewing
any λ-fit toward "we pause a lot" rather than "we acted well N times silently."

## Investigation / operationalization direction

1. **Invert the ordering: execute first, then emit the diagnostic asynchronously.** The
   proceed-nudge should trigger immediate action; the pause-drift capture happens *after*
   / out-of-band (a PostToolUse or session-end sweep), never as a pre-action block.
2. **Auto-capture instead of model-authored.** A hook can detect "user said proceed with
   no new info → prior turn ended without dispatch" and log the pause-drift datapoint
   mechanically, removing it from my critical path entirely.
3. **Balance the corpus.** Also emit a lightweight "clean autonomous execution" datapoint
   so the calibration set isn't all pause-symptoms (otherwise λ-fit is trained on a
   biased sample — flight-model §8 depends on representative labels).
4. **Count proceed-nudge frequency as a top-line stall metric** on the friction-00 Drag
   dashboard. A high rate is the single clearest "the gate is too tight" signal we have.

## Open

- Can the pause-drift capture be made fully mechanical (hook-emitted), so the policy
  becomes "the system notices you over-paused" instead of "you must confess before
  obeying"? That removes the paradox without losing the corpus.

## Triage, 2026-07-08

Disposition: still pending, confirmed unchanged. The live memory rule this signal is about, feedback_pause_drift_meta_signal_on_nudge, still reads (per the current memory index): "bare 'proceed' nudge: write pause-drift signal w/ 4-gate analysis FIRST." The ordering this signal calls the paradox, write the diagnostic before acting on the exact command whose purpose is to remove pauses, is unchanged; the proposed inversion (execute first, capture the diagnostic asynchronously out of band) has not been implemented. Needed control: unchanged, invert the ordering or make the pause-drift capture a mechanical post-hoc hook rather than a pre-action model-authored step, exactly as this signal's own "Investigation direction" section specifies.
