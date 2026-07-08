---
signal_id: RETRO-2026-04-08-intent-framework-SIG-5
title: BUILD intent type missing from taxonomy — Brien's most common session type has no operational definition
severity: low
detected: 2026-04-05
status: open
source: retroactive-extraction
trust_score: 0.35
autonomy: L1
---
# BUILD Intent Type Missing from Taxonomy

## Observation
The intent taxonomy defines 8 primary types (PREPARE, RESEARCH, COACH, DELIVER, EVALUATE, POSITION, EXPLORE, SCAN) plus 3 meta types (BUILD, IMPROVE, REFLECT). Meta types are described as "about the system itself" but don't have named compositions in the skill graph. This entire session was a BUILD — and the orchestrator has no composition for it.

## Context
Noted in the journal entry as system learning. BUILD is Brien's most common session type (he builds skills, methodology, frameworks regularly).

## Implication
- A BUILD composition could wire: read existing architecture, identify gaps, build atomic pieces, register in skill graph, update CLAUDE.md
- Low priority because BUILD sessions are inherently unstructured (can't pre-compile a chain for creative work)
- But BUILD could benefit from a post-execution checklist: register new skills, update inventory counts, run register-skill.sh, update CLAUDE.md

## Triage note, 2026-07-08

Disposition: still pending. Checked Core/frameworks/methodology-library/meta/skill-graph.md directly: no BUILD composition is wired there. The global CLAUDE.md's Behavioral Rules do carry a version of the post-execution checklist this signal asked for ("Run register-skill.sh when you create skills. Run generate-claude-md.sh when structure changes."), so the low-priority checklist half is honored as a standing instruction rather than an orchestrator composition. The named gap, BUILD has no composition in the skill graph itself, is unchanged. Needed control: either wire a BUILD composition into skill-graph.md matching the read-identify-build-register-update chain this signal proposed, or explicitly accept the standing-instruction version as sufficient given severity was already scored low.
