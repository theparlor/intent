---
id: SIG-2026-07-04-stop-array-paraphrase-ceiling-ungoverned
created: 2026-07-04
type: signal
status: captured
severity: medium
confidence: 0.85
trust: 0.6
autonomy: L4
decision_owner: none required today. Naming an extension option is sufficient; ratifying which option ships is Brien's call whenever this is picked up.
related:
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md
  - Core/frameworks/intent/.intent/signals/SIG-2026-07-03-autonomy-grant-pause-drift-audit.md
  - Core/frameworks/intent/.intent/signals/SIG-2026-07-03-layer42-recall-unmeasured.md
  - ~/.claude/hooks/link-format-stop-check.sh
  - ~/.claude/hooks/presend-assertion-check.sh
  - ~/.claude/hooks/engagement-signal-cadence-check.sh
  - ~/.claude/hooks/forge-signal-cadence-stop-check.sh
  - ~/.claude/settings.json
upstream_control_path: "NONE TODAY. lexical-layer-freeze.yaml only names autonomy-grant-stop-check.sh and closure-discipline-stop-check.sh in its baseline and closure_discipline blocks; drag_dashboard.py's cap-guard (frozen_at_check comparison) has no reference to the other four Stop-array entries at all, so none of their growth is measured, capped, or flagged as ACCRETION-DRIFT regardless of how many CHECK-style variants they accumulate."
catch_mechanism: "NONE TODAY. No test, invariant, or dashboard section currently asserts that link-format-stop-check.sh, presend-assertion-check.sh, engagement-signal-cadence-check.sh, or forge-signal-cadence-stop-check.sh stay at a bounded pattern count. A future CHECK-1-style patch to any of the four would land silently."
pipeline_survival: "yes: this signal file persists under .intent/signals/ and is discoverable by the standard signal sweep (session-start overwatch, reckoning, scout) the same as any other signal in this directory. It does not depend on any code path surviving."
---

# Four Stop-array hooks share the frozen lexical layer's shape but sit outside its cap discipline

## Finding

`Core/frameworks/intent/hooks/lexical-layer-freeze.yaml` freezes exactly two hooks:
`autonomy-grant-stop-check.sh` (baseline, frozen at CHECK 7, 2026-05-29) and
`closure-discipline-stop-check.sh` (companion, same freeze, `closure_discipline` block).
Its own rationale (lines 17-26 of the yaml) is explicit about why: the lexical
approach grew CHECK 1 through CHECK 7 in one month, each CHECK a reaction to a
linguistic variant the prior CHECK missed, and the yaml states outright that
"the lexical approach cannot converge." The cap mechanism, enforced by
`drag_dashboard.py`'s `sanctioned_additions` block-guard (lines 50-52, 56-63),
exists specifically so no new CHECK ships without a Drag-budget debit and a
named sunset clause tied to the Layer 4.2 structural successor.

Four other hooks registered in the same Stop array in `/Users/brien/.claude/settings.json`
(lines 171-199) share the identical architectural shape, reactive regex-on-prose
matching applied to the transcript's last assistant-message text at Stop time,
but none of them appears anywhere in `lexical-layer-freeze.yaml`. Each already
shows the same iteration signature the freeze was written to stop:

- **`~/.claude/hooks/link-format-stop-check.sh`** (129 lines; source-of-truth copy
  does not exist in `Core/frameworks/intent/hooks/`, live copy only). Lines 83-94
  define four separate regex patterns (`anchor_local`, `anchor_ext`,
  `backtick_abs`, `bare_rel`, `tilde_path`) matched against `prose` (the
  fenced-code-stripped transcript text, line 81). The header comment at lines
  20-21 states this is already a second-generation fix: "Created 2026-06-04
  after the 3rd recurrence (06-01/06-02/06-04). Memory existed and did not
  hold -> mechanism-level fix." Line 88's comment documents a prior regex
  revision made 2026-06-10 after a false-positive was caught in session
  `ed280c22`, the same iterate-on-bypass pattern as the frozen CHECK series.

- **`Core/frameworks/intent/hooks/presend-assertion-check.sh`** (130 lines;
  source-of-truth copy exists, mirrors the live copy). Lines 103 and 107 define
  `SEND_RE` and `AUDIT_RE`, two hand-maintained alternation regexes matched
  against `LOWER_FULL` (the lowercased last-assistant-message text, line 99),
  and line 120 blocks only when the send-marker regex matches and the
  audit-marker regex does not. The header (lines 22-25) states the design is
  "conservative by design: suppresses ONLY on an explicit assertion-audit
  marker... Errs toward firing," the same posture that, for the autonomy-grant
  hook, produced seven successive CHECKs as users found unmatched phrasings.

- **`~/.claude/hooks/engagement-signal-cadence-check.sh`** (181 lines; no
  source-of-truth copy in `Core/frameworks/intent/hooks/`). Not a prose-regex
  match like the other three, it counts Write/Edit `tool_use` file paths
  (lines 84-119) against a watchlist threshold, so its detection surface is
  structural rather than lexical. Included here because it is registered in
  the same Stop array and its own header (line 29) explicitly states "Pattern
  mirrors: autonomy-grant-stop-check.sh, closure-discipline-stop-check.sh,"
  i.e., its author already treats it as a sibling of the frozen hooks, even
  though its detection mechanism is not itself a paraphrase-vulnerable
  regex-on-prose match. Flagged for completeness per the task's naming, not
  because it independently exhibits the paraphrase-ceiling failure mode.

- **`~/.claude/hooks/forge-signal-cadence-stop-check.sh`** (243 lines; no
  source-of-truth copy in `Core/frameworks/intent/hooks/`). Same
  tool_use-attribution shape as the engagement-signal hook (lines 156-190
  scan transcript `tool_use` records for Edit/Write/MultiEdit/NotebookEdit
  under `Core/products/forge/`), not a prose regex. Its header (line 40)
  states "Pattern mirrors: engagement-signal-cadence-check.sh,
  closure-discipline-stop-check.sh," again self-identifying as part of the
  same hook family the freeze was written to govern, and its changelog
  (lines 38-39) shows one full rewrite already ("Rewritten 2026-05-31: mtime
  walk -> transcript tool_use attribution") after a documented false-positive
  class. Flagged for the same completeness reason as the engagement hook.

Two of the four (`link-format-stop-check.sh`, `presend-assertion-check.sh`)
are prose-regex Stop hooks in the exact shape the freeze's rationale
describes: hand-maintained alternation patterns matched against the last
assistant message, already mid-iteration (a documented false-positive fix on
`link-format-stop-check.sh` 2026-06-10; a deliberately conservative,
known-to-underfire posture on `presend-assertion-check.sh`). The other two
(`engagement-signal-cadence-check.sh`, `forge-signal-cadence-stop-check.sh`)
are structural tool_use-attribution checks, not paraphrase-vulnerable prose
matchers, but sit in the same Stop array, self-declare as siblings of the
frozen hooks in their own header comments, and carry no growth cap either.

## Why it matters

The freeze exists because unbounded CHECK accretion on a single lexical hook
was explicitly diagnosed as unconvergeable and a real drag cost
(`lexical-layer-freeze.yaml` lines 17-26; corroborated independently by the
2026-07-03 audit's root cause 2, `Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md`
lines 33). That diagnosis is generic to the mechanism (regex-on-prose at Stop
time), not specific to the autonomy-grant hook's subject matter. Two of the
four hooks named here use the identical mechanism and already show the same
early iteration signature (a 2026-06-04 rewrite plus a 2026-06-10 regex fix on
`link-format-stop-check.sh`; a self-described error-toward-firing posture on
`presend-assertion-check.sh`) that, on the autonomy-grant hook, took five weeks
to reach seven CHECKs and a formal freeze. Without a cap or a named structural
successor, each of these four is a candidate for the same whack-a-mole growth
the freeze was written to prevent, and none of it would currently register on
`drag_dashboard.py`'s cap-guard, because that guard only inspects the two
hooks named in the yaml's `baseline` and `closure_discipline` blocks.

This is a governance-layer gap of the same kind root cause 5 in the 2026-07-03
audit names for the autonomy-grant hook mechanism generally (spec lines 39):
"never modeled... as a governed artifact" until adversarially tested. These
four hooks have not yet been adversarially tested or measured at all, only
observed here to share the frozen layer's shape.

## Recommendation (naming only, not implemented)

Two options, either sufficient to close the gap; neither implemented as part
of this signal:

1. **Extend `lexical-layer-freeze.yaml`'s existing cap discipline** to cover
   all four hooks by adding entries alongside the current `baseline` and
   `closure_discipline` blocks (or a new `stop_array_prose_hooks` block for
   the two genuinely lexical ones), so `drag_dashboard.py`'s cap-guard
   inspects their CHECK/pattern counts too and flags ACCRETION-DRIFT the same
   way it does for the frozen pair.
2. **Write per-hook freeze entries** as standalone sibling YAML files (or a
   single multi-hook freeze registry) if the four hooks' growth patterns
   don't map cleanly onto the existing `baseline`/`closure_discipline` schema,
   preserving the same `rule.no_new_check_without` discipline (drag budget
   debit, sunset clause, flight-model cross-reference) per hook.

Either path should distinguish the two genuinely prose-regex hooks
(`link-format-stop-check.sh`, `presend-assertion-check.sh`, the real
paraphrase-ceiling candidates) from the two tool_use-attribution hooks
(`engagement-signal-cadence-check.sh`, `forge-signal-cadence-stop-check.sh`,
structurally different detection, no regex-on-prose exposure) so the cap
discipline is applied to the actual failure mode rather than uniformly by
Stop-array membership alone.

No hook file, the freeze yaml, or `drag_dashboard.py` was edited to produce
this signal. Signal only.

## Triage, 2026-07-08

Disposition: still pending, Brien-gated (unchanged). Confirmed neither option
has been implemented: `lexical-layer-freeze.yaml` still names only
`autonomy-grant-stop-check.sh` and `closure-discipline-stop-check.sh`, with
no new block for the four hooks this signal named. This signal's own
`decision_owner` field states ratifying which extension option ships is
Brien's call; deliberately not implementing either option in this pass, both
because that is an explicit deferral in the signal itself and because doing
so would mean editing the frozen lexical layer during the active Layer 4.2
calibration window (see the companion 2026-07-03 audit signal, same
directory).
