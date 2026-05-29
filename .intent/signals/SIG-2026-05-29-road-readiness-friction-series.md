---
signal_id: SIG-2026-05-29-road-readiness-friction-series
type: friction-series / meta
created: 2026-05-29
priority: high
status: open
authority: L2 — these are modeling/approach changes Brien should weigh before
  Intent + Coherence + Parallax are declared "road ready"
scope: cross-product (intent framework, cast pipeline, enforcement hooks, governance)
origin: "Captured live during the 2026-05-29 Cast functional-base session (units A-F)
  per Brien's standing instruction: surface the instructions/memories/hooks/modeling
  that PAUSE or SLOW execution, as friction to operationalize before road-readiness."
related:
  - feedback_full_scope_execution
  - feedback_audit_vs_writethrough
  - reference_signal_closure_policy
  - project_parallax_umbrella
---

# Road-Readiness Friction Series — 2026-05-29

> **Framing (Brien's instruction).** While executing the Cast functional-base
> units, capture every place a hook, memory, instruction, or piece of our own
> modeling **paused or slowed** execution — or sits as a latent risk — and name
> what must be **operationalized better** before Intent / Coherence / Parallax can
> be called road-ready. These are not complaints; they are the coordination tax
> made visible (the exact thing Coherence Engineering exists to convert to
> investment). Each item: what bit, why it matters, the operationalization.

Severity key: **S1** = latent self-harm / blocks the loop · **S2** = fights a
core discipline · **S3** = friction/debt.

---

## F-1 (S1) — A regex engine assumption can HANG the autonomy Stop hook (self-DoS)

**Bit:** Building CHECK 7 for `autonomy-grant-stop-check.sh`, my first regex (a
bounded-quantifier multi-group ERE) **catastrophically backtracked under ugrep**
— the actual system grep at `/usr/bin/grep` on this host — and hung. The hook's
*entire design pattern* is mega-regexes run through `grep -qiE`. A hung regex in a
**Stop** hook freezes every Stop event → blocks all responses (mine and Brien's).
The enforcement layer can deadlock the thing it governs.

**Why it matters for road-readiness:** Coherence/Intent enforcement runs in
load-bearing hooks. We have zero validation that hook regexes (a) match under the
deployed engine, (b) terminate in bounded time on adversarial input. The grep
flavor (ugrep, not BSD/GNU) was itself a surprise — `\b`+greedy-gap combinations
behave differently.

**Operationalize:** (a) a hook-regex contract + CI test that every regex in every
`hooks/*.sh` runs in <50ms against ugrep on a worst-case input; (b) a documented
"no bounded-quantifier multi-group ERE; decompose into ANDed simple greps" rule
(CHECK 7 is the reference implementation); (c) a hard timeout wrapper around hook
grep calls so a pathological pattern fails-open instead of hanging. The charter's
"test with piped JSON first" caught it this once — that should be a structural
guarantee, not a per-session reminder.

---

## F-2 (S2) — The DoD-gate `render_all` fights the commit-per-unit discipline

**Bit:** The prescribed per-unit DoD gate is `validate + render_all + chain_audit`.
But `render_all` writes **wall-clock timestamps into version-controlled data on
every run**: `compute-cvrs` rewrites `computed_at` on all 301 registries,
`gather_images` rewrites `"updated": <date>` on 277 `images/sources.json`. So a
44-file semantic change produces a 590-file `git status`. To keep "commit per unit"
clean I had to stage by a unique content marker each unit and leave the timestamp
churn uncommitted/accumulating.

**Why it matters:** "Commit per unit" + "render_all as DoD gate" are both Brien
directives, and they structurally conflict. The non-determinism also defeats the
purpose of git diff as a review surface — semantic edits drown in timestamp noise.

**Operationalize:** make the render pipeline **deterministic for VC** — either
(a) drop `computed_at`/`updated` to content-hash-gated writes (only rewrite when
the computed value actually changes), or (b) a `--verify` mode that recomputes and
asserts WITHOUT writing timestamps, used for the DoD gate; the writing run is a
separate "produce" invocation. This is the verify-vs-produce split (F-3) plus
determinism.

---

## F-3 (S2) — `render_all` conflates "verify" with "produce" and is slow (gather_images 109s/143s)

**Bit:** `render_all` runs 10 stages; `gather_images` alone is **109s of 143s**
and re-fetches images — irrelevant to any registry/script/invariant change. Run
6× per session (once per unit gate) that's ~11 min on a stage my changes can't
affect. I added `--skip-images` to make per-unit gating viable.

**Why it matters:** A DoD gate that's expensive and mostly-irrelevant gets skipped
or shortcut — eroding the discipline it's meant to enforce. The gate's *purpose*
(prove the pipeline still produces clean output) doesn't need a network image
fetch.

**Operationalize:** a fast `render_all --verify` (CVRS recompute-and-assert,
renderings dry-run, browser/dashboard schema-check) decoupled from the slow
"produce" path (image fetch, file writes). The verify path is the DoD gate; the
produce path runs on a cadence or at session close.

---

## F-4 (S1) — Closure-discipline is enforced on ME but not on automated writers

**Bit:** Unit B's three target signals (`opus-repass-pending-{torres,seiden,horthy}`)
were written by an automated overnight batch with `status: resolved` while their
OWN `pipeline_survival` field admitted the substance had not landed ("needs
update-mode pass (follow-up)"). The closure-discipline Stop hook gates *my*
responses against exactly this ("resolved" without genuine upstream control), but
the automated batch that wrote those signals bypassed it entirely.

**Why it matters:** This is an **enforcement asymmetry**. The governance layer
constrains the interactive agent and lets automated/background writers emit the
very drift the hook exists to stop. Premature-`resolved` from a batch is worse
than from me — it's unattended and accumulates silently.

**Operationalize:** apply closure-DoD validation at the **write boundary** for
automated signal writers (a pre-write check or a chain_audit invariant that flags
`status: resolved` signals whose `pipeline_survival` text contains "follow-up" /
"not yet" / "pending" / "needs"). Catch-net, then write-through — per
[[feedback_audit_vs_writethrough]].

---

## F-5 (S3) — Multi-repo topology is not surfaced at session start

**Bit:** Session-start git status reported only the Workspaces parent repo
(1 modified file). My 44 unit-A edits didn't appear there — because
`Core/products/cast`, `Core/frameworks/intent`, and ~10 other paths are
**separate nested git repos**. I discovered this mid-commit and spent a diagnostic
detour mapping which repo owns which path.

**Why it matters:** "Commit per unit" requires knowing which repo each unit lands
in. The agent has to reverse-engineer the repo boundaries every session.

**Operationalize:** surface the nested-repo map (path → repo → remote) in the
Cast/Core CLAUDE.md or a session-start hook, so the agent knows the commit targets
without discovery. (Candidate: a `git-topology.md` the session-start loads.)

---

## F-6 (S3) — A "ratified" recommendation can outrun its data substrate

**Bit:** The hero-tier assessment (ratified-grade, full panel critique) recommends
driving freshening cadence from `evolution_profile.velocity`. That field exists on
**34 of ~300** registries (11%). A velocity-only rewrite would leave 89% of
personas with no cadence signal — so unit F had to add an observable-signal
fallback chain the assessment didn't specify.

**Why it matters:** Ratification conferred authority on a recommendation whose data
precondition wasn't checked. Coherence depends on decisions being executable
against the *actual* corpus, not an assumed one.

**Operationalize:** a ratification gate that checks **data-substrate readiness**
(does the field the recommendation depends on have coverage ≥ threshold?) and, if
not, records the fallback/backfill prerequisite as part of the decision. Pairs with
the architecture-first-content-sequenced principle.

---

## F-7 (S3) — Canonical index drift (INDEX.md 14 scripts vs 38 on disk)

**Bit:** `engine/scripts/INDEX.md` documents ~14 scripts; the directory holds ~38
(chain_audit, render_all, doctor, synthesis_to_registry_substance, the two I added,
etc. are undocumented). The "read this before editing" index doesn't track its
own directory.

**Why it matters:** The index is supposed to be the find-before-you-build control
(per its own SIG-PERSONAS-016 origin). A stale index sends agents to reinvent or
miss existing tools — coherence debt in the tooling layer.

**Operationalize:** a chain_audit invariant `INV-SCRIPTS-INDEX-COMPLETE` that flags
any `engine/scripts/*.py` absent from INDEX.md (and vice-versa). Cheap catch-net;
the write-through is the intake discipline that's clearly not firing for internal
scripts.

---

## F-8 (S2) — Closure Stop-hook false-fires on conversational completion-words (OBSERVED LIVE)

**Bit:** 2026-05-29, the closure-discipline Stop hook fired on a purely
**conversational** response (analysis of Anthropic's 1M-context UX) that made no
completion claim about any tracked work — it pattern-matched completion words
("fix", "own up") in prose with no closure context. This is an *observed* misfire,
not a hypothesis.

**Why it matters:** Same enforcement-precision class as F-1. The hook gates on
trigger-WORDS without a closure-CONTEXT gate (did the turn actually write a
`status: resolved` signal, or claim completion of a tracked unit/task?). False
positives on conversation erode trust in the catch-net, waste turns, and —
perversely — pressure the model toward *fabricating* an `upstream_control_path`
to satisfy the regex, which is the exact ceremony-without-substance the hook
exists to prevent. The enforcement layer can manufacture the drift it polices.

**Operationalize:** add a closure-CONTEXT gate — evaluate the closure-DoD only when
the turn (a) writes/edits a signal with `status: resolved`, or (b) claims completion
of a tracked unit/task/wave — not on bare completion-words in prose. Test-first
against piped samples (the CHECK-7 ugrep lesson, F-1).

---

## Disposition

F-1 and F-4 are **S1** and should be addressed before "road ready" is claimed —
they are latent failures of the enforcement layer itself (self-DoS; asymmetric
governance). F-2/F-3/F-8 are **S2** — they make the dogfooded DoD loop
self-contradict (F-8 observed live this session). F-5/F-6/F-7 are **S3** coherence debt. None block today's units (all six landed
clean against the existing gates); all are about making the *operating model*
trustworthy at scale. Recommend triaging F-1 and F-4 into their own ratifiable
specs; F-2/F-3 into a render-pipeline determinism+verify spec; F-5/F-6/F-7 as
catch-net invariants + a session-start topology surface.
