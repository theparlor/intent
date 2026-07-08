---
title: Decision Title
id: DDR-XXX
type: decision
created: YYYY-MM-DD
updated: YYYY-MM-DD
depth_score: 2
depth_signals:
  file_size_kb: 3.7
  content_chars: 3344
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.30
status: proposed | accepted | superseded | validated | invalidated
confidence: 0.00
origin: human | agent | synthetic
persona: PER-NNN
journey_stage: JRN-NNN#stage-name
---
# DDR: Decision Title

## Context

Why this decision is needed now. What forces are at play.
Reference the persona pain points (PER-NNN/PP-NNN) this addresses.

## Decision

What was decided. Be specific and concrete.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Option A | ... | ... | ... |
| Option B | ... | ... | ... |

## Consequences

**Positive:**
- Expected benefit

**Negative:**
- Expected tradeoff or risk

**Neutral:**
- Side effects that are neither good nor bad

## Validation Criteria

How we'll know if this decision was right. Observable, measurable
outcomes that can be checked during the Observe phase.

- [ ] Criterion 1
- [ ] Criterion 2

## Definition of Done (Restructure DDRs)

> Added 2026-05-07 per Brien directive following the 2026-05-07 Forge/Cast write-through panel critique. Open to refinement.

**Required for restructure-class DDRs** — multi-file rename, schema change, directory reorganization, taxonomy shift, or any decision that authorizes changes across N>3 files. Optional for non-restructure decisions (e.g., a single-product policy choice or a standalone constraint).

A restructure DDR is not "accepted" until propagation is verified closed. Per Source-Pattern Principle 8 (`Core/frameworks/coherence-engineering/spec/source-pattern-principles.md`): a restructure event is not complete when file changes ship — it is complete when its propagation manifest is verified closed. Without these four fields, the restructure is not chartered.

### Propagation Owner
Who verifies claim-source alignment post-shipment. Default: DDR author. Named explicitly so the loop is closable.

### Verification Window
How soon after the DDR ships does propagation need to be verified.
- **L4 reversible local:** 24h
- **L2 design change:** 7d
- **L0 strategic / cross-product:** before next dependent DDR

### Acceptance Criterion
The invariant that holds when propagation has succeeded. Machine-readable: a `chain_audit` invariant ID, a grep assertion, a count check, or a structured equivalent. Example: "`chain_audit.py#INV-FORGE-INTAKE-PATH-CANONICAL` reports 0 violations."

### Propagation Manifest
List of files and surfaces touched by the change set. Auto-generated from `git diff --name-only` between pre- and post-restructure commits, then pasted here at DDR-acceptance time. Items may be marked "(landed)" when verified.

---

**Lineage:** Source-Pattern Principle 8 (`Core/frameworks/coherence-engineering/spec/source-pattern-principles.md`); Larsen + Meadows panel critique 2026-05-07; SIG-FORGE-ARCH-OPEN-2026-05-07 Decision 3. Empirical motivation: WS-DDR-026 authorized ~870 file changes 2026-04-18 with zero propagation owner; 19+ days of stale `forge/CONTEXT.md` followed. WS-DDR-070 (Cast↔Forge bounded context) is the first DDR authored against this addendum — the dogfood case. **Independent positive case:** the closure of `SIG-CAST-INTAKE-SYNTHESIS-WRITETHROUGH-GAP` (2026-05-07) populated equivalent closure-DoD fields (upstream control + catch-mechanism + pipeline survival) when remediating an unrelated synthesis write-through gap — same discipline shape applied at signal-closure level by an independent agent without prompting. Empirical validation that the four-field primitive is the natural shape.

## Definition of Done (Tool-Capability Assumptions)

> Added 2026-07-08 per RETRO-2026-06-19-acoe-jira-canon-SIG-2. Open to refinement.

**Required for any decision that turns on a tool or platform can/can't-do claim** — e.g. "system X cannot query Y," "the API has no endpoint for Z," "the UI has no bulk-edit option." Optional for decisions that make no such claim.

A decision is not "accepted" while it rests on an untested tool-capability assumption. Reasoning about what a tool *should* be able to do is not a substitute for testing what it *actually* does — a half-true premise can feel fully verified (a queryable link TYPE mistaken for a non-existent FIELD, where the field genuinely does return zero results, is exactly the kind of confirmation that hides the error). Without these two fields, the capability claim is asserted, not verified.

### Empirical Test
The exact query, command, or action run against the live system, and its literal result — not a description of expected behavior, the actual output.

### Test Date
When the empirical test was run. If the underlying system can change (schema, permissions, config, feature flags), a stale test is not sufficient grounds for re-ratifying a decision that was previously reversed on this claim.

---

**Lineage:** RETRO-2026-06-19-acoe-jira-canon-SIG-2. A ratified canon decision reduced a workflow lane to flag-only on the unverified premise that vanilla Jira JQL cannot query an issue link. A live board contradicted it; a 30-second prod JQL test (`issueLinkType = "is blocked by"`) returned 68 results — a valid native field. The decision was reversed once the claim was actually tested: it had conflated a queryable link TYPE with a non-existent field, and the field alone genuinely did return 0 results, which is what made the wrong premise feel confirmed. The error survived multiple downstream audits and a full canon cascade because every artifact dutifully restated the unverified premise — a full reverse-cascade across ~13 files once the truth surfaced.
