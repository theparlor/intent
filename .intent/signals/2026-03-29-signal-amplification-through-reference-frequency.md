---
id: SIG-015
timestamp: 2026-03-29T22:30:00Z
source: conversation
author: brien
confidence: 0.9
trust: 0.55
autonomy_level: L2
status: active
cluster: signal-capture-surfaces
parent_signal:
related_intents: [signal-trust-framework, enrichment-pipeline]
---
# Signal amplification through reference frequency

During v0.6.0 development, a pattern emerged: the same signals kept getting referenced in conversation — SIG-008 (signals die in context switches), SIG-014 (agent context limits cause content drift) — not because anyone was tracking references, but because the work kept bumping into the same friction points. Each reference is an implicit vote: "this signal matters more than its static trust score suggests."

This is analogous to well-understood patterns in other domains:
- **OTel alerting**: An error that happens once is a log line. An error that happens 12,000 times in a day is a P1 incident. Frequency changes urgency.
- **Academic citation**: A paper's quality is fixed at publication, but its influence compounds as other papers cite it. PageRank is built on this insight.
- **Epidemiology**: A single case is surveillance. A cluster is an outbreak. The count itself changes the classification.

The Intent signal model currently treats each signal as a static document with a fixed trust score. But signals have a **frequency dimension** that we're not capturing. Every time a conversation, agent trace, or new signal references an existing signal, that's a tally mark that should change the signal's effective weight.

## What this implies for the schema

1. **`referenced_by` field**: List of signal IDs, conversation IDs, or commit SHAs that reference this signal
2. **`reference_count` computed field**: Length of referenced_by, or a time-decayed count
3. **Amplification factor in trust scoring**: Base trust + f(reference_frequency, recency)
4. **Re-evaluation trigger**: When reference_count crosses a threshold, re-run trust scoring
5. **Co-reference clustering**: Signals that get referenced together reveal emergent problem structure

## Trust Factors

- Clarity: 0.8 (the pattern is clearly observed and well-analogized)
- Blast radius: 0.5 (changes the trust model, the enrichment pipeline, and potentially the signal template)
- Reversibility: 0.7 (additive schema change, doesn't break existing signals)
- Testability: 0.6 (can instrument reference tracking and measure whether amplified signals correlate with promoted intents)
- Precedent: 0.3 (novel within Intent, but well-precedented in citation analysis and alerting systems)
