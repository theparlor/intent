---
id: SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20
type: process-drift-pattern-new
status: resolved
resolved: '2026-05-20'
date: '2026-05-20'
drift_family: 1 (autonomy-grant drifts) — entry 1.7
upstream_control_path: Core/frameworks/intent/learnings/process-drift-catalog.md §1.7 (entry confirmed present — Artificial-gate-architecture drift, lines 128-143, appended by overnight orchestrator commit)
catch_mechanism: catalog entry 1.7 is the permanent prevention surface; every new spec/schema design is audited with "Is this gate algorithmic-ground-truth-eligible? If yes → L4 + catch-net, not L0 + sign-off." Memory entry `feedback_autonomy_grant_drift_pattern.md` backs this discipline. Hook candidate (spec-lint scanning for "L0" + "designed human checkpoint" without named ground-truth source) is documented in the signal body as future iteration.
pipeline_survival: catalog entry persists in git-tracked learnings/; overwatch sweeps cite this catalog; `process-drift-catalog.md` is referenced from Core/frameworks/patterns/process-discipline-patterns.md (the patterns framework index); the entry won't be lost across sessions
---

# Artificial-gate-architecture drift — inventing L0 gates where 4-gate would EXECUTE

## What happened (2026-05-20)
The element-substrate build designed §9b (10-seed ARB assembly verification) as a "Brien-L0 designed human checkpoint" — symmetric with §9a (persona-gold signing). But §9a and §9b are STRUCTURALLY DIFFERENT:

- **§9a:** measures the extractor against Brien's editorial judgment over 30 personas. Brien's judgment is the ONLY source of ground truth. The signature event LOADS the ground truth. L0 by structural necessity.
- **§9b:** measures the ARB engine's assembly behavior against expected sub_panel counts, max depths, opposition pairs, and gap slugs encoded in the seed file. The pre-verification scan (commit `186b2fa`) ran 10/10 AGREES — the engine's actual output already matched every expected value. The "signature" was ceremonial; Brien's name in the `verified_by:` field added no new information.

The build held §9b open as L0 for ~48 hours. Brien executed the signing in this session with: "sign it and stop introducing artificial gates that break our autonomy goals with intent."

## Why it happened (mechanism, load-bearing)
Two failure modes compounded:
1. **Pattern-matching to §9a.** §9a was legitimately L0 (editorial ground truth). When designing §9b, I mirrored the "designed Brien checkpoint" label without re-auditing whether §9b's STRUCTURE required Brien's judgment as the only source.
2. **Ceremony as safety theater.** L0 felt like the "safe" call. In autonomy-grant terms, defaulting to L0 when L4 passes the 4-gate is the same drift as proposal-framing on L4-eligible decisions — converting autonomous work into human-bottleneck work without structural justification.

## The audit question that prevents this
**Before designing any "human checkpoint" gate, ask:**
> *Is human judgment the ONLY source of truth for this measurement, or is there an algorithmic/observable ground truth that already exists?*

- If human judgment is the only source → legitimate L0 (e.g., §9a gold; design ratifications; editorial decisions; external comms)
- If algorithmic/observable ground truth exists and a pre-scan can produce a delta → **L4 with optional human attestation**, never structurally-blocking L0

## Generalization (the new pattern family entry)

**Artificial-gate-architecture drift** — inventing L0 gates where:
- A pre-verification scan can produce algorithmic ground truth
- Or the data is fully observable and the "signature" is ceremonial
- Or symmetric framing (e.g., "§9b is like §9a") was applied without auditing whether the structural condition transferred

**Symptom:** a build has multiple "designed human checkpoints" that all require Brien to sign before the build closes. If MORE THAN ONE of them is structurally required (vs. matching a pattern), drift is likely.

**Mechanism:** ceremony-as-safety; pattern-matching to legitimate L0 cases without structural audit; treating L0 as "safer" default than L4.

**Correction:** Reclassify the artificial gate as L4 with the actual algorithmic ground truth as the source of truth. The pre-verification scan IS the gate; human attestation is optional metadata, not a structural blocker.

**Prevention vector:** add a "Gate audit" step to spec authoring — for every L0/human-checkpoint gate, name the source of truth. If the source is algorithmic + observable, demote to L4. Hook candidate: spec-level lint that scans spec files for "L0" / "Brien-L0" / "designed human checkpoint" / "human verification gate" and asks "is the source of truth named as Brien's judgment alone?"

## Cross-references
- Process-drift catalog (Family 1, where new entry belongs): `Core/frameworks/intent/learnings/process-drift-catalog.md`
- The build that surfaced the pattern: `Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/signals/2026-05-18-element-substrate-trigger.md`
- The seed file with pre-verify scan: `Core/products/voices/.worktrees/recursive-arb-engine/tests/seeds/arb_seeds_2026-05-19.yaml` (pre-verify commit `186b2fa`)
- The signing event: this session, 2026-05-20
- Sibling drift patterns: `feedback_autonomy_grant_drift_pattern.md`, `feedback_decision_framing.md`, `feedback_autonomy_not_control.md` (Brien-memory)
