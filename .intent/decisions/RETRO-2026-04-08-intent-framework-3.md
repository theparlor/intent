---
decision_id: RETRO-2026-04-08-intent-framework-3
title: Karpathy handoff package ingested into Intent project, not Skills Engine — distinct products sharing architectural DNA
date: 2026-04-05
status: accepted
source: retroactive-extraction
session_date: 2026-04-08
---
# Karpathy Materials → Intent Project (Not Skills Engine)

## Context
A parallel session produced a 4-file handoff package about integrating Karpathy's LLM Knowledge Base architecture with the Intent project. This session needed to ingest the package into Workspaces and use it as architectural input for the skills engine intent framework.

## Decision
Handoff package stored at `Core/frameworks/intent/reference/karpathy-synthesis/` (4 files: handoff context, Karpathy full picture, structural parallels docx, three-layer architecture). The materials belong to the Intent project, not the Skills Engine. The Skills Engine references the patterns (compilation over retrieval, lint, IG&C) but doesn't own the Karpathy research.

## Alternatives Considered
- **Store in Skills Engine** — the session used the patterns, so they could live there. Rejected: the research was about the Intent project specifically, not about consulting skills.
- **Store in Core/reference/concepts/** — as a concept exploration of "LLM knowledge bases." Rejected: the material is project-specific (Intent's three-layer architecture), not a generic concept exploration.
- **Store in Intent project reference (chosen)** — the canonical home for research about the Intent project. Skills Engine references the patterns by attribution, not by owning the source material.

## Consequences
- Skills Engine methodology files cite "Karpathy compilation model" and "Boyd's IG&C" by reference, not by inlining the source research
- The Intent project has a new reference/ directory with rich architectural context for future development
- If the patterns need to be formalized as reusable methodology, they'd move to Core/frameworks/ not Core/products/skills-engine/
