---
id: RAT-002
type: rationale
created: 2026-04-05
updated: 2026-04-13
thought_leaders:
  - josh-seiden
frameworks:
  - Argyris
  - Beer
  - Seiden
  - outcomes-over-output
  - double-loop-learning
depth_score: 4
depth_signals:
  file_size_kb: 4.5
  content_chars: 3523
  entity_count: 6
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.28
related_entities:
  - {pair: josh-seiden ↔ marty-cagan, count: 83, strength: 0.189}
  - {pair: jeff-patton ↔ josh-seiden, count: 75, strength: 0.285}
  - {pair: josh-seiden ↔ teresa-torres, count: 71, strength: 0.185}
  - {pair: jeff-gothelf ↔ josh-seiden, count: 63, strength: 0.364}
  - {pair: josh-seiden ↔ outcomes-over-output, count: 51, strength: 0.315}
name: Double-Loop Learning as the Critical Feedback Path
confidence: 0.85
origin: agent
sources:
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
  - raw/research/2026-04-12-chet-richards-boyds-ooda-loop.md
related_decisions:
  - DDR-003
related_themes:
  - THM-002
---
# Rationale: Double-Loop Learning as the Critical Feedback Path

## Argument

Flow 5 (Observe → Domain Knowledge Base) is the most important data flow in the three-layer architecture. Without it, the system can only do single-loop learning: optimizing how it executes within existing assumptions. With it, the system can question the assumptions themselves — the governing variables that determine what gets built.

Argyris' distinction:
- **Single-loop:** Thermostat detects temperature drift, adjusts heating. Governing variable (target temperature) is never questioned.
- **Double-loop:** System detects that the target temperature itself is wrong — the room is used differently than assumed.

In Intent terms:
- **Single-loop (Flow 6):** Observation says "spec drift detected, update spec status." The domain model is unchanged.
- **Double-loop (Flow 5):** Observation says "users don't behave the way PER-001 predicts. Persona confidence decreases. Journey map JRN-001 flagged for revision. DDR-007 may be invalidated." The domain model itself evolves.

## Framework Application

- **Argyris (Double-Loop Learning):** The risk is "defensive routines" — organizational patterns that suppress disconfirming signals instead of surfacing them. Intent's lint operation is explicitly designed to surface disconfirming evidence, not just confirming evidence.

- **Beer (VSM):** Flow 5 is the 3-4 Homeostat. If System 3 (operations/execution) dominates, the system becomes operationally efficient but strategically blind. If System 4 (intelligence/knowledge base) dominates, plans disconnect from capability. The bidirectional coupling keeps both in balance.

- **Seiden (Outcomes Over Output):** An outcome is a change in human behavior that drives business results. Flow 5 measures behavioral change (did users do what the persona predicted?) and feeds it back into the domain model. This gives the observe phase Seiden's specific meaning — you're observing behavioral change, not system metrics.

## Evidence

- [Three-Layer Architecture](../raw/research/2026-04-05-three-layer-architecture-formalized.md) — "Without double-loop learning, the system can refine how it builds but never question whether it's building the right thing."
- Argyris documented that organizations systematically suppress double-loop learning through defensive routines. Intent's lint operation is designed to counteract this by making disconfirming evidence un-ignorable.
- [Chet Richards — Boyd's OODA Loop](../raw/research/2026-04-12-chet-richards-boyds-ooda-loop.md) — Boyd's actual diagram (Figure 5) embeds a learning loop: Observation → Analyses & Synthesis → Hypothesis → Test → feedback to Orient. Richards: "It is worth pointing out that the bottom loop — the process of observation, analyses/synthesis, hypothesis, and test that creates novelty for strategy to employ — also updates our orientations." This is structurally identical to Flow 5. Boyd validates that the learning loop is not optional but the mechanism by which the system maintains viability.

## Risks

- Double-loop updates to the knowledge base could be disruptive — invalidating a persona or DDR cascades through all linked specs and contracts
- The observe phase must be sophisticated enough to detect domain-level insights, not just system metrics. This is hard.
- Over-triggering Flow 5 (questioning every assumption on every observation) creates churn. Need confidence thresholds for when to trigger knowledge base updates vs. when to treat observations as noise.
