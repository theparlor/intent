---
id: SIG-053
timestamp: 2026-04-09T06:00:00Z
source: conversation
confidence: 0.95
trust: 0.9
autonomy_level: L4
status: captured
cluster: methodology-gaps
author: brien
related_intents: [INT-012, INT-013]
referenced_by: [DEC-20260409-02]
parent_signal: SIG-049
---
# Measurability + visibility are infrastructure prerequisites for adopting Intent

Brien's explicit position during 2026-04-09 session, answering open question 5 on trust scores:

> "we should explicitly pursue blue green environments and feature flag change management so that the code can advance but humans are still required to accept the result of a potential multitude of impactful changes. we will also need significant automated testing and change reporting. if your development and your product isn't measurable and the measures visible it shouldn't be using our approach. it lacks the ability to generate and rely on valid signals."

## The load-bearing principle

**If your development and your product isn't measurable, and the measures aren't visible, it shouldn't be using our approach. It lacks the ability to generate and rely on valid signals.**

This is a new first-class criterion for when Intent can and cannot be adopted safely. Until now, Intent's adoption story has implicitly assumed teams have modern engineering infrastructure. This signal makes that assumption explicit and operational.

## The four prerequisite infrastructure capabilities

1. **Blue-green deployment or equivalent reversibility infrastructure** — the code can advance but the result must be accepted by humans before rollout. Without this, the "reversibility" factor in the trust formula is fictional.

2. **Feature flag change management** — impactful changes are gated behind flags that humans control. Intent's L3/L4 autonomy brackets assume the ability to ship code that is still "off" until a human turns it on.

3. **Significant automated testing** — signals about outcomes depend on tests that actually run and report. Without automated testing, contract.assertion.passed/failed events are either manually authored (slow, biased) or absent (silent failure).

4. **Change reporting that is visible** — the measures must be visible, not hidden in dashboards nobody checks. Forsgren's DORA research is clear: measurement without visibility is cargo cult measurement.

## Why this matters for trust scoring

Brien's stated purpose for trust scores: "consider the current maturity of our agents and identify the risk of tasks we face and use those to calibrate our trust for decision making without interruptive human in the loop."

His stated measure: "knowing a reversible decision was made and can be reviewed later."

The trust formula (clarity + 1/blast_radius + reversibility + testability + precedent) is doing the right math — but the math is only meaningful if the infrastructure supports the values. Specifically:

- **`reversibility` is fictional** if the deployment environment doesn't actually support rollback
- **`testability` is fictional** if automated tests don't exist
- **`blast_radius` is unknowable** if change impact isn't measurable
- **`precedent` is unknowable** if past outcomes aren't visible

So: trust scores without this infrastructure are **calibrated on assumptions the environment cannot honor**. The L3/L4 autonomy brackets become unsafe not because the math is wrong, but because the real world doesn't match the math.

## The "when NOT to adopt" consequence

This signal generates a new first-class content obligation: Intent's site needs an explicit "cultures and infrastructures where you should not adopt Intent" section. This is a Dunford-style positioning move — naming who you're not for is category clarity. It also satisfies Rumelt's "strategy is choosing what not to do."

Candidate exclusions:
- Teams without reliable automated testing
- Environments without deploy rollback capability
- Orgs where change reporting is hidden or unreliable
- Cultures where measurement is politically contested (see: Goodhart's Law risk)
- Teams where the measures exist but aren't treated as valid signals (e.g., vanity dashboards nobody reads)

## The connection to psych safety (SIG-049)

This signal is a child of SIG-049 (psychological safety never addressed). The connection:

- Promise 4 of the Safety Contract distinguishes failure types (basic, complex, intelligent)
- But distinguishing failure types requires knowing what happened
- Knowing what happened requires measurability + visibility
- Therefore: the Safety Contract cannot be honored without the infrastructure prerequisites

Psychological safety and measurability are technically distinct but operationally co-dependent. A team cannot run intelligent failures safely if they can't see the failure. A team cannot celebrate the right kind of wrong if the wrong is invisible.

## Trust Factors

- Clarity: 0.95 (Brien's explicit statement, specific mechanisms named)
- Blast radius: 0.7 (affects who can adopt Intent — significant)
- Reversibility: 0.8 (can be revised if we learn more)
- Testability: 0.85 (the infrastructure prerequisites are observable)
- Precedent: 0.95 (DORA research, continuous delivery literature, Accelerate)

## Required actions

1. Add Promise 10 to the Psychological Safety Contract: "Infrastructure prerequisites for safe trust-scored autonomy"
2. Add a "when NOT to adopt Intent" section to the rebuilt site content (INT-012)
3. Add infrastructure readiness questions to the discovery interview protocol
4. Add a cultural/infrastructure readiness checklist to any future pilot engagement intake

## Lineage

- **Jez Humble + Dave Farley** — *Continuous Delivery* (2010) — blue-green, feature flags, deployment pipelines
- **Nicole Forsgren, Jez Humble, Gene Kim** — *Accelerate* (2018) — DORA metrics, measurability as prerequisite for improvement
- **Martin Fowler** — feature toggles pattern
- **Brien's own instinct** — "measurable and visible or don't use Intent"
- **Amy Edmondson** — Right Kind of Wrong (2023) — failure classification requires visibility
