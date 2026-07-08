---
id: SIG-045
title: Pawel Huryn's Task Delegation CLAUDE.md pattern validates Intent's model mixing architecture with specific routing rules
timestamp: 2026-04-12T23:30:00Z
source: substack-note
author: brien
confidence: 0.85
trust: 0.8
autonomy_level: L3
status: active
cluster: productivity-os-layers
referenced_by:
  - "Pawel Huryn, Substack note on task delegation"
  - "SIG-036: Multi-model adversarial synthesis"
  - "SIG-043: Prompt caching and context formatting"
  - "LLM landscape April 2026"
---

# SIG-045: Pawel's Task Delegation Pattern

## What was noticed

Pawel Huryn shared a CLAUDE.md snippet for task delegation that encodes model routing rules directly in the prompt:

"Spawn subagents to isolate context, parallelize independent work, or offload bulk mechanical tasks. Don't spawn when the parent needs the reasoning, when synthesis requires holding things together, or when spawn overhead dominates."

Model routing:
- Haiku: bulk mechanical work, no judgment
- Sonnet: scoped research, code exploration, in-scope synthesis
- Opus: subtasks needing real planning or tradeoffs

"Parent owns final output and cross-spawn synthesis. User instructions override."

## Why this matters

This is exactly the model mixing architecture Brien has been designing, now encoded as a portable CLAUDE.md block that any practitioner can paste into their setup. Pawel claims it saves 50%+ of tokens in a week.

The pattern validates three Intent architectural decisions:
1. Model mixing is the right approach (not one model for everything)
2. The routing should be context-aware (mechanical vs judgment vs synthesis)
3. The parent-agent owns synthesis — sub-agents are context firewalls (Dex Horthy's insight)

## Connection to Productivity Stack

This lives at L1/Prompt in the Productivity Stack — a CLAUDE.md block that encodes governance rules for agent spawning and model selection. It's the kind of best practice that SIG-043 (prompt caching + structured formatting) identified as needing to be addressed at the L1-L2 foundation layer.

## Action

Consider incorporating this exact pattern (or an adapted version) into Brien's CLAUDE.md files and into the Cowork plugin's default configuration. It's immediately usable and addresses a real cost/quality tradeoff.

## Triage, 2026-07-08

Disposition: still pending, partially converged from a different direction. No literal Haiku/Sonnet/Opus routing block was adopted verbatim into CLAUDE.md as this signal proposed. A related but less formal version exists in persistent memory (feedback_spawn_model_economy.md: chips default to Opus, use Agent with model:sonnet/haiku for audits and mechanical work), which captures the same mechanical-vs-judgment routing principle without the specific portable CLAUDE.md block this signal recommended incorporating.
