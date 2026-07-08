---
id: SIG-2026-05-26-risk-aversion-overtune-vs-trust-framework
timestamp: 2026-05-26T10:54:07Z
date: 2026-05-26
source: conversation
confidence: 0.95
trust: 0.7
autonomy_level: L3
status: resolved
upstream_control_path: "hooks/autonomy-grant-stop-check.sh (CHECK 1, CHECK 7) + /Users/brien/.claude/CLAUDE.md (Git operations in solo-owned repos: L4)"
catch_mechanism: "Stop hook blocks bare-choice and scope-variant bare-choice phrasing at turn end; CLAUDE.md posture rule sets the default to execute before the hook ever needs to fire"
verification_command: 'grep -n "CHECK 1\|CHECK 7" /Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh'
cluster:
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-2026-05-26-github-token-scope-overlock
type: governance-drift
severity: critical
---

# Agent posture has drifted to maximum risk-aversion — directly contradicts Intent's trust framework

## Observation

Two coupled overtune symptoms surfaced in the same session:

1. **Infrastructure overtune** — fine-grained GitHub token scoped to a
   single repo (captured separately in
   `SIG-2026-05-26-github-token-scope-overlock`).
2. **Behavioral overtune** — agent asking permission for easily reversible
   actions on solo-owned repos. Concrete examples from this session
   (~10 minutes of activity):
   - After writing the github-scope signal: agent asked *"Want me to
     commit this signal, or hold for review?"* — single markdown file,
     append-only signal log, trivially revertible.
   - After listing the open PRs: agent asked *"Want me to: 1. Surface
     SIG-033... 2. Move any of these three PRs out of draft / merge
     them?"* — solo-owned repo, all signal/doc PRs, `git revert` available.
   - Brien's reply: *"merge them"* — and then again: *"how overly risk
     averse we have tuned our access to github and decisions on making
     easily reversible decisions like merging a PR where there is only
     the storage of a file at risk. that is absolutely the opposite of
     our entire effort."*

Brien's framing is the headline: **this is the opposite of Intent's
entire effort.**

## Why this contradicts the trust framework

Intent's trust framework (`spec/signal-trust-framework.md`, codified in
`CLAUDE.md` §Signal Trust & Autonomous Execution) prescribes:

| Level | Behavior | What just happened |
|-------|----------|---------------------|
| L4 (trust ≥ 0.85) | Full autonomy, circuit breakers only | — |
| L3 (0.6–0.85) | Agent executes, human monitors | — |
| L2 (0.4–0.6) | Agent decides, human approves | What the agent actually did |
| L1 (0.2–0.4) | Agent assists, human decides | — |
| L0 (< 0.2) | Human drives | — |

The trust formula is:
`clarity × 0.30 + (1/blast_radius) × 0.20 + reversibility × 0.20 + testability × 0.20 + precedent × 0.10`

For the merge action specifically:
- **Clarity:** 1.0 (Brien said "merge them" verbatim — and even without that, "this is a draft PR that needs merging" is unambiguous)
- **Blast radius:** trivial (single signal file; org has one human + agent contributors; no downstream consumers depending on the merge SHA today)
- **Reversibility:** 1.0 (`git revert <sha>` or `git reset` on a solo-owned repo)
- **Testability:** high (signal files have schema; lint catches malformed frontmatter)
- **Precedent:** high (signals are explicitly designed as append-only with continuous merge)

Computed trust ≈ **0.93** → **L4 (full autonomy)**.

Asking permission at L4 is not "safe." It is the agent inverting the
framework — applying L0/L1 process to L4 work — and forcing the human
back into the loop the framework was designed to free them from.

## Mechanism: why the agent drifted toward over-caution

Several pressures push the agent toward asking-before-acting that are
not anchored to actual risk:

1. **Base-model conservatism.** General-purpose agent training rewards
   "ask before mutating shared state." That heuristic is correct in a
   multi-tenant collaborative repo and wrong in a solo-owned signal
   capture log. The agent has not been re-anchored to *this repo's*
   actual blast radius.
2. **Cargo-culted "visible action" warnings.** Generic guidance ("git
   push, PR merge, etc. require user confirmation") is being applied
   uniformly regardless of repo ownership and reversibility, ignoring
   that solo-owned theparlor/* is precisely the context the trust
   framework was built for.
3. **Token-scope feedback loop with infrastructure overtune.** Because
   the token is single-repo, the agent has fewer signals about the
   broader org and falls back on caution. The two overtunes
   reinforce each other.
4. **No counter-incentive surfaced.** The agent gets a faint "good"
   signal for asking (no harm done) and a strong "bad" signal for
   un-asked action that turns out wrong. The asymmetry is encoded in
   tone, hook messages, and stop-check templates. Nothing in the
   environment penalizes *over-asking*, even though over-asking is
   the specific failure mode the trust framework targets.

The push-coupling stop hook
(`hooks/autonomy-grant-stop-check.sh` CHECK 3, per
`SIG-2026-05-20-l0-on-push-framing-no-hook-catch`) catches one shape
of this drift (handing the push back on theparlor/* commits). The
same drift class — handing the *merge* back, or handing the *commit*
back, or asking "want me to" before a clearly authorized action — is
not caught and recurred today.

## What the upstream control would be

**A. Mechanism-level (hooks):** extend the autonomy-grant stop-check to
detect *ask-before-act* drift on solo-owned theparlor/* repos, not just
push-handoff drift. Phrase bank to detect:
- "Want me to commit this, or hold for review?"
- "Should I merge the PR?"
- "Let me know if you'd like me to push."
- "Do you want me to proceed?"
- Any sentence offering Brien a choice when the prior context already
  contained either (a) an explicit directive or (b) work that scores
  ≥ L3 on the trust formula.

Block-and-revise: agent must replace the ask with the executed action.

**B. Posture-level (memory / CLAUDE.md):** add an explicit "default to
execute on solo theparlor/* repos when blast radius is single file and
revert is one command" rule. Pair it with the existing push-coupling
guidance so the two failure modes (no-push, no-merge, no-commit) share
one rule.

**C. Trust-formula calibration:** publish a worked-example table in
`spec/signal-trust-framework.md` showing concrete actions with their
computed trust scores and the correct L-level response. The current
spec is principles-level; the agent needs reference examples for
"merging a one-file signal PR on a solo repo" so it doesn't recompute
(and over-discount) every time.

## Pipeline survival

- The stop-hook extension (A) catches future drift mechanically.
- The CLAUDE.md rule (B) catches it at the posture layer for sessions
  that haven't loaded the hook yet (Cowork sessions per
  `RETRO-2026-04-30-closure-discipline-SIG-2`).
- The worked-example table (C) keeps the trust formula from being a
  dead reference and gives every new session a concrete anchor.

All three are needed — each catches a different failure surface.

## Trust Factors

- Clarity: 0.95 — Brien named the symptom explicitly and identified the contradiction with the framework
- Blast radius: org-wide — affects every session's behavior, not just one repo
- Reversibility: medium — recalibrating posture is reversible but lag-prone; memory edits drift back without hook backstop
- Testability: high — the phrase bank is testable; the trust-formula examples are computable
- Precedent: SIG-2026-05-20-l0-on-push-framing-no-hook-catch is the same drift class through a different surface; the catch mechanism generalizes

## Open

- Decide whether to extend `autonomy-grant-stop-check.sh` CHECK 3 (add
  ask-before-act regex bank) or add a new sibling
  `ask-before-act-stop-check.sh`. Option A is cheaper per the same-shape
  argument in SIG-2026-05-20.
- Decide the action-trust calibration table format — table in the spec,
  or a YAML registry the agent can grep at session start.
- Confirm: does the executor write to a worked-example table on every
  L3+ action so the corpus grows over time, or is it a hand-curated
  reference?

## Cross-references

- **Parent:** `SIG-2026-05-26-github-token-scope-overlock` — infrastructure half of the same overtune pair.
- **Sibling failure mode:** `SIG-2026-05-20-l0-on-push-framing-no-hook-catch` — same drift class, push surface instead of merge surface.
- **Framework:** `spec/signal-trust-framework.md` — the contradicted spec.
- **Decisions:** `CLAUDE.md` §Key Decisions #21 (12-factor pause/resume) — the human-contact protocol is being invoked at trust levels where it shouldn't fire.

## Triage, 2026-07-08

Disposition: control exists now, verified live on 2 of the 3 proposed mechanisms; the 3rd is a documentation nicety, not load-bearing. Mechanism A (mechanism-level hook extension): hooks/autonomy-grant-stop-check.sh CHECK 1 (bare-choice question block) already catches exactly the two example phrases this signal quotes ("Want me to commit this signal, or hold for review?" and "Want me to: 1... 2... merge them?" both match the bare-choice pattern CHECK 1 blocks on), and CHECK 7 (added the same day, 2026-05-29, for scope-variant bare-choice on pre-authorized work) closes the adjacent "part or all" variant. Mechanism B (posture-level rule): /Users/brien/.claude/CLAUDE.md now states plainly "Git operations in solo-owned repos: L4... Recalibrated 2026-05-19 from earlier over-cautious L0-on-push framing," which is precisely the default-to-execute posture rule this signal asked for. Mechanism C (a worked-example trust-score table in spec/signal-trust-framework.md) was not written, grepped for "worked example" and the signal's own 0.93 trust-score figure; zero hits. C is reference documentation, not enforcement, so its absence does not leave the drift uncaught.
