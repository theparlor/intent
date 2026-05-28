---
signal_id: RETRO-2026-04-08-intent-framework-SIG-1
title: Subaru has the thinnest knowledge graph despite being Brien's primary engagement
severity: high
detected: 2026-04-05
status: resolved
resolved_date: 2026-05-28
source: retroactive-extraction
trust_score: 0.71
autonomy: L3
upstream_control_path: Work/Consulting/Engagements/Subaru/knowledge/ — 9 stakeholder profiles + company dossier + personas/journeys/themes/decisions/design-rationale directories fully built
catch_mechanism: library-index artifact registry + overwatch Section 2 freshness scan
pipeline_survival: yes — canonical on-disk knowledge/ structure
---
# Subaru Has the Thinnest Knowledge Graph Despite Being Primary

## Observation
First artifact registry scan revealed: Subaru (Brien's primary engagement, 18-week, on-site 3 days/week) has 1 stale dossier (28d old), zero stakeholder profiles, zero industry scans, and zero competitive landscapes. F&G (pitch stage, less active) has 11 artifacts. The engagement Brien spends the most time in has the least compiled intelligence.

## Context
Discovered during first lint pass of the artifact registry built in this session. Registry scanned all 4 active engagements. Subaru has 7 total files but only 1 qualifies as a research artifact (the company dossier). Named stakeholders exist in the artifacts (Greg Giuffrida, Gino, Dan Compas, Brendan Greer, Natalie Miller) but none have been profiled.

## Implication
- Brien operates on direct knowledge at Subaru (he's there 3 days/week) so never felt the need to compile. But compiled intelligence compounds in ways direct knowledge doesn't.
- This is the highest-value target for the first orchestrated skill chain execution: individual-research profiles for named Subaru stakeholders would immediately prove the pipeline on Brien's most valuable engagement.
- The contrast (primary engagement = thinnest graph) is structurally inevitable when research is demand-driven rather than proactive. The signal scoring model + lint operation are designed to prevent exactly this gap.

---

## Triage note — 2026-05-28 (superseded by completed work)

**Status:** the original gap no longer exists, but this signal was never formally closed. Subaru's knowledge graph has been substantially built: `Work/Consulting/Engagements/Subaru/knowledge/` contains personas, dossiers, journeys, themes, decisions, domain-models, and design-rationale directories. `people/` contains 9 profiled stakeholders including Giuffrida, Guarnere, Miller, Goldshteyn, McCracken, and others. The "1 stale dossier, zero stakeholder profiles" state from 2026-04-05 is fully resolved. This signal can be closed as resolved.

**upstream_control_path:** `Work/Consulting/Engagements/Subaru/knowledge/` — built-out knowledge graph with stakeholder profiles
**catch_mechanism:** library-index + overwatch Section 2 artifact registry scanning
**pipeline_survival:** yes — knowledge/ is canonical on-disk
