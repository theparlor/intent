# Signal Amplification Through Reference Frequency

> Source: SIG-015 — captured 2026-03-29
> Status: Draft
> Author: Brien

## Problem

The current signal trust model computes a static score at capture time:

```
trust = clarity × 0.30 + (1/blast_radius) × 0.20 + reversibility × 0.20 + testability × 0.20 + precedent × 0.10
```

This score never changes. But signals gain weight through repeated reference — when conversations, agents, and new signals keep pointing back to the same friction point, that frequency is information the system should use.

A signal referenced five times in one session is hotter than a signal referenced once across three months. The system doesn't know this yet.

## Design

### New Schema Fields

Add to the signal template frontmatter:

```yaml
# --- existing fields ---
trust: 0.45
autonomy_level: L2
status: active

# --- new amplification fields ---
referenced_by: []          # List of references: ["SIG-014", "conv:2026-03-29-v06", "commit:4aa7a2f"]
reference_count: 0         # Computed: len(referenced_by) — denormalized for fast sorting
last_referenced: null       # ISO timestamp of most recent reference
amplification_score: 0.0   # Computed: dynamic boost from reference frequency
effective_trust: 0.45      # Computed: base trust + amplification_score
```

### Amplification Formula

The amplification score uses a time-decayed reference count:

```
amplification_score = Σ weight(ref_i) × decay(age_i)
```

Where:
- `weight(ref)` depends on reference source:
  - Signal → Signal reference: **0.15** (a new signal citing this one)
  - Conversation reference: **0.10** (human or agent naturally references it)
  - Commit reference: **0.05** (code change that addresses or relates to signal)
  - Intent/Spec reference: **0.20** (formal work product links back)
- `decay(age)` is an exponential decay with half-life of 7 days:
  - `decay = 0.5 ^ (age_days / 7)`
  - A reference from today has weight 1.0
  - A reference from 7 days ago has weight 0.5
  - A reference from 30 days ago has weight ~0.05

### Effective Trust

```
effective_trust = min(1.0, base_trust + amplification_score)
```

Capped at 1.0. The amplification can push a signal's effective trust across autonomy level boundaries — an L0 signal that keeps getting referenced can graduate to L1 or L2 purely through amplification.

### Re-evaluation Triggers

When a signal's `effective_trust` crosses an autonomy level boundary, trigger re-evaluation:

| Crossing | Action |
|----------|--------|
| L0 → L1 | Notify: "Signal gaining traction, consider enrichment" |
| L1 → L2 | Auto-enrich: run Context Agent and Trust Scorer |
| L2 → L3 | Draft intent + spec for human review |
| L3 → L4 | Flag for autonomous execution (requires circuit breaker config) |

Re-evaluation also triggers when:
- `reference_count` increases by 3+ in a single session
- Two or more signals in the same cluster all get referenced in the same conversation
- A signal that was `dismissed` gets re-referenced (potential false dismissal)

### Co-Reference Clustering

Signals that get referenced together in the same context (conversation, commit, agent trace) form **emergent clusters** — distinct from the manual cluster assignments in the current schema.

```yaml
# In events.jsonl
{
  "event": "signal.co_referenced",
  "data": {
    "signals": ["SIG-008", "SIG-014", "SIG-015"],
    "context": "conversation:2026-03-29-v06-session",
    "co_reference_count": 3
  }
}
```

When the same signal pair co-occurs across 3+ contexts, the system should suggest a cluster merge or a new parent signal that captures the shared theme.

This is the system *self-organizing*. The signals reveal their own architecture through the pattern of what gets referenced together.

## Implementation Plan

### Phase 1: Schema (now)
- [ ] Add `referenced_by`, `reference_count`, `last_referenced`, `amplification_score`, `effective_trust` to signal template
- [ ] Update `intent-signal` CLI to accept `--references SIG-XXX` flag on capture
- [ ] Update `intent-signal review` to show effective_trust alongside base trust
- [ ] Emit `signal.referenced` event when a reference is added

### Phase 2: Tracking (next)
- [ ] Build reference tracking in the enrichment pipeline
- [ ] Auto-detect references in conversation transcripts (pattern: "SIG-NNN" or signal title)
- [ ] Auto-detect references in commit messages
- [ ] Compute amplification_score on each reference event

### Phase 3: Re-evaluation (later)
- [ ] Implement autonomy level crossing detection
- [ ] Auto-enrich signals that cross L1 → L2
- [ ] Draft intent+spec for signals that cross L2 → L3
- [ ] Co-reference clustering with merge suggestions

## Open Questions

1. **Should dismissed signals be resurrectable?** If a dismissed signal starts getting re-referenced, should it automatically change status back to `active`? Current instinct: yes, with a `signal.resurrected` event.

2. **Self-referential amplification?** SIG-015 describes amplification, and will itself be referenced when implementing amplification. Should a signal's own implementation references count toward its amplification? Probably not — exclude references from implementation work on the signal itself.

3. **Amplification ceiling?** Should there be a max amplification_score (e.g., 0.3) to prevent a frequently-referenced but fundamentally low-trust signal from reaching L4? Or does the formula's time decay handle this naturally?

4. **Cross-repo references?** When Intent is installed on Brien's 4 repos, should a signal in repo A that gets referenced in repo B's commit count? This connects to the multi-machine sync problem (SIG-013).
