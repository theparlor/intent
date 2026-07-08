---
id: SIG-2026-05-30-friction-unification
created: 2026-05-30
type: friction-unification/meta-synthesis
status: symptom-repaired, upstream-pending
severity: S1 (two latent self-harm items partially addressed)
confidence: 0.92
trust: 0.72
author: claude-sonnet-4-6 (session 2026-05-30)
cluster: SIG-2026-05-29-friction
related:
  - SIG-2026-05-29-friction-00-road-readiness-drag-synthesis
  - SIG-2026-05-29-road-readiness-friction-series
  - SIG-2026-05-29-friction-01-stop-hook-lexical-arms-race
  - SIG-2026-05-29-friction-02-catch-net-brittleness-bidirectional
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - Core/products/cast/farm/freshening-schedule.yaml
  - feedback_audit_vs_writethrough
  - feedback_recalibrate_saturated_metrics
  - feedback_demonstrable_function_over_machinery
  - project_cast_topical_relevance
upstream_control_path: >
  F-1: pre-commit hook on hooks/ dir wired to hook_regex_contract.py (wiring is the remaining step).
  F-4: write-boundary gate teaching automated signal writers to run closure_writeboundary_check.py
  before emitting (write-through; catch-net is installed, routing is the remaining step).
catch_mechanism: >
  Core/frameworks/intent/tools/hook_regex_contract.py (F-1 catch-net — 24 tests pass).
  Core/frameworks/intent/tools/closure_writeboundary_check.py (F-4 catch-net — 21 tests pass).
pipeline_survival: >
  The two catch-net tools are standalone and wirable to pre-commit/CI; they are not yet wired.
  Standalone tools survive; pre-commit wiring and the lexical sunset (2026-06-12) remain open.
---

# Friction Unification — Both Catalogs Are Instances of One Anti-Pattern

## The anti-pattern

> **A score or gate that measures its own ACTIVITY (a proxy) instead of the OUTCOME it serves —
> with no value term — saturates or accretes overhead and cannot converge.**

Both friction catalogs captured on 2026-05-29 are instances of this one structural failure.
The friction-00..05 series identifies it at the **measurement/architecture level**.
The F-1..F-8 series captures **live operational instances** of the same failure.
They are two halves of one backlog, not duplicates.

The pattern appears across products (enforcement layer, Cast scoring, closure governance) because
it is a systemic property of proxy-measurement systems with no value term and no convergence proof —
not a bug in any single component.

---

## Catalog mapping (from SIG-2026-05-29-friction-00 §Companion)

| F-series (live instance) | friction-series (structural) | Anti-pattern manifestation |
|---|---|---|
| **F-1** regex can HANG the Stop hook (self-DoS, ugrep backtracking) — S1 | friction-01 + friction-02 | Catch-net (hook) measuring its own completeness (CHECK N+1 for every variant) with no termination condition — and the catch-net mechanism itself has a catastrophic failure mode |
| **F-8** closure hook false-fires on conversational words — S2 | friction-02 (false-positive class) | Proxy measure (completion-words) without outcome gate (was a tracked unit actually closed?) |
| **F-4** closure-discipline NOT enforced on automated writers — S1 | friction-00 (new angle) | Enforcement measures the interactive agent's output, not the governance outcome (signals actually resolve cleanly) — the enforcement layer can be trivially bypassed by the automated path it was built to govern |
| **F-2 / F-3** render_all non-deterministic + verify/produce conflation — S2 | friction-03 (per-turn tax) | DoD gate measures pipeline activity (render_all ran) not pipeline correctness (rendered output is valid) |
| **F-5 / F-6 / F-7** repo-topology / data-substrate / index drift — S3 | coherence debt | Ratified recommendations not checked against actual data coverage |

---

## Additional evidence: Cast CVRS (pattern crosses products)

From the 2026-05-29 Cast functional-base session and the cross-session handoff:

**Instance 1 — CVRS freshness dimension (corpus-touch metric):**
- The freshness score measured corpus file touch events (proxy: "was a file written?")
- Not the outcome it serves: "does the persona reflect current discourse and key sources?"
- Result: freshness pinned at 100% for all mass-touched personas — the score saturated and could
  not distinguish genuinely fresh personas from timestamp-noise from render_all runs.
- Cite: feedback_recalibrate_saturated_metrics; SIG-2026-05-30 Cast cross-session handoff §1.

**Instance 2 — Cast breadth/variety score (modern-channels proxy):**
- Breadth was measured as presence of "modern channels" (podcasts, newsletters, X/Twitter)
  without weighting by the persona's topical domain or historical period.
- Historical voices (Tubman, Lincoln, pre-digital practitioners) structurally scored 0 on
  breadth/variety regardless of actual corpus depth — the proxy is orthogonal to the outcome
  for historical/public-domain figures.
- Cite: project_cast_topical_relevance; SPEC-topical-relevance-001 (draft).

Both Cast instances are the same anti-pattern: activity proxy (file touch; channel presence)
without a value term (is the persona actually useful for the panels it serves?) and without a
saturation detector. Score ceilings were hit and declared "earned" before the saturation
was detected.

---

## F-1 fix: hook_regex_contract.py

**File:** `Core/frameworks/intent/tools/hook_regex_contract.py`

**What it does:**
- Scans `hooks/*.sh` for literal grep -E patterns (variable-expanded patterns skipped — see note)
- Timing check: runs pattern against adversarial input via subprocess.run(timeout=0.5s)
  — FAIL if it times out (catastrophic backtrack / self-DoS risk)
- Static smell: detects two shapes regardless of local grep engine:
  - Shape 1: multi-group + greedy gap + `\b` (documented ugrep ERE failure shape)
  - Shape 2: ambiguous/nested quantifier on group, e.g. `(a+)+` `(a|b+)+` (canonical NFA shape
    that hangs ugrep — the F-1 incident engine; BSD/macOS grep uses DFA and may not hang,
    but the pattern is fragile across environments)
- Exit 2 if any FAIL; exit 0 if all pass; WARN for static smells
- `--print-wrapper` prints the fail-open shell wrapper snippet

**Tests:** 24 passing (test_hook_regex_contract.py)

**This is the catch-net.** Per feedback_audit_vs_writethrough, the write-through is harder:
wiring hook_regex_contract.py into pre-commit on the hooks/ dir so that NO new regex pattern
lands without passing the timing + static smell contract. That wiring is the remaining step.

**Note on pattern extraction:** Hook patterns passed as shell variables (`grep -qiE "$BARE_CHOICE_RE"`)
cannot be resolved without executing the shell — correctly skipped. The actual BARE_CHOICE_RE
and similar mega-patterns in autonomy-grant-stop-check.sh would need to be tested by injecting
them directly as literals into hook_regex_contract.py's test harness, or by a separate
hook-execution test that pipes known adversarial inputs through the hook and measures wall time.
This is a scope gap — the tool catches NEW patterns being added, and any literal patterns in hooks.

**Live scan result (2026-05-30):** 2 literal patterns found in hooks/*.sh, both PASS.
The hooks correctly use shell variables for their mega-patterns — which is why they're not
caught by this tool's pattern extraction. The wiring step above plus a hook-execution test
harness is needed for full coverage.

---

## F-4 fix: closure_writeboundary_check.py

**File:** `Core/frameworks/intent/tools/closure_writeboundary_check.py`

**What it does:**
- Scans a signals dir for `.md` files with `status: resolved` (claiming done)
- Flags as PREMATURE-RESOLVED if:
  - Required closure-DoD fields are missing: `upstream_control_path:` or `catch_mechanism:`
  - Body contains weasel markers: follow-up, not yet, pending (as standalone value),
    needs [word], TODO, incomplete, to be [done/fixed/...], will [fix/be done/need/...]
- Weasel pattern precision:
  - "will detect / will catch / will fire / will run / will prevent" are NOT flagged — these
    describe catch-net capability, not deferred work (the F-4 false-positive class)
  - `status: symptom-repaired, upstream-pending` is NOT a violation — it is the honest
    not-yet-done designation; only `status: resolved` combined with evidence of incompleteness
    triggers a violation
- Exit 2 if violations found; exit 0 if clean
- `--dir`, `--json`

**Tests:** 21 passing (test_closure_writeboundary_check.py)

**This is the catch-net.** Per feedback_audit_vs_writethrough, the write-through is:
teaching automated signal writers to run this check BEFORE emitting. The check can be called
as a Python function or CLI at write time:
```python
from closure_writeboundary_check import check_file
violations = check_file(signal_path)
if violations:
    raise ValueError(f"Signal fails closure-DoD: {violations}")
```

**Live scan result (2026-05-30):** 18 violations found across 9 signal files.
REAL SIGNAL — reported here, not hidden.

Violation breakdown by file:
- `2026-04-06-wiki-naming-wrong.md` — missing required fields (resolved, pre-DoD era)
- `2026-04-12-karpathy-source-extraction-backlog.md` — missing required fields
- `2026-04-13-ke-mcp-write-back.md` — missing fields + "incomplete" in body
- `2026-04-13-trust-as-orientation-proxy.md` — missing required fields
- `RETRO-2026-04-08-intent-framework-SIG-2.md` — missing required fields
- `RETRO-2026-04-11-intent-site-SIG-1.md` — missing required fields
- `RETRO-2026-04-21-invocation-gap-SIG-1.md` — missing fields + "follow-up" in body
- `SIG-035-intent-mcp-servers-hardcode-ports.md` — missing required fields
- `SIG-2026-05-28-stop-hook-check-6-trailing-observation.md` — "needs new pattern class"
  (NOTE: this may be a false positive — "needs" appears in the description of what a CHECK
  targets, not as a claim that the signal's work is incomplete. Precision tuning candidate.)
- `SIG-AUDIT-2026-05-20.md` — "not yet appended" (genuine weasel)
- `SIG-EXEC-2026-05-20.md` — "will verify" hit by will-verb pattern
  (NOTE: "overwatch sweeps will verify staleness" is a capability statement; the will-verb
  pattern should exclude "verify" → false positive. Precision tuning candidate.)
- `SIG-HOOK-OVERRIDE-META-INSTRUCTIONAL-2026-05-20.md` — "needs widening" + "not yet" +
  "Follow-up" (genuine weasels — the signal has an explicit Follow-up section)
- `SIG-INTENT-BROKEN-LINKS-FIXED-2026-05-20.md` — "invariant needs to be authored"
  (genuine weasel — explicitly admits a follow-on task)

**Triage:** ~10 of 18 violations appear genuine (pre-DoD-era signals claiming resolved
without required fields, or explicit follow-up admissions). ~2-3 appear to be precision
gaps in the weasel-pattern (will-verify, needs-as-description). Both refinement candidates
are documented above; no tuning applied here to keep the catch-net conservative.

---

## What is NOT resolved

**The lexical arms-race convergence (Layer 4.2 calibration → sunset):**
The lexical Stop-hook layer is frozen at CHECK 7 per `lexical-layer-freeze.yaml`.
The structural successor (Layer 4.2 autonomy-posture check) is deployed warn-only.
The convergence path is TIME-GATED:
- Layer 4.2 14-day calibration → FP rate measured
- If FP < 5%: retire CHECKs 2 and 3 (0 fires in 45 days per drag_dashboard.py)
- Scheduled review: **2026-06-12** (per autonomy-flight-model-ratification-tracker.md)

hook_regex_contract.py and closure_writeboundary_check.py are catch-nets-for-catch-nets.
They do not replace the structural successor path; they instrument the current catch-net
layer for the hazards that the lexical approach cannot prevent (F-1: hung grep; F-4:
automated writer bypass).

---

## Closure-DoD

```
upstream_control_path:
  F-1: pre-commit hook on hooks/ dir wired to hook_regex_contract.py (tool exists; wiring
       remains — next commit to hooks/*.sh should trigger the contract check).
  F-4: write-boundary gate teaching automated signal writers to run
       closure_writeboundary_check.py before emitting (tool exists; routing to automated
       writers remains — document the import pattern above; add to signal-recording spec).
  Lexical sunset: autonomy-flight-model-ratification-tracker.md D1-D4 + 2026-06-12 review.

catch_mechanism:
  Core/frameworks/intent/tools/hook_regex_contract.py (F-1 catch-net; 24 tests passing).
  Core/frameworks/intent/tools/closure_writeboundary_check.py (F-4 catch-net; 21 tests passing).

pipeline_survival:
  Tools are standalone Python3 stdlib-only; no installation required.
  They survive as long as the tools/ directory is in the repo.
  The wiring step (pre-commit + automated-writer routing) is what makes them load-bearing
  rather than advisory. Until wired: these are advisory catch-nets requiring manual invocation.
  Wiring is a single-session task (add pre-commit config + import in signal recorder).
```

Status honestly: `symptom-repaired, upstream-pending`.
- F-1 tool: resolved at tool level (catch-net exists, shape detection works, 24 tests pass).
- F-4 tool: resolved at tool level (catch-net exists, weasel detection works, 21 tests pass).
- F-1 wiring to pre-commit: pending.
- F-4 routing to automated writers: pending.
- Lexical sunset (the root cause): pending, time-gated to 2026-06-12.

## Triage, 2026-07-08

Disposition: still pending, confirmed unchanged on the wiring question. Checked directly: no `.pre-commit-config.yaml` exists in this repo, and `.git/hooks/pre-commit` (if present) does not reference `hook_regex_contract.py` or `closure_writeboundary_check.py`. Both catch-nets remain advisory, callable manually but not load-bearing. The lexical-sunset half of this signal is tracked separately and is explicitly out of scope for tonight (files matching *layer42* are excluded from this pass; SIG-2026-06-12-layer42-calibration-review is the live thread for that). Needed control: the non-blocking `coherence-preflight` aggregator this signal itself proposes (run all standalone catch-nets, report, don't block) is still the concretely-named, not-yet-built next step.
