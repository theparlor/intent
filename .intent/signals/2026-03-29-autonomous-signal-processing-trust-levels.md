---
id: SIG-001
timestamp: 2026-03-29T07:00:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.85
autonomy_level: L2
status: active
cluster: autonomous-infrastructure
parent_signal:
related_intents: []
---
# Signal: Autonomous signal processing needs five trust levels (L0-L4)

## Observation

Signals range from "noisy idea" (L0, human review required) to "actionable intelligence" (L3-L4, autonomous execution ok). A five-level framework emerged:

- **L0**: Captured, needs human review (trust < 0.3)
- **L1**: Reviewed, pattern confirmed (trust 0.3-0.5)
- **L2**: Elevated, high-confidence signal (trust 0.5-0.7)
- **L3**: Autonomous action triggered (trust 0.7-0.9)
- **L4**: System behavior modified (trust > 0.9)

Each level has different actions: L0 → alert, L1 → dashboard, L2 → conditional action, L3 → auto-execute with logging, L4 → system reconfiguration.

## Why It Matters

Without levels, either all signals are ignored or all are acted on. This creates false negatives (missed problems) or alert fatigue (acted on noise). The five levels let the system *calibrate* trust: start conservative, observe outcomes, increase autonomy as confidence grows.

## Trust Factors

- Clarity: Very High — the framework is testable
- Blast radius: Very High — defines all downstream automation boundaries
- Reversibility: High — can adjust thresholds without rewiring systems
- Testability: Very High — each level has measurable criteria
- Precedent: Very High — five-level taxonomies are standard (severity, risk, confidence, etc.)
