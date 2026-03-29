---
id: SIG-003
timestamp: 2026-03-28T12:00:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.35
autonomy_level: L1
status: active
cluster: signal-capture-surfaces
parent_signal:
related_intents: []
---
# Signal: Conversations should automatically feed the notice layer

## Observation

During the Cowork session that produced the work ontology and OTel mapping, Brien asked: "how do we take this thread here between us and turn it into consideration and part of the intent ideation and notice layer as we talk?"

## Implication

If Intent is a system for surfacing and acting on insights, then the insights generated during Cowork/Claude sessions are primary signal sources. They should flow into `.intent/signals/` with minimal friction — ideally automatically.

## Proposed Mechanism

1. **During session**: Human or Claude identifies key insights and writes signal files to `.intent/signals/` in real time (what we're doing right now)
2. **Post-session**: An extract-signals agent reads the conversation transcript (available via Cowork session API or Entire.io capture) and proposes signal files
3. **On schedule**: The observe-cycle agent reads accumulated Entire.io traces and extracts signals automatically

## Design Constraint

Signal extraction must be high-precision, low-volume. The notice layer should contain 3-5 high-quality signals per session, not 50 low-quality ones. The agent should surface what's surprising or non-obvious, not summarize everything.

## Dogfooding Note

This signal file was itself generated during the conversation it describes — demonstrating the pattern in action.
