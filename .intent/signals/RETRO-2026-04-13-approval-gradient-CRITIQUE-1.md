---
id: RETRO-2026-04-13-approval-gradient-CRITIQUE-1
type: critique
source: session-analysis
created: 2026-04-13
topic: approval-gradient
severity: medium
related:
  - RETRO-2026-04-13-approval-gradient-SIG-2
  - RETRO-2026-04-13-approval-gradient-DEC-3
status: open
---

# Critique: Phase 2 Trust Model Has Unresolved Computation Dependencies

## The Problem

The contextual action trust model (DEC-3) is architecturally sound but computationally incomplete. Two of four factors (precedent at 0.35 weight, novelty at 0.20 weight) require payload similarity comparison. Combined, these factors represent 55% of the trust score. Without a defined similarity metric, Phase 2 can't ship.

## What's Unresolved

1. **Payload similarity metric.** How does the system determine that today's Slack message to #subaru is "similar" to the one Brien approved yesterday? Options range from simple (template matching, keyword overlap) to complex (embedding cosine similarity). Each has different accuracy, cost, and infrastructure requirements.

2. **Per-action-type payload schemas.** Slack messages (channel + text + blocks), emails (to + subject + body), PRs (repo + title + body + base), and calendar events all have different structures. Similarity computation may need to be action-type-specific.

3. **Familiarity decay.** Brien communicates with #subaru daily now, but engagements end. Familiarity should decay over time — a channel Brien hasn't messaged in 30 days shouldn't retain high familiarity. The decay function isn't specified.

## Why This Matters

Brien's ceremony tax concern is valid and urgent. If Phase 2 stalls because the similarity metric isn't designed, Brien lives with full-gate friction indefinitely. The risk isn't that Phase 2 is wrong — it's that the unstated computation dependency delays it.

## Recommended Approach

Start simple, validate, upgrade:
1. **Template matching** — if Brien approves "standup update: {variable}" and the next message matches the template, precedent is high. No ML needed.
2. **Structural fingerprint** — hash the non-variable parts of the payload. Similar fingerprints = similar payloads.
3. **Keyword overlap** — Jaccard similarity on extracted keywords. Cheap, interpretable.
4. **Embeddings** — only if 1-3 fail to discriminate routine from novel.

Design the metric during Phase 1. Test it against Phase 1's approval records before shipping Phase 2.
