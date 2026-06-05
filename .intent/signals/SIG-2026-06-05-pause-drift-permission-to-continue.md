---
id: SIG-2026-06-05-pause-drift-permission-to-continue
type: signal
status: open
severity: behavioral
created: 2026-06-05
target: autonomy-grant enforcement — the "pause for permission to continue" drift pattern
discovered_during: "Gauntlet v1 ship. I ended two consecutive responses with 'Recommended next move (when you want it)' / 'Standing recommendation unchanged ... when you want it' for the independent rung. Brien: 'fire away, we have plenty of budget ... record signal to better understand more about when and why you pause for permission to continue.'"
requested_by: brien
upstream_control_path: "PENDING — candidate hook enhancement to Core/frameworks/intent/hooks/ (the Stop-hook family that already blocks bare-choice questions). The existing autonomy-grant Stop hook catches 'A or B?' bare-choice framing; it does NOT reliably catch SOFT-QUEUE framing ('recommended next move, when you want it' / 'standing recommendation' / 'let me know'). That gap is the upstream control to build."
catch_mechanism: "PARTIAL today — autonomy-grant-drift-detector skill + the autonomy-grant Stop hook fire on bare-choice and 'would you like me to'. This signal documents the soft-queue variant they under-catch. The sharpened sub-rule below (the bundling rule) is the human-readable control until the hook is extended."
pipeline_survival: "n/a (behavioral signal); the rule survives as memory + hook once the hook is extended."
reconsider_when:
  - "soft-queue framing ('when you want it' / 'standing recommendation' / 'the natural next step would be') recurs after this signal -> build the hook enhancement (Layer-4 Stop pattern-match on soft-queue phrases lacking a same-turn execution of the L4 portion)."
  - "a recommended next step is genuinely irreducible (no L4-buildable increment, the WHOLE thing is gated) -> then surfacing-and-waiting is correct, not drift; do not over-correct into executing gated work."
---
# When and why I pause for permission — the worked example + the taxonomy

Brien asked me to understand my own pausing. Here is the honest analysis of the instance that triggered it, then the general taxonomy.

## The instance
After shipping Gauntlet v1, I twice ended with: *"Recommended next move (when you want it): build the independent rung..."* and *"Standing recommendation unchanged ... when you want it."* That is proposal-framing + queuing — asking, implicitly, for permission to continue.

## The 4-gate, applied honestly to "build the independent rung"
1. **Reversible?** Yes — new code in a solo repo, fully revertible.
2. **Local blast?** *Split.* The fresh-context-judge adapter is fully local. The DeepEval variant needs an external API key. The human-peer variant routes to a human (**L0**).
3. **Precedent?** Yes — the rung is named in the approved Gauntlet spec (`independence ladder`, `reconsider_when`, the v2 deferred list). The build was already authorized.
4. **Info gap?** *Split.* No gap for the fresh-context variant. A real gap only for the vendor-external variant (which framework / whose key?) and the human variant (opt-in).

**Verdict:** the L4-buildable increment (a fresh-context independent judge behind the existing eval-port ABC) passed all four gates → it should have been **executed in-turn**. Only the vendor-external / human variant carried a real gate.

## The specific failure mode: BUNDLING
The next step was **decomposable**: an L4 core (fresh-context judge — no key, no human) + a gated tail (DeepEval key / human opt-in). I collapsed both into one "when you want it" and queued the whole thing. A gated tail held the executable head hostage.

## The taxonomy (the durable takeaway)

**Legitimate pause — surface the SPECIFIC gate, then stop on that one thing:**
- Irreversible / destructive (force-push main, delete, overwrite-without-surface).
- External side-effect requiring a credential or new paid dependency (API key, money).
- Cross-human routing — Slack/email/PR-with-reviewers/calendar-with-attendees (**L0**).
- A genuine info gap only Brien can fill.
- A real either/or design fork whose branches diverge materially and irreversibly.

**Drift pause — should have executed + signalled:**
- Reversible + local + precedented + no-info-gap work framed as "recommended / when you want it / standing recommendation / let me know / the natural next step."
- **Bundling**: queuing an executable increment because *part* of the larger arc is gated.
- Stopping at "natural completion" while an L4 backlog remains.

## The sharpened rule (the correction)
**When a recommended next step decomposes into an L4-buildable increment + a gated remainder, execute the increment in-turn and surface ONLY the remainder's specific gate. Never queue the whole thing because part of it is gated.** Don't let a gated tail hold the executable head hostage.

## Why the existing hook under-caught this
The autonomy-grant Stop hook blocks **bare-choice** ("A or B?") and "would you like me to". This was neither — it was **soft-queue** ("recommended, when you want it"). Same drift, different surface form. The upstream fix is to extend the Stop pattern to soft-queue phrases that appear without a same-turn execution of the L4 portion (see `upstream_control_path`).

## Corrective action taken this turn
Per Brien's "fire away": executing the L4 increment now — a fresh-context independent eval-judge adapter behind `engine/eval_port.py` — and surfacing only the genuine remaining gate (vendor-external DeepEval key / human-peer opt-in) as a specific decision, not a blanket pause.
