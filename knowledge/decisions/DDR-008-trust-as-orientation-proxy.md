---
title: Trust Scoring as Orientation Quality Proxy with Decay Mechanics
id: DDR-008
type: decision
created: 2026-04-13
updated: 2026-04-13
depth_score: 4
depth_signals:
  file_size_kb: 6.0
  content_chars: 5469
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
status: accepted
confidence: 0.80
origin: agent
persona: PER-001
journey_stage: JRN-001#compile-understanding
sources:
  - raw/research/2026-04-12-chet-richards-boyds-ooda-loop.md
  - knowledge/design-rationale/RAT-003-dual-circuit-architecture.md
related_decisions:
  - DDR-003
  - DDR-007
related_signals:
  - SIG-034
related_themes:
  - THM-002
---
# DDR: Trust Scoring as Orientation Quality Proxy with Decay Mechanics

## Context

Boyd's OODA diagram (Richards 2020) reveals that the Implicit Guidance & Control (IG&C) bypass — Orient directly to Act, skipping Decide — is the dominant operating mode for well-trained organizations. The condition: orientation must be accurate AND shared. Wrong orientation + IG&C = fast, confident, wrong actions.

Intent's trust scoring already gates autonomy levels (L0–L4). But the current trust formula (clarity × 0.30 + inverse blast radius × 0.20 + reversibility × 0.20 + testability × 0.20 + precedent × 0.10) treats trust as a static property of a signal. Boyd's insight is that trust should also reflect the quality of the orientation — the compiled knowledge base that informs the decision.

RAT-003 established the structural mapping. This DDR formalizes two operational consequences.

## Decision

### 1. Trust Score Incorporates Orientation Quality

The trust formula gains an orientation quality modifier that adjusts the base trust score based on the state of the knowledge artifacts the signal touches:

```
effective_trust = base_trust × orientation_modifier
```

Where `orientation_modifier` (0.5–1.2) is computed from:
- **Persona confidence** — are the personas this signal affects validated? (avg confidence of related PER artifacts)
- **DDR coverage** — has the relevant design space been decided? (are there accepted DDRs for this domain?)
- **Source freshness** — are the raw research sources current? (days since last validation of related sources)
- **Contradiction density** — has lint found unresolved contradictions in this domain? (penalizes unresolved conflicts)

A signal in a well-compiled domain (high persona confidence, accepted DDRs, fresh sources, no contradictions) gets an orientation boost. A signal in a domain with stale or contradictory orientation gets a penalty, forcing it through the full Spec cycle even if its intrinsic trust is high.

### 2. Trust Decays with Time Since Validation

Trust is not permanent. The orientation quality modifier decays:
- **0–30 days since validation:** Full modifier (no decay)
- **30–90 days:** Linear decay to 0.8× modifier
- **90+ days:** Capped at 0.7× modifier until re-validated

"Validation" means: a lint pass confirmed the artifact is current, OR the artifact was updated based on new evidence, OR a query consulted the artifact and found it consistent with current observations.

This means a domain that was well-compiled 6 months ago but hasn't been touched will gradually lose its IG&C privilege — signals in that domain will route through full Spec even if they would have been L3/L4 when the domain was fresh.

### 3. The IG&C Threshold

The threshold for bypassing explicit Spec authoring:

| Effective Trust | Autonomy | Boyd Equivalent |
|---|---|---|
| ≥ 0.85 | L4 — full autonomy | IG&C dominant. Act from compiled orientation. |
| 0.60–0.85 | L3 — execute, human monitors | IG&C with verification. Act, then observe. |
| 0.40–0.60 | L2 — decide, human approves | Full Decide node. Draft Spec, Brien approves. |
| 0.20–0.40 | L1 — agent assists | Orient insufficient. Enrich before deciding. |
| < 0.20 | L0 — human drives | No compiled orientation. Strategic ambiguity. |

## Alternatives Considered

1. **Keep trust static per signal.** Rejected — this ignores the compounding value of a well-maintained knowledge base and the decay risk of a stale one. Two identical signals in different domains should route differently based on orientation quality.

2. **Replace trust formula entirely with orientation-based scoring.** Rejected — the intrinsic properties of a signal (clarity, blast radius, reversibility) still matter. A high-blast-radius change in a well-compiled domain is still dangerous. The orientation modifier adjusts the base score, doesn't replace it.

3. **Decay based on calendar time only.** Partially rejected — pure calendar decay doesn't account for domains that are stable and don't need frequent revalidation. Validation-based decay (reset on lint/query/update) is more accurate.

## Consequences

**Positive:**
- Trust scoring now reflects both signal properties AND knowledge base quality
- Stale domains naturally lose autonomy, forcing re-engagement with the knowledge base
- Well-maintained domains earn faster execution — rewarding good knowledge hygiene
- Boyd's theory provides external validation, not just internal convention

**Negative:**
- Computing orientation_modifier requires reading multiple KB artifacts per signal — adds latency to trust scoring
- Decay mechanics need a "last_validated" timestamp on every knowledge artifact (schema addition)
- May create a "cold start" problem for new domains with no KB artifacts (orientation_modifier = ?)

**Mitigations:**
- Cache orientation quality per domain (recompute on lint, not per signal)
- Default orientation_modifier for unknown domains = 0.7 (conservative, forces Spec)
- Add `last_validated` to knowledge artifact frontmatter schema

## Validation Criteria

- [ ] A signal in a domain with high-confidence personas and recent DDRs scores higher effective trust than the same signal in a domain with stale/missing KB artifacts
- [ ] Trust decays measurably after 30 days without validation
- [ ] A lint pass resets the decay clock for artifacts it confirms
- [ ] Cold-start domains default to conservative autonomy levels
