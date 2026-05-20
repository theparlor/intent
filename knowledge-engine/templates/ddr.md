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
