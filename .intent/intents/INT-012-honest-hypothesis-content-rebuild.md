---
id: INT-012
title: "Rebuild site content with hypothesis framing + named attribution + tablestakes/evolutionary distinction"
status: proposed
proposed_by: "brien"
proposed_date: 2026-04-09T05:06:00Z
accepted_date:
signals: [SIG-046, SIG-047, SIG-049]
specs: []
owner: "brien"
priority: next
product: spec
---
# Rebuild site content with hypothesis framing + named attribution + tablestakes/evolutionary distinction

## Problem

The current site presents Intent as a shipped product. The actual state is: 1 of 4 phases operational, discovery N=1, architecture immature, psych safety unaddressed. Presenting this as shipped invites panel verdicts like "rejected", "not production", "blocked" — which is what happened.

Brien's instinct (from 2026-04-09 session conversation): reframe as honest hypothesis, distinguish tablestakes from evolutionary, NAME the methodology heroes while keeping service names genericized. This is a novel synthesis the panels didn't propose but strongly supports.

## Desired Outcome

Site content is rebuilt with three explicit maturity states labeled on every claim:

### Maturity labels (inline on the site)

1. **TABLESTAKES** — solid, proven, baseline expectation. Things we consider non-negotiable hygiene.
   - Examples: "Specs as executable contracts" (TDD, Beck). "Continuous discovery" (Torres). "Story mapping" (Patton). "Outcomes over output" (Seiden). "Observability via OTel" (CNCF).
2. **EVOLUTIONARY** — our current hypothesis, actively testing. Provisional, subject to revision.
   - Examples: "Trust-scored autonomy via weighted signal math." "Panel-review as async feedback primitive." "Four-persona spec-shaping protocol."
3. **OPEN QUESTION** — unresolved, pressure-testing with collaborators. Uncertain.
   - Examples: "Double-loop learning as architected mechanism (not just asserted)." "Federation without leak." "Four-server MCP topology vs. single process."

### Named methodology attribution (novel synthesis from Brien 2026-04-09)

Keep service names abstract (Notice, Spec, Execute, Observe) for portability.
NAME the methodology heroes explicitly:
- Notice → continuous discovery (Torres), OODA observation phase (Boyd)
- Spec → story mapping (Patton), outcomes over outputs (Seiden), specs-as-contracts (Beck)
- Execute → trust-gated agent execution (original research, labeled EVOLUTIONARY)
- Observe → double-loop learning (Argyris), PDCA (Deming), Build-Measure-Learn (Ries)

Lineage page at `/lineage.html` with full attribution graph.

### Hypothesis framing

- Hero copy explicitly: "This is an active research hypothesis. Here's what we believe is solid. Here's what we're still working through. Come pressure-test it with us."
- No claims of "shipped product" or "production ready" where the evidence doesn't support it
- Architecture page: "Here's our current design. Here are the known failure modes. Here's what we're hardening this month."

### Psychological safety contract (SIG-049)

New page at `/safety-contract.html` addressing:
- What trust scores are NOT used for (performance reviews)
- Who sees signals (engagement scoping rules)
- How disagreeing with a spec is protected
- How agent-output accountability is assigned

This page is a prerequisite for any team pilot invitation.

## Evidence

- **SIG-046:** Methodology lineage unacknowledged — 2 panels explicit, confirmed by Brien
- **SIG-047:** Hypothesis framing missing — Brien's instinct confirmed by implicit panel reaction
- **SIG-049:** Psychological safety never addressed — Org Design panel, critical severity

## Constraints

- MUST NOT start until subtraction pass (INT-008) is complete
- MUST NOT split into two sites — one site, progressive disclosure
- MUST credit ancestors with direct names (Torres, Patton, Cagan, Boyd, Deming, Ries, Edmondson, Argyris)
- MUST include the psych safety contract before any team pilot invitation
- MUST NOT present evolutionary/open-question items as tablestakes

## Open Questions

- Visual system for maturity labels — color? icon? sidebar?
- Where does the lineage page live? Under Story? Under Build?
- Does the safety contract get its own primary nav slot, or live under Build?
- How often are maturity labels reviewed and promoted (evolutionary → tablestakes)?

## Dependencies

- Blocked by INT-008 (subtraction pass must complete first)
- Informs INT-010 (discovery interview questions draw from evolutionary/open-question items)
- Related to INT-011 (operator persona captures "what does hypothesis framing sound like in my voice")

## Out of Scope

- Two-site split (rejected — see misalignment analysis)
- New branding (reuse existing slate theme)
- Video content (text first)
