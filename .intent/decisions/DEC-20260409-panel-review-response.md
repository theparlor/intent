---
id: DEC-20260409-01
title: "Response to multi-panel review: subtract before build, keep one site, panels become first-class primitive"
date: 2026-04-09
status: decided
superseded_by:
supersedes:
related_signals: [SIG-041, SIG-042, SIG-043, SIG-044, SIG-045, SIG-046, SIG-047, SIG-048, SIG-049, SIG-050, SIG-051, SIG-052]
related_intents: [INT-007, INT-008, INT-009, INT-010, INT-011, INT-012]
author: brien
---
# DEC-20260409-01: Response to multi-panel review

## Context

On 2026-04-09, an 8-panel persona-dispatch review of the intent-site returned 48 voices of structured critique. The review surfaced 10 cross-cutting findings (F1–F10), ranging from positioning failures to architectural gaps to an unaddressed psychological safety concern.

Brien's initial reaction proposed:
1. Split the site into two properties (concept site + technical pressure-test site)
2. Archive current content and "build new material in as many repos as needed"
3. Re-introduce named attribution while keeping genericized service names
4. Reframe Intent as active hypothesis rather than shipped product
5. Distinguish tablestakes from evolutionary
6. Build team/operator personas starting with a brien-operator self-persona

The panels (implicit recommendation) and Brien (explicit instinct) had areas of agreement and disagreement that needed to be explicitly resolved before proceeding.

## Decision

### Accepted from Brien's instincts

1. **Reframe as honest hypothesis with tablestakes/evolutionary/open-question labels.** This is a novel synthesis the panels couldn't propose (they assumed shipped-product framing). Accepted. Implemented via INT-012.

2. **Re-introduce named methodology attribution while keeping generic service names.** Neither panel proposed this combination, but it correctly splits shareability (generic services) from credibility (named heroes). Accepted. Implemented via INT-012 + new lineage.html.

3. **Build team/operator persona type, starting with brien-operator.** Novel gap in the persona system. Accepted. Implemented via INT-011.

4. **Archive current site content.** Accepted as part of the subtraction pass, not as prelude to new build-out. Implemented via INT-008.

### Rejected from Brien's instincts

1. **Two-site split (concept site + technical pressure-test site) is REJECTED.** The panels' #1 and #3 findings were "no target user" and "six category framings." Splitting into two sites compounds these problems, not solves them. Two audiences served badly is worse than one audience served well. The correct move is ONE site with layered progressive disclosure.

2. **"Build new material in as many repos as needed" is REJECTED (for now).** The panels prescribed subtraction and sharpening, not addition. Brien's reflex was to build more; the correct first move is to delete first. This became SIG-052 as a recognized failure pattern, and the operator persona (INT-011) explicitly captures this reflex with a corrective prompt.

### Added from panel findings that Brien missed

1. **Run 10 external discovery interviews (INT-010).** Brien's response addressed content strategy and architecture, but 4 panels independently flagged the N=1 external evidence problem. No amount of better content compensates for zero external signals. This is the highest-leverage individual move per Torres/Cagan/Blank/Fitzpatrick unanimous recommendation.

2. **Psychological safety contract (SIG-049 → INT-012).** Brien did not mention psych safety in his response. The Org Design panel (Edmondson voice) flagged this as the biggest latent failure mode. Trust scoring is literally a performance-evaluation shadow system; signals with attribution become dossiers in low-trust orgs. This is a methodology fix, not a content fix. Prerequisite for any team pilot.

### Novel discovery from the exercise itself

**Panel-as-async-feedback-loop is the genuine breakthrough** (SIG-041 → INT-007). None of the 8 panels caught this — they were busy being the panel. Brien noticed it in the synthesis. Agents can now call structured panel review after any cycle and get fast, clean, structured feedback asynchronously. This may be the most valuable shipping artifact hiding inside Intent, and it is being productized as a first-class skill in `Core/products/skills-engine/skills/claude-code/meta/panel-review/`.

## Alternatives Considered

### Alt 1: Accept Brien's two-site split
**Rejected because:** It compounds the category confusion problem (F3) and the no-target-user problem (F1). The panels were explicit that subtraction, not addition, was the correct move.

### Alt 2: Build out all 6 intents in parallel immediately
**Rejected because:** INT-008 (subtraction) must gate INT-012 (new content rebuild). Building new content before the old is removed compounds surface area. The sequence matters.

### Alt 3: Ignore the psych safety finding (1/8 panels)
**Rejected because:** Low agreement count but high severity. Edmondson's research is unambiguous on the failure mode. Ignoring a critical finding because only one panel caught it would undermine the entire panel-review approach — the value is in catching what individual panels miss, including findings owned by only one panel.

### Alt 4: Ship the panel-review primitive as a one-off script
**Rejected because:** The primitive is too valuable for one-off use. It becomes a first-class skill with structured input/output so agents can call it during any cycle. This is the difference between a helper and a product.

## Consequences

### Positive

- Execution sequence is clear: subtract → discover → rebuild → harden, not simultaneous chaos
- Panel-review becomes a reusable primitive available in every future cycle
- Content strategy has honest framing that matches actual maturity state
- Engineering backlog has panel-validated priorities
- Operator persona closes a real gap in the persona system

### Negative

- Brien's instinct to "build more" is explicitly overridden, which may feel like friction
- Discovery interviews are a 2-week delay before rebuilding content
- Psychological safety contract adds methodology work that wasn't originally planned
- The two-site option remains on the table if progressive disclosure doesn't work — not killed, just deferred

### Risks

- The "one-site progressive disclosure" approach may itself fail the Dunford category test if not executed carefully. Mitigation: panel-review the rebuilt site before launch.
- Discovery interviews may reveal the target user is different from the assumed "practitioner-architect," forcing a larger pivot. This is a FEATURE, not a bug — better to find out in week 2 than week 20.
- The operator persona type may proliferate (every user wants one) before v1 proves the pattern. Mitigation: brien-operator only until the primitive is validated.

## Validation Criteria

Decision is validated if:
1. Subtraction pass completes within 1 week (INT-008)
2. 10 external discovery interviews complete within 2 weeks (INT-010)
3. Panel-review primitive ships as a callable skill within 1 week (INT-007)
4. Architecture P0 items complete within 1 week (INT-009)
5. Re-run the panel review on the rebuilt site and measure: did agreement on F1 (no target user) drop? did F3 (category confusion) drop? did F10 (psych safety) get addressed?

If validation criteria fail, reconvene the panel and decide what's wrong with the decision itself (double-loop).

## Implementation

See:
- INT-007 (Panel-review primitive)
- INT-008 (Subtraction pass)
- INT-009 (Architecture hardening)
- INT-010 (External discovery interviews)
- INT-011 (Operator persona)
- INT-012 (Content rebuild with hypothesis framing)
