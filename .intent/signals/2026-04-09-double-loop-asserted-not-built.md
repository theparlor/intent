---
id: SIG-050
timestamp: 2026-04-09T04:48:00Z
source: agent-trace
confidence: 0.85
trust: 0.8
autonomy_level: L3
status: captured
cluster: methodology-gaps
author: panel-review-2026-04-09
related_intents: []
referenced_by: []
parent_signal:
---
# Double-loop learning is asserted in decisions but not architected in the tool surface

Three panels (ARB, Strategy, Org Design) independently flagged that D17 cites Argyris and declares "Observe updates Layer 1 (domain understanding), not just Layer 3" — but the only mechanism shown is spec-delta detection and signal suggestion. That's single-loop (observed vs. expected), not double-loop (questioning the governing variables).

Direct quote from Org Design panel (Argyris voice): *"Label one persona pass 'Challenge the Intent' and you have real double-loop learning. Right now it's single-loop dressed in double-loop language."*

## The latent mechanism already exists

The 178-persona voice library is the perfect double-loop mechanism — different personas surface contradictory mental models that could expose governing variable errors. But the site frames them as execution helpers, not premise-challengers. This is the single biggest missed opportunity in the methodology.

## Required outcome

- Add a new spec-shaping protocol pass: "Challenge the Intent" (Pass 0, before △ ◇ ○ ◉)
- Pick one persona class (e.g., Rumelt, Christensen, Mintzberg) to explicitly ask "should we even want this outcome?"
- This pass has the power to REJECT an intent, not just refine it
- Integrates with panel-as-a-service primitive (SIG-041) — a rejection triggers a deeper panel review
- Converts the double-loop claim from metaphor to mechanism

## Relationship to Panel primitive (SIG-041)

The "Challenge the Intent" pass is actually a specialized instance of the panel-as-a-service primitive. Rather than having 4 personas review a spec, one rotating challenger reviews the intent itself. This is the same mechanism applied at a different ontological level (intent vs spec).

## Trust Factors

- Clarity: 0.85 (3 panels converged, Argyris theory is specific)
- Blast radius: 0.4 (changes spec-shaping protocol, moderate)
- Reversibility: 0.8 (can remove the pass)
- Testability: 0.6 (hard to measure "did this actually question assumptions")
- Precedent: 0.9 (Argyris double-loop learning, 1978)
