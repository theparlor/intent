---
id: SIG-2026-06-01-ws-ddr-099-phase1-stall-watch-falsified
date: 2026-06-01
type: signal
severity: info
status: resolved
source: weekly-overwatch-sweep (Section 11a IAD disconfirmation)
related: WS-DDR-099, SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20
upstream_control_path: Core/products/org-design-tooling/.claude/commands/overwatch.md (Section 11a/11b signal-lens scope)
catch_mechanism: this signal + recommended 11a multi-source widening (commits/specs/code, not signals-only)
pipeline_survival: n/a (observation + scope note; no generated artifact to be overwritten)
---

# WS-DDR-099 Phase 1 stall-watch — FALSIFIED + measurement blind spot

## What the sweep flagged
The 2026-06-01 weekly overwatch Section 11a (disconfirmation) flagged **[IAD] WS-DDR-099
intent-knowledge MCP Phase 1** as a possible stall: "no execution-progress signal in 5 days
since scaffold; interim signals point to drag (substrate-not-materialized, sibling-spec-blocked)."

## Disconfirming evidence (the watch is wrong)
Phase 1 is **actively progressing**, not stalled. Evidence outside the signal log:
- `5ca8566 feat(intent-knowledge): build D1–D4 envelope/verb extensions + preservation_invariant (DEC-012)` — ~2026-05-31
- `6c65f48 docs: refresh substrate-exposure Phase 1 checkpoint — all 4 agents complete`
- `605cf6c test(intent-knowledge): substrate-exposure verb suite (34 tests)`
- `f3cf63e feat(substrate): Phase 2 swap — BM25 via library-index-mcp import` (already into Phase 2 prep)
- Runnable server tree exists: `servers/knowledge.py`, `observe.py`, `notice.py`, `spec.py`, `lib/classification.py`, `lib/library_index_client.py`
- Specs current: `spec/substrate-exposure-architecture.md` (05-29), `spec/SPEC-substrate-exposure-envelope-extensions-DRAFT.md` (05-31), `servers/DEPLOYMENT-INTENT-KNOWLEDGE.md` (05-29)

## The real finding (meta) — Boyd's external reference point had a blind spot
Overwatch is the "outside reference point" that guards against incestuous amplification. But its
Section 11a/11b lens reads **only `.intent/signals/`**. WS-DDR-099 progress was recorded as
**commits, specs, and code** — invisible to a signals-only staleness check. The sweep therefore
manufactured a false stall-positive: the watchdog confirmed its own framing (no signal = no progress)
rather than checking reality. This is the exact pathology Section 11 exists to catch, occurring inside
Section 11 itself.

## Recommended upstream fix (overwatch Section 11a)
When disconfirming a DDR/product claim, widen the evidence lens beyond `.intent/signals/` to include
`git log` (since the claim date) and spec/code-tree mtimes for the named component. A DDR is "stalled"
only if NONE of {signals, commits, specs, code} moved — not if signals alone are quiet. Active builders
who commit-but-don't-signal are a known pattern, not a stall.

## Disposition
- WS-DDR-099 Phase 1: **on-track** (Phase 1 substantially complete; Phase 2 BM25 swap underway). No action.
- Overwatch 11a lens-widening: captured here for the next overwatch skill revision.
