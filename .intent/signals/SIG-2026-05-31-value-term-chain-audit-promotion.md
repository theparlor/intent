---
id: SIG-2026-05-31-value-term-chain-audit-promotion
product: intent
type: structural-completion
status: resolved
created: 2026-05-31
track: road-readiness A.1
upstream_control_path: "Core/frameworks/intent/tools/value_term_invariants.py (cross-product chain_audit invariant class) + per-product write-through registries Core/products/{cast,topography,pulse}/value-term-registry.yaml + Core/frameworks/intent/tools/value-term-registry.yaml — the score-owner declares each score beside its code"
catch_mechanism: "value_term_invariants.py INV-VALUE-TERM-CLEAN (every registry audits clean) + INV-VALUE-TERM-COVERAGE (every score-product has a registry); tests test_value_term_invariants.py (9) + test_value_term_audit.py (30, incl. --all cross-product discovery); advisory --scan grep for unregistered score code"
pipeline_survival: "Registries are declarative YAML read at audit time; no pipeline stage (render_all, compute-cvrs, etc.) writes or wipes them — unlike the compute-cvrs sibling-wipe pattern. The invariant is read-only and side-effect-free; running it cannot regress the scores it audits."
verification_command: "cd Core/frameworks/intent/tools && python3 -m pytest test_value_term_audit.py test_value_term_invariants.py -q  # 39 passed; python3 value_term_invariants.py  # exit 0"
---

# Value-Term Audit → Cross-Product Chain-Audit Invariant Class (road-readiness A.1)

Promoted the value-term/outcome catch-net (intent `094ced2`: a single-registry tool)
into a **cross-product chain_audit invariant class** with per-product write-through
registries. This institutionalizes the anti-pattern the whole road-readiness arc proved:
**a score that measures its own activity (a proxy) instead of the outcome it serves cannot
converge** (flight-model §1; SIG-2026-05-30-cross-session-coherence §1).

TDD throughout (RED → GREEN per the Iron Law); 39 tests pass; the live ecosystem audit and
the invariant class both exit 0 on day one (zero-violation-start — the known violations are
registered as *tracked* defects, not untracked ones).

## RESOLVED (this session) — the structural catch-net

- **Cross-product engine** — `value_term_audit.py --all [ROOT]` discovers every
  `value-term-registry.yaml` under Core/ (skipping `.venv`/`.worktrees`), audits each,
  aggregates, exit 2 on any FAIL. New `discover_registries()`. Existing `--registry` and
  `--scan` preserved (no regression: 30/30 original + new tests).
- **Per-product write-through registries** — split the intent-repo monolith (the drift
  defect: a cast score declared in the intent repo never gets edited) into:
  - `products/cast/value-term-registry.yaml` (7 entries — 5 CVRS dims + 2 relevance scores)
  - `products/topography/value-term-registry.yaml` (2)
  - `products/pulse/value-term-registry.yaml` (2)
  - `frameworks/intent/tools/value-term-registry.yaml` (3 intent-own; cast entries migrated out)
- **Chain-audit invariant class** — `value_term_invariants.py` (INV-VALUE-TERM-CLEAN +
  INV-VALUE-TERM-COVERAGE), `--emit-signal` with honest-DoD frontmatter, exit 0/1; matches
  the `cortege_invariants.py` / `chain_audit_portfolio.py` convention. Intended consumer:
  org-design-tooling `governance_audit.py` nightly + overwatch.
- **Operator doc** — `value-term-registry-README.md` (loop · schema · consumer matrix).
- **TOOLS-INDEX.md** entry (was absent).

## TRACKED, NOT FIXED (downstream) — the 3 violations are now *visible and audited*

Registering a defect makes the catch-net WATCH it; it does not fix the score. Each is
`status: defect` + remediation, so the audit is clean while the fix is owned elsewhere:

| Violation | What it measures today | Remediation (owner) |
|---|---|---|
| cast `synthesis_quality` ([compute-cvrs.py:341](../../../products/cast/engine/scripts/compute-cvrs.py)) | our synthesis-production (model-tag cap + synthesis recency) — handling proxy, 25/85≈29% of CVRS | decouple from model-tag/our-recency; derive from corpus synthesizability — CVRS recalibration (cast, 3 dims saturated 2026-05-29) |
| topography `vision_align` ([score.py:35](../../../products/topography/src/topography/score.py)) | hand-entered 0.9 with no canonical vision doc (no outcome signal) | Track B decision A — author vision doc under Throughline; pass vision=None until then |
| pulse activity counters ([digest.py:222](../../../products/pulse/src/digest.py)) | channels_polled / items_extracted — loop runs daily but is activity-closed, not outcome-closed | ✅ **CLOSED 2026-05-31** → `pulse-outcome-feedback` (acted_on_rate) + `score.saturation_report` added; activity counters flipped defect→fixed. Trace: `products/pulse/.intent/signals/SIG-2026-05-31-pulse-value-term-close.md` |

Corrected against disk (trust disk over stale signal): the handoff's "Pulse: no loop ever
closed" is false — briefs run daily 2026-05-06→05-31; the real gap is the missing
outcome-feedback signal. Topography's "phantom 10%" is mathematically sound
(weight applied/redistributed correctly); the real defect is the unsourced input. Cast
`breadth` "fixed" claim verified TRUE (work-forms path at compute-cvrs.py:662-679).

~~One honest WARN remains on `pulse-relevance-score` (no saturation_guard)~~ — **WARN cleared
2026-05-31**: `score.saturation_report` (skip_rate≥0.95 OR T1+T2==0) is now the registered
saturation_guard, wired into every brief. Demonstrated against the real brief history it
fires on 12/13 (every brief since 05-20). The 381/383 tier-4-skip rate is exactly what it now
catches. Ecosystem `--all` is now 0 FAIL · **0 WARN**.

## Commits (per-repo coherent units, specific-file staging)
- intent: engine `--all` + invariant class + tests + registry migration + operator doc
- cast / topography / pulse: each product's `value-term-registry.yaml`
- workspaces: TOOLS-INDEX.md + handoff A.1 status + this signal
