---
id: THM-004
type: theme
created: 2026-04-13
updated: 2026-04-13
depth_score: 2
depth_signals:
  file_size_kb: 3.8
  content_chars: 3520
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
name: Spec-Governed Execution — Intent's Position in the SDD Landscape
confidence: 0.80
origin: agent
sources:
  - raw/research/2026-04-12-fowler-sdd-tools-survey.md
  - raw/research/2026-04-12-rvk7895-llm-knowledge-bases.md
related_personas:
  - PER-001
related_decisions:
  - DDR-002
signals:
  - SIG-032
---
# Theme: Spec-Governed Execution — Intent's Position in the SDD Landscape

## Insight

Böckeler (Thoughtworks, 2025) identifies three levels of Spec-Driven Development: **spec-first** (spec written before coding), **spec-anchored** (spec kept alive for ongoing evolution), and **spec-as-source** (humans never touch code, only specs). She warns that spec-as-source risks combining MDD's inflexibility with LLM non-determinism — "Verschlimmbesserung."

Intent occupies a fourth position: **spec-governed execution**. Specs are not just generation prompts (spec-first), not just persistent documentation (spec-anchored), and not the only editable artifact (spec-as-source). They are **contracts that agents execute against, verified through trust gates and the observe phase.**

This distinction matters because:
- Spec-first tools (Kiro) turn small bugs into 4 user stories with 16 acceptance criteria
- Spec-anchored tools (spec-kit) create verbose multi-file topologies reviewers won't read
- Spec-as-source tools (Tessl) produce non-deterministic code from deterministic specs

Intent's trust scoring adapts the workflow to problem complexity — not every signal needs a full spec. The observe phase detects and corrects non-deterministic agent behavior over time. The spec is an executable assertion, not a generation prompt.

## Evidence

- Böckeler (2025): "I'd rather review code than all these markdown files." Spec-kit's review burden was counterproductive.
- Böckeler (2025): Kiro turned a small bug fix into 4 user stories, 16 acceptance criteria — problem size mismatch.
- Böckeler (2025): "small work packages almost seem counter to the idea of SDD" — iteration incompatibility with up-front design.
- Tessl: same spec produces different code on successive runs. Non-determinism is the key tension.
- rvk7895: implements auto-evolve after query — the knowledge base enriches itself through use, not just through explicit ingestion. This is the observe-loop applied to compilation.

## The MDD Warning

Böckeler's most structural insight: the closest historical parallel for SDD is **Model-Driven Development**, not BDD/TDD. MDD failed because it sat at an "awkward abstraction level" with "too much overhead." LLMs remove MDD's constraints (no parseable spec language needed, no code generators to build) but add non-determinism (MDD didn't have this).

Intent's answer to the MDD trap:
- Spec-as-contract + trust gates = executable assertion, not generation prompt
- Observe phase detects when the same spec produces divergent outcomes
- Trust scoring decays confidence when non-determinism is detected
- The spec is not the only artifact — the knowledge base provides the orientation that resolves ambiguity

## Implications

- Intent should explicitly position against the three SDD levels in external communication
- The "memory bank / spec separation" all three tools struggle with is already solved in Intent: context docs (project-level, persistent) vs. specs (execution-level, task-scoped)
- The review burden problem is real and Intent must not replicate it — trust scoring that scales spec depth to signal complexity is the mechanism

## Open Questions

- What is the minimum viable spec for L3/L4 trust signals? Can it be lighter than Kiro's 3-doc model?
- How does spec-governed execution interact with the IG&C bypass (RAT-003)? High-trust situations may not need specs at all.
- Should Intent expose a "spec complexity budget" analogous to how rvk7895 uses model tiers for different operations?
