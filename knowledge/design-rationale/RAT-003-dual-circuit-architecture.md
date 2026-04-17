---
id: RAT-003
type: rationale
created: 2026-04-13
updated: 2026-04-13
frameworks:
  - Boyd
  - Beer
  - Argyris
depth_score: 4
depth_signals:
  file_size_kb: 5.0
  content_chars: 4673
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.21
related_entities:
  - {pair: Boyd ↔ Beer, count: 2, strength: 0.667}
  - {pair: Beer ↔ Argyris, count: 2, strength: 0.667}
name: Boyd's Dual-Circuit Model as Theoretical Grounding for Two-Speed Architecture
confidence: 0.90
origin: agent
sources:
  - raw/research/2026-04-12-chet-richards-boyds-ooda-loop.md
  - raw/research/2026-04-12-rotifer-compile-dont-search-agent-memory.md
related_decisions:
  - DDR-003
related_themes:
  - THM-001
  - THM-002
---
# Rationale: Boyd's Dual-Circuit Model as Theoretical Grounding for Two-Speed Architecture

## Argument

Intent's architecture operates at two speeds simultaneously. Chet Richards' peer-reviewed analysis of Boyd's actual OODA diagram (Necesse 2020) reveals that this is not an implementation choice but a structural requirement of any viable adaptive system.

Boyd's full diagram (Figure 6 in Richards) contains **two simultaneously active circuits:**

1. **Fast IG&C path** (Orient → Act): Executing current repertoire. Compiled orientation triggers action directly, bypassing explicit decision. This is the dominant mode for well-trained organizations.

2. **Learning loop** (Observe → Analyses & Synthesis → Hypothesis → Test → feedback to Orient): Generating new repertoire and updating orientation. Essentially Deming's PDCA embedded within OODA.

"Both are active, although the emphasis is on one or the other." Active engagement → IG&C emphasis. Between engagements → learning loop emphasis.

## Mapping to Intent

| Boyd's Circuit | Intent Implementation | When Dominant |
|---|---|---|
| Fast IG&C (Orient → Act) | Skill chain orchestrator executing known patterns via compiled context (INTENT.md, decision log, prior specs) | Active execution — trust ≥ L3, established repertoire |
| Learning loop (Observe → Orient) | Signal-detector, journal, lint, overwatch — discovering new patterns, questioning assumptions | Between executions — new signals, low-trust situations, post-observe reflection |

**The IG&C bypass is the key insight.** Boyd explicitly labeled the path from Orient directly to Act, skipping Decide entirely. In Intent terms: when the knowledge base has sufficient compiled orientation (persona confidence high, DDR established, journey validated), the system can move from Notice directly to Execute without full Spec authoring. The trust score is what determines whether the bypass is safe.

**The condition Boyd identified:** IG&C only works when orientation is accurate AND shared. Wrong orientation + IG&C = fast, confident, wrong actions. This maps directly to Intent's trust gates — the trust score is the proxy for orientation quality. Low trust forces explicit Spec (the Decide node). High trust enables the bypass.

## Incestuous Amplification as Governance Failure Mode

Boyd identified that the IG&C feedback from Orient back to Observe creates a dangerous self-reinforcing loop: orientation filters observation to confirm itself. Richards: "Strategists call this 'incestuous amplification' — a self-reinforcing loop that becomes increasingly disconnected from reality."

In Intent terms: if the knowledge base only surfaces signals that confirm existing personas, DDRs, and themes, the system stops noticing gaps. **Overwatch and consistency-audit are the external reference points Boyd prescribes** — they break the confirmation loop by asking "what are we NOT seeing?"

Boyd's prescription: "even attempting to assess your organization's status from inside will increase the confusion and disorder within it. You need outside reference points."

## Behindigkeit — The Meta-Capability

Late in life, Boyd added **Behindigkeit** — the ability to break out of deeply held patterns. Not just operating within doctrine but knowing when to abandon it. This is the meta-capability overwatch should surface: not just "are we drifting from our patterns?" but "should we be drifting from our patterns?"

## Evidence

- Richards (2020): "Both processes operate in harmony" (Figure 6 caption)
- Boyd (1986, p. 5): "Idea of fast transients suggests that, in order to win, we should operate at a faster tempo or rhythm than our adversaries — or, better yet, get inside adversary's observation-orientation-decision-action time cycle or loop"
- Boyd never described OODA as sequential: "Observation, orientation and action are continuous processes, and decisions are made occasionally in consequences of them" (Storr objection, cited by Richards)
- Honda vs. Yamaha: 113 new models in 18 months. Decisive factor was not speed through the loop but that each pass improved orientation. "Just going through some loop without learning anything is a waste of time"

## Risks

- Over-relying on IG&C (fast path) produces confident wrong actions when orientation is stale. Trust scoring must decay with time since last validation.
- Under-using IG&C forces explicit Spec for situations where compiled orientation is sufficient, creating Böckeler's "Verschlimmbesserung" — making things worse through overhead.
- Behindigkeit is hard to operationalize — how does overwatch distinguish "healthy drift from doctrine" from "unhealthy drift from discipline"?
