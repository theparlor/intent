---
signal_id: SIG-2026-05-29-stop-hook-check-7-scope-variant
type: enforcement-hardening
created: 2026-05-29
priority: medium
status: resolved
component: hooks/autonomy-grant-stop-check.sh (Layer 4 linguistic detector)
upstream_control_path: "hooks/autonomy-grant-stop-check.sh CHECK 7 — the Stop-hook block is the mechanism-level control; fires on the scope-variant question pattern regardless of recommendation marker"
catch_mechanism: "CHECK 7 block decision + ~/.claude/audit/autonomy-grant-stop-detections.log (CHECK7-CAUGHT) + JSONL telemetry (check:7 fields) for frequency observability"
pipeline_survival: "yes — hook is registered as a Stop hook in settings.json; runs on every Stop. bash -n clean; e2e-tested (positive blocks, negative + tech-A/B pass, no hang)."
---

# CHECK 7 — scope-variant bare-choice ("do part OR do all") on pre-authorized work

## Gap

CHECK 1 (bare-choice) blocks `(want me to|should i) X or Y?` ONLY when no
recommendation marker exists anywhere (`BARE_MATCH=1 AND REC_MATCH=0`). The
**scope-variant** — "Want me to do just the first tier, or all of them?" — slips
past because a recommendation almost always precedes it (`REC_MATCH=1` disables
CHECK 1). This is the variant the charter named: a scope choice between a partial
subset and the full set of already-authorized work, re-litigating a scope Brien
has already set ([[feedback_full_scope_execution]]).

## Fix

Added CHECK 7: fires REGARDLESS of `REC_MATCH` (the recommendation is exactly what
lets it slip CHECK 1), gated only by `dispatch=0`. Detection = AND of four fast
independent greps in the last paragraph: a lead-in question + a partial-scope
token + a full-scope token + "or". The conjunction keeps the FP rate low — a
genuine technical A/B ("Postgres or SQLite?") lacks the partial+full scope tokens
and passes clean (verified).

## Load-bearing implementation finding (→ friction candidate)

The first attempt used a single bounded-quantifier multi-group ERE
(`LEAD[^?]{1,160}(PARTIAL)[^?]{1,120}\bor\b[^?]{1,120}(FULL)[^?]{0,120}\?`). It
**catastrophically backtracks under ugrep** (the system grep on this host,
aliased at /usr/bin/grep) and HANGS. A hung regex in a Stop hook would freeze
EVERY Stop event — blocking all responses. This is a latent risk in the hook's
whole design pattern: any future mega-regex check could hang the Stop path. The
mitigation here was decomposition into simple ANDed greps; the broader lesson is
captured as a friction signal (regex-engine assumptions in load-bearing hooks are
unvalidated). The charter's "test with piped sample JSON first" instruction is
what caught it before it went live.

## Verification

- isolation: 5 positives match, 5 negatives pass (incl. tech-A/B, rec-reveal, completion)
- `bash -n` clean
- e2e via piped Stop JSON + fixture transcripts: positive (scope-question with a
  recommendation) → CHECK 7 block; normal completion → exit 0 no block; tech-A/B
  → exit 0 no block; no hang
