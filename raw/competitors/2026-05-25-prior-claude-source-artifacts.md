---
title: Prior Claude Session — source artifacts (3)
type: external-input / source-archive
source: prior Claude session (separate from this Workspaces session)
date: 2026-05-25
ingested: 2026-05-26
ingest_session_signal: .intent/signals/SIG-2026-05-26-flight-model-ingestion.md
status: archived-verbatim
contents:
  - intent_signal_inventory.py (v0 discovery crawler)
  - autonomy-flight-model v0.1 DRAFT (coupled forces spec)
  - autonomy-gate-matrix v0.1 DRAFT (12-surface × mode table)
related:
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md (this-session synthesis)
  - Core/frameworks/intent/spec/autonomy-gate-surface-matrix-v0-DRAFT.md (this-session elevation)
  - Core/frameworks/intent/tools/intent_signal_inventory_v0.py (v0 script archived)
  - Core/frameworks/intent/tools/intent_signal_inventory.py (re-grounded v1)
---

# Prior Claude Session — Source Artifacts

> Verbatim archive of the three artifacts produced by the prior Claude session, 2026-05-25.
> Each is preserved as-written for archeology.
> Where this-session work supersedes or extends, the relationships are noted in the
> companion artifacts at the paths in `related:` above.

---

## Artifact 1 — `intent_signal_inventory.py` (v0)

> Re-archived at `Core/frameworks/intent/tools/intent_signal_inventory_v0.py`.
> v0 limitation: handles JSON/JSONL only. Brien's actual signal corpus is YAML-frontmatter
> in markdown — v0 would underreport the corpus by >95%. Re-grounded v1 at
> `Core/frameworks/intent/tools/intent_signal_inventory.py`.

```python
#!/usr/bin/env python3
"""
intent_signal_inventory.py — Discovery-first inventory of Intent drift/autonomy signal.

Purpose: turn "I don't know what calibration data I have or where" into a measurement.
This does NOT normalize or extract a training set yet — it INVENTORIES. Discovery
before extraction. It makes no assumptions about exact field names; it reports the
schema it actually finds and counts records that look like autonomy-calibration gold.

Usage:
    python intent_signal_inventory.py /path/to/intent-repo /path/to/productA /path/to/productB ...

Output:
    - human-readable report to stdout
    - machine-readable inventory.json in the current directory
"""

from __future__ import annotations
import json, sys, os
from pathlib import Path
from collections import Counter, defaultdict

# --- What we hunt for -------------------------------------------------------

INTENT_MARKERS = [".intent", "spec", "specs"]            # dirs that mean "intent-wired"
JSONL_GLOBS = ["*.jsonl", "*.ndjson"]                    # event streams
JSON_GLOBS = ["events*.json", "drift*.json", "*signals*.json"]
MD_SIGNAL_HINTS = ("signal", "drift", "ddr", "contract") # md filenames worth counting

# Keys that, if present on a record, indicate autonomy-calibration relevance.
AUTONOMY_KEYS = {
    "boundary_crossed", "review_flagged",
    "autonomy_level", "old_autonomy", "new_autonomy",
    "trust", "old_trust", "new_trust", "trust_factors",
    "blast_radius", "reversibility", "testability", "clarity", "precedent",
}
# Keys that suggest a human verdict exists -> the was-the-grant-right LABEL (gold).
LABEL_KEYS = {
    "human_decision", "override", "overridden", "accepted", "rejected",
    "approved", "approver", "outcome", "verdict", "human_in_loop", "resolution",
}

# [Full script content preserved at tools/intent_signal_inventory_v0.py]
```

---

## Artifact 2 — `autonomy-flight-model` v0.1 DRAFT

> Synthesized + extended in this-session at
> `Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md` (SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001).
> The v1 adds: substrate-blending (Witness, Voices, Cast, Throughline, Topography, Loom mappings),
> ratification dependencies, panel-composition recipe, "what this is NOT replacing" section,
> Coherence-Engineering frame correction, sequenced build plan.

```markdown
---
artifact: autonomy-flight-model
version: 0.1
status: draft
supersedes: trust-formula-v1 (additive weighted sum)
relates_to: [autonomy-gate-matrix, L0-L4, observe-loop, drift-signals]
origin: agent
---

# The Autonomy Gate as Flight Dynamics

The v1 gate was an **additive weighted sum** — facets treated as independent
contributions. Flight is **coupled**: the forces derive from and constrain each
other and must be solved together. This artifact reframes the gate as a small
coupled system with a *tunable* operating point, replacing a caution-biased
scoring rubric with a model that can be flown hotter on purpose.

## The four forces

| Force           | Direction             | Autonomy analogue                                            | Notes                                                     |
| --------------- | --------------------- | ------------------------------------------------------------ | --------------------------------------------------------- |
| **Gravity (W)** | down (constant pull)  | inherent stakes: `blast_radius × exposure × irreversibility` | always present; must be overcome to fly                   |
| **Thrust (T)**  | forward (engine)      | drive to act: `strategic_value × λ`                          | λ = **coefficient of bravery** (the throttle)             |
| **Lift (L)**    | up (holds you aloft)  | recoverability: `f(containment, detection_speed, reversibility/fail-forward)` | generated by configuration **and** airspeed (active loop) |
| **Drag (D)**    | back (opposes thrust) | overhead of caution: approval latency + stage-gate friction + re-explain tax + HITL wait | **induced drag** rises as you add lift machinery          |

## Flight conditions

- **Airworthy (grant autonomy):** `L ≥ W` — you can recover from the worst case → cleared to act.
- **Climb (increase autonomy):** `T > D` **and** `L ≥ W` — excess thrust over overhead, lift adequate.
- **Stall (the caution crash):** thrust too low → airspeed too low → `L` collapses below `W` → you fall.
  *Too timid is a crash mode.* No action → no loop data → lift decays. **This is where Intent flies today.**
- **Overspeed (the recklessness crash):** high `T`, `L < W` — moving fast with inadequate recovery. The crash to actually fear.
- **Best L/D (operating target):** maximize autonomy per unit overhead. The efficient cruise; the tuning goal for λ.

## The coefficient of bravery (λ)

λ is a knob **in the model, not in the LLM**. The LLM regresses to population-average
caution; moving the decision out of the LLM is what makes "be braver where it's worth it"
a tunable parameter instead of a personality trait of the model.

- λ low → underpowered → stall-prone (v1 default).
- λ high with inadequate lift → overspeed → structural failure.
- The **flight envelope** = the set of `(λ, configuration)` where `L ≥ W` and you sit between
  stall and overspeed. You *widen the envelope by building lift* (containment + a faster loop) —
  i.e., containment buys autonomy, now with a stability rationale.

## Modeling technique: estimate, then decide

Two stages, deliberately separated:

1. **Estimation (LLM, with uncertainty).** Ask the model only for the *inputs* to each force —
   blast radius, value, reversibility, detection speed — each as an estimate **plus variance**
   (the weather: forecastable to a degree, never removed). LLMs are good at this and bad at the
   verdict; keep them on estimation.
2. **Decision (deterministic, tunable).** Compute `W, T, L, D`. Check airworthiness `L ≥ W`.
   Compute climb capacity `T − D`. Apply λ. Locate within the envelope. Emit:
   autonomy level **and** recovery primitive.

High-variance estimates route to a **cheap probe** (ephemeral wiki / dry run), not to default
human escalation.

## Calibrating λ from the drift corpus

The recorded autonomy-drift signals are a **labeled calibration set**. Fit λ by minimizing
*both* crash types simultaneously:

- **drift-toward-stall** — gate was too tight; the grant should have run hotter (false caution).
- **drift-toward-overspeed** — gate was too loose; the grant exceeded recoverable limits (false grant).

λ is learned from your own history, not guessed. Re-fit as the corpus grows; λ may differ by
altitude and by surface.

## Recovery primitive is envelope-dependent (V1)

Recovery is not a fixed rollback policy — it depends on position in the flight:

- **Before V1 (low airspeed / pre-commit):** reject the takeoff — **rollback**.
- **Past V1 (committed / airborne):** fly through and divert — **fail-forward**.

Teach users the rule, not the reflex: *stop reaching for the brakes once you're already airborne.*

## Decision rights by altitude (pilot vs. tower)

- **Cockpit (pilot):** fast, tactical, local — engineer + agent. Holds the controls in the moment.
- **Tower (ATC):** strategic, slower, portfolio/org altitude. Sequences traffic, owns the airspace.
- **Autopilot:** flies the continuous coupled math indefinitely.
- **Reserved-for-pilot:** the handful of decisions never to be programmed — novel, ethical,
  genuinely strategic (the ditch-in-the-river call).

## Why this lives above the harness/prompt layers

A bravery coefficient computed by a coupled model fit to drift data cannot exist at the prompt
or harness layer — it requires the operating-model substrate: typed artifacts, an Observe loop
that emits drift signals, and a topology defining pilot vs. tower. That substrate **is** the
coherence layer. This is the defensible ground.

## Next build steps

1. Extract and structure the existing drift signals into a labeled `(inputs, outcome, was-grant-right)` set.
2. Formalize `W, T, L, D` as functions of the v1 facets + the missing terms (value, detection latency, containment, actor competence).
3. Define the envelope boundaries (stall line, overspeed line) and solve for the safe λ range per configuration.
4. Wire the estimate→decide split into the intent-notice / intent-observe MCP servers.
```

---

## Artifact 3 — `autonomy-gate-matrix` v0.1 DRAFT

> Elevated to its own spec at
> `Core/frameworks/intent/spec/autonomy-gate-surface-matrix-v0-DRAFT.md`
> (SPEC-INTENT-AUTONOMY-SURFACE-MATRIX-001). Sibling to the flight-model spec —
> flight model = HOW the gate computes; surface matrix = WHERE the gate applies + deterministic preconditions.

```markdown
---
artifact: autonomy-gate-matrix
version: 0.1
status: draft
plane: bridge   # governs Execute against the Ownership Topology
relates_to: [trust-formula, contract, L0-L4]
origin: agent
---

# Intent — Autonomy Gate Matrix

Maps each **execution surface** an agent can touch to the **autonomy floor** required
and the **deterministic precondition (hook)** that must hold *before* the action fires.

## How to read this

- **Autonomy floor (contained)** assumes the listed containment posture is in place.
  Strip the containment and drop one or two levels — containment is the lever that
  *buys* autonomy without lowering the harm bar.
- **Deterministic precondition (hook)** is the *law* layer: it fires regardless of the
  trust score. Trust governs the ceiling (how much autonomy you grant); the hook governs
  the floor (what is forbidden until a precondition holds). A failed hook blocks the
  action even at L4.
- Every surface splits into **read vs. mutate** — the gate behaves very differently
  across that line, and collapsing them is the most common design error.
- Today's trust formula has *no value term and no detection-latency term*. Until those
  land, treat these floors as a caution-biased baseline to be loosened deliberately
  (see shadow-autonomy calibration), not as settled safe limits.

## Matrix

| #    | Surface    | Mode                                 | Inherent blast radius | Containment posture (the lever)                          | Autonomy floor (contained) | Deterministic precondition (hook)                            |
| ---- | ---------- | ------------------------------------ | --------------------- | -------------------------------------------------------- | -------------------------- | ------------------------------------------------------------ |
| 1    | Filesystem | read                                 | low                   | path allowlist, no symlink escape                        | L1                         | path ∈ allowlist; resolved real-path stays inside root       |
| 2    | Filesystem | write / edit                         | medium                | workspace sandbox; all targets git-tracked               | L2                         | inside workspace root; file is git-tracked (recoverable); not matching protected globs (`.env`, `**/secrets/**`, CI config) |
| 3    | Repo / git | read / clone                         | low                   | read-only token                                          | L1                         | token scope is read-only                                     |
| 4    | Repo / git | commit to branch                     | low–med               | feature branch only, never protected                     | L2                         | target branch ∉ protected set; no `--force`; commit signed   |
| 5    | Repo / git | push / open PR                       | medium                | PR + required review + CI gate                           | L3                         | targets a PR, not direct-to-main; merge blocked until CI green + human approve |
| 6    | Terminal   | read / inspect                       | low                   | non-mutating command class                               | L1                         | command ∈ read-only allowlist (`ls`, `cat`, `git status`, …) |
| 7    | Terminal   | mutate (install / build / exec / rm) | high                  | ephemeral/disposable container + snapshot                | L3                         | running in disposable env; rollback point exists; command ∉ denylist (`rm -rf /`, `curl … \| sh`, credential reads) |
| 8    | Database   | read                                 | low–med               | read replica + row/column scoping                        | L2                         | connection uses read-only role/replica; query has `LIMIT`; restricted columns require explicit grant |
| 9    | Database   | write / migrate                      | high                  | transaction + dry-run plan + fresh backup; staging first | L3 (L4 only with gate)     | wrapped in transaction w/ rollback; migration has a down-migration; backup age < N min; applied to staging before prod |
| 10   | Browser    | navigate / read (public)             | low                   | no stored credentials attached                           | L2                         | no authenticated session bound; destination ∈ domain allowlist |
| 11   | Browser    | authenticated action                 | high                  | non-prod tenant / sandbox account                        | L3                         | acting against non-prod tenant **or** explicit per-action human confirm; destructive/financial endpoints require L4 + human |
| 12   | Network    | outbound egress                      | medium (exfil)        | egress proxy + domain allowlist                          | L2                         | destination ∈ allowlist; payload scanned for secrets/PII before send |

## Missing facets this matrix exposes (feed back into the trust formula)

1. **Strategic value / upside** — the accelerator. Lets high-value work earn *investment
   in containment* rather than only earn more brakes. Without it the gate operationalizes
   caution, not strategy.
2. **Detection latency** — distinct from reversibility. "How fast will we know it broke"
   deserves its own term; a reversible-but-silent failure beats an irreversible-but-loud one
   in danger, not safety.
3. **Containment posture as input** — blast radius should be the *contained* radius, since
   containment is engineerable. Reward the posture; don't penalize the raw task.
4. **Actor competence / earned trust** — accrue trust to the *actor*, not just the task, so
   agents can graduate (Cagan's earned autonomy).
5. **Uncertainty / variance** — carry the spread, not just the mean. Route high-variance to a
   cheap probe (ephemeral wiki), not to default human escalation.

## Find-the-ledge protocol (calibration, not nerve)

- **Shadow autonomy:** run the agent at *floor + 1*, dry-run/proposal-capture only; log the
  would-be action; diff against human-approved ground truth. Promote the floor only after
  agreement on safe-calls crosses threshold (reuse the OVS drift-monitor calibration pattern).
- **Reversibility as budget:** treat snapshots / transactions / flags / undo logs as spend
  that moves the ledge outward — manufacture reversibility, don't merely score it.
- **Spend saved caution on Observe:** every second shaved off time-to-detect earns a notch
  of looseness at the gate. Loose gate + tight loop > tight gate + loose loop.
```

---

## End of source archive

Three this-session companion artifacts created on ingestion:
1. `Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md` — SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 (v1 synthesis + substrate blend + ratification gate)
2. `Core/frameworks/intent/spec/autonomy-gate-surface-matrix-v0-DRAFT.md` — SPEC-INTENT-AUTONOMY-SURFACE-MATRIX-001 (elevation of Artifact 3 to spec status)
3. `Core/frameworks/intent/tools/intent_signal_inventory.py` — v1 re-grounded to actual signal schema (MD frontmatter + closure-discipline DoD); v0 preserved at `intent_signal_inventory_v0.py`
