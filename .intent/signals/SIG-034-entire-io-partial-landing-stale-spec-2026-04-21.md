---
id: SIG-034
title: entire.io v0.5.1 partially landed — 1 of 4 Core repos actually capturing; observability-stack.md:361-367 describes pre-v0.5 structure
date: 2026-04-21
status: open
category: framework-gap
severity: high
related:
  - Core/frameworks/intent/spec/observability-stack.md (stale lines 361-367)
  - Core/frameworks/intent/spec/repo-pattern.md (Layer 3 Observability = entire.io)
  - Core/products/witness/.intent/signals/SIG-WITNESS-001 (forensics + event-tagging roadmap)
  - SIG-035 (security posture reframe — parallel sub-project dependency)
  - SIG-036 (audit-catchnet pattern — same write-through root cause)
  - memory/feedback_audit_vs_writethrough.md (canonical policy violated here)
---

# SIG-034 — entire.io partial-landing + stale observability spec

## Origin

During the 2026-04-21 Intent framework rigor audit pivot session, Brien flagged that `entire.io` "is supposed to be an outsourced layer of our intents framework accountable for traceability on signal and decisions from our session information. it is possible it never landed or fell out of the framework."

Verification of actual state follows.

## Observed state

**Installation (machine level):**
- `/opt/homebrew/bin/entire` v0.5.1 present
- 0.5.5 available (upgrade pending)
- Commands: `configure, enable, disable, rewind, reset, resume, status, explain, doctor`

**Coverage (Tier 1 = Core + frameworks, ~32 candidate repos):**
| Repo | `.entire/` present? | Capturing? |
|---|---|---|
| library-index | yes | **yes** — session data in shadow branch |
| (3 others) | yes | no — enabled but idle, manual-commit mode, never exercised |
| remaining ~28 | no | no |

**False-positive surface:** at a glance, "4/32 have `.entire/`" reads as "starting to land." Actually: 1/32 is capturing. Three are costume — directory scaffolded, zero session data written.

**Spec drift:** `Core/frameworks/intent/spec/observability-stack.md:361-367` describes `.entire/sessions/*.json` file structure. Actual v0.5.1 uses a shadow-branch model with `.entire/settings.json + logs/ + metadata/`. Spec predates the v0.5 restructure.

## Why this matters

Witness forensics (SIG-WITNESS-001), drift pipelines, and any observability consumer that assumes `.entire/` = "session data available" is being fed by one repo. The Intent framework rigor audit (sub-project #1) cannot be grounded on this substrate until it is actually capturing.

"4 landed" was a wish-state read of the directory tree, not a verified read of the shadow-branch contents.

## Root cause

**Write-through discipline gap.** The acceptance bar was: "directory created via `entire enable`." Should be: "**capturing** — session data appears under shadow-branch across N sessions of real use." Same family as SIG-036 (audit-as-catchnet) and `feedback_audit_vs_writethrough.md`: relied on later audit ("is it capturing?") instead of enforcing capture-time proof.

## Recommended fix (sub-project #5, accepted scope: D — Core + frameworks only)

1. Upgrade to 0.5.5 globally
2. Propagate `entire enable` to the 17+ missing T1 repos (Core + frameworks subtrees)
3. **Acceptance bar: (b) Capturing** — not (a) Enabled. Verified via `git log <shadow-branch>` having entries after N days / M sessions of use
4. Catalog T2 remainder (~15 products / knowledge farms) for deferred ingestion — gated on #6 security posture first
5. Update `observability-stack.md:361-367` to reflect shadow-branch model
6. Install a write-through check in Intent rigor audit (#1 deliverable): any `.entire/` without capture activity → flag stale, not landed

## Follow-up
- Sub-project #5 design doc (install + propagate + spec correction)
- Tie to SIG-036 — this is one instance of the same discipline gap symptom
- After #6 security posture Phase (a) Understand, T2 propagation plan gains the access model to protect farm-level capture

## Triage, 2026-07-08

Disposition: still pending, substantial progress (one item fixed this pass). Re-verified against live state: `entire` CLI is at v0.5.1 (recommendation #1, upgrade to 0.5.5); checked `brew`, the upgrade requires trusting the `entireio/tap` cask tap, which is a trust decision left for Brien rather than something to force through in a triage pass. Coverage has grown dramatically: 21 `.entire/` directories now exist under `Core/` (up from the 4 costume-scaffolded ones this signal found), and spot-checking `frameworks/intent`, `products/cast`, `products/library-index`, and `products/witness` shows real `entire/*-e3b0c4` shadow branches with commits dated through 2026-07-08, i.e. the acceptance-bar correction (recommendation #3, "capturing" not "enabled") is empirically satisfied for those repos. **Fixed this pass (recommendation #5):** `spec/observability-stack.md` section 4 was stale on two counts: it called Entire.io "the execution observability layer" (the same DEC-007 overclaim DEC-009 already corrected elsewhere) and described the pre-v0.5 flat `.entire/sessions/*.json` layout. Both corrected in place: the section now reads "authoring-provenance recorder... corrected 2026-05-26 per DEC-009" and describes the actual shadow-branch (`entire/<hash>-<hash>`) + `.entire/metadata/<session>/full.jsonl` structure. No explicit write-through "capturing check" was found wired into a rigor-audit deliverable (recommendation #6). T2 catalog status (recommendation #4) not verified. Remaining needed control: version bump to 0.5.5 (Brien-gated on the tap-trust decision) and, lower priority now that coverage is broad, the write-through capture-check.
