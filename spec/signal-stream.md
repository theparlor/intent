---
title: Signal Stream
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
technologies:
  - jira
depth_score: 4
depth_signals:
  file_size_kb: 10.3
  content_chars: 9782
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.10
related_entities:
  - pair: consulting-operations ↔ teresa-torres
    count: 62
    strength: 0.087
  - pair: consulting-operations ↔ marty-cagan
    count: 62
    strength: 0.077
  - pair: consulting-operations ↔ subaru
    count: 44
    strength: 0.117
  - pair: consulting-operations ↔ slack
    count: 40
    strength: 0.12
  - pair: jira ↔ subaru
    count: 39
    strength: 0.235
---
# Signal Stream

> Observations captured from Intent's own development. Each signal has a confidence score, source, and related intents. This is what the observe layer looks like in practice.

## What Is a Signal?

A signal is an observation — something noticed during work, research, or conversation that may be worth acting on. Signals are the raw inputs to the Intent loop. They sit at the very top of the work ontology: before an intent is declared, before a spec is written, before anything is built.

Signals are not tasks. They're not tickets. They're evidence. Each one carries a confidence score (how sure are we this matters?), a source (where did this come from?), and links to related intents (what might we do about it?).

The signal stream is the Intent system's replacement for the traditional backlog. Instead of a prioritized list of work items that someone groomed in a meeting, signals flow in continuously from observation — and the team decides which ones to act on based on evidence, not ceremony.

## How Signals Work

Signals are stored as markdown files in `.intent/signals/` within each repo. They follow a naming convention: `YYYY-MM-DD-slug.md`. Each file contains frontmatter with structured metadata and a body with the observation narrative.

A signal can come from anywhere: a conversation with a user, a pattern noticed in agent execution traces, a competitive move, a failed contract assertion, or a gut feeling that something is off. The key discipline is writing it down — making the implicit explicit so the team can reason about it together.

## Current Signals

### SIG-001: Work needs a formal ontology
- **Confidence:** 0.92
- **Source:** Internal research
- **Related intents:** Intent positioning

Teams who've tried AI-augmented workflows consistently report that ticket-based coordination breaks down. The friction isn't execution — it's spec quality. This suggests a category shift, not an optimization within agile. Work needs a formal hierarchy: Signal → Intent → Spec → Contract → Capability → Feature → Product.

### SIG-002: OTel conventions apply to work, not just systems
- **Confidence:** 0.87
- **Source:** Implementation experience
- **Related intents:** Tech architecture

OpenTelemetry's trace/span/parent model maps directly to how work flows through teams. A trace is an Intent. A span is a work unit (spec, contract, capability). Parent-child relationships capture the hierarchy. This isn't a metaphor — it's a structural isomorphism that lets Intent events integrate with existing observability infrastructure.

### SIG-003: Conversations are signals, not noise
- **Confidence:** 0.79
- **Source:** Ari conversation, user feedback
- **Related intents:** GTM strategy, feature prioritization

When engineer Ari described how his team rewired around AI — tickets becoming bot specs, refinement becoming design sessions, PRDs moving outside Jira — that conversation was a signal. The insight wasn't just what he said, but that he'd arrived at Intent's core thesis independently. Conversations with practitioners are primary evidence, not anecdotes.

### SIG-004: The gap is bigger in larger teams
- **Confidence:** 0.85
- **Source:** Customer interviews
- **Related intents:** Audience targeting

Solo practitioners and small teams can collapse workflow locally. The pain multiplies in orgs where process coordination is the primary tax. Intent's value increases with org size. Three disciplines feel the shift differently: architects see efficiency gains, PMs see validation of discovery-hard thesis, designers see spec quality mattering.

### SIG-005: Work units need schemas before they need UIs
- **Confidence:** 0.88
- **Source:** Persona research, implementation experience
- **Related intents:** Positioning, tech architecture

Building a dashboard before defining what work units look like is premature. The schema is the product. Once signals, intents, specs, and contracts have stable schemas, visualization is straightforward. This is why Intent is file-native and git-tracked before it's a web app.

## Signal Lifecycle

Signals don't disappear. They either get linked to an intent (someone decided to act on it), get merged with another signal (same observation from a different angle), or get archived with a note explaining why the team chose not to act. The archive is valuable too — it records what the team noticed but deliberately chose to defer.

### Closure Criteria (added 2026-04-16 per SIG-046 / SIG-F-001)

A signal may transition to `status: resolved` ONLY when **one** of the following is true:

1. **Upstream control installed.** The recommendation in the signal's Implication / Proposed Resolution section has been implemented as a gate, policy, emission-helper, or DoD entry that will catch the next instance automatically. Evidence of the control (file path, DoD ID, spec ID) must be recorded in the signal's Resolution section.

2. **Explicitly deferred with rationale.** Set `status: deferred`, add `deferral_rationale:` (why the upstream fix isn't being built now), and `reassess_by:` (a date, not a vague condition). Deferred signals remain active in the governance view; they do not disappear.

**Intermediate state for symptom-only repairs:** If a defect has been repaired but the upstream control is NOT yet installed, use `status: symptom-repaired, upstream-pending`. This is a VISIBLE governance debt — it surfaces in overwatch and blocks "clean" closure reporting. It exists to prevent the premature-closure failure mode where running a one-time repair script looks like resolution.

> **Canonical spelling (WS-DDR-113, 2026-06-12):** the token is `symptom-repaired, upstream-pending` — comma + space, exactly. The run-on variant `symptom-repaired-upstream-pending` had diverged organically (26 files); the corpus was normalized to the comma form and `hooks/closure-discipline-signal-check.sh` now blocks new writes of the variant. One spelling keeps status greps and the two-bucket governance views trustworthy.

**Closure audit:** When a signal closes as `resolved`, the closer must answer:
- What is the upstream control? (gate / policy / DoD / emission discipline)
- Where does it live? (file path + ID)
- How would the same class of defect be caught if reintroduced? (test / lint / pre-commit hook / DoD validation)

If any answer is "N/A" or "we just fixed this instance," the correct status is `symptom-repaired, upstream-pending`, not `resolved`.

**Precedent — why this rule exists:** SIG-006 (persona-corpus YAML parse failures, 2026-04-08) was closed `resolved` after a repair script ran, even though its own Implication recommended a validation gate. The gate was never installed. The same class of defect recurred 8 days later as SIG-046 in a different file type. Discovery in SIG-F-001 found ~21 similar premature-closures across products (27% of all resolved signals). This rule is the meta-fix.

### Downstream-fix ⇒ upstream examination (added 2026-07-02 per SIG-2026-06-27)

When a signal records a **downstream / leaf fix of an upstream-originated drift** (a convention, contract, naming, or schema that changed at its source and left consumers bound to the old form), closing it as `resolved` REQUIRES one of:

- `triggers_upstream_examination:` — pointing at a sibling open signal that asks "what convention drifted to allow this, and what else is still bound to it?", **or**
- `upstream_examination: not-applicable` — with a one-line rationale (e.g. an isolated typo with no shared convention).

Without this, the correction-propagation reflex (fix the leaf → examine the source → find the other bound consumers) stays an operator habit rather than a mechanism, and the *next* consumer bound to the same dead convention degrades silently — exactly the ~2-month synthesis-glob drift that surfaced this rule.

**Enforcement:** `tools/closure_writeboundary_check.py` carries a write-boundary detector arm (`DOWNSTREAM-FIX-NO-UPSTREAM-SIGNAL`) that flags a `status: resolved` signal whose body uses downstream-fix framing but declares neither field. It is **date-scoped to signals dated on/after 2026-07-02** (zero-violation-start: legacy resolved signals are not retro-flagged). The upstream *sensor* that finds the other bound consumers is `tools/convention_migration_invariant.py` (Control A) reading `bound_consumers` / `forbidden_legacy_patterns` from port contracts.

## Schema v2: Flight-Model Input Fields (added 2026-05-26)

Per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 (`Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md`), forward signals SHOULD include flight-model input fields in their frontmatter to support λ calibration. These fields are **recommended, not required** — legacy signals are not retro-backfilled. The forthcoming `lambda_fit.py` tool will weight calibration-ready signals (those carrying these fields) higher than legacy signals (which use heuristic input derivation).

### Recommended frontmatter fields

```yaml
# Existing closure-discipline fields (required for status: resolved)
upstream_control_path: ...
catch_mechanism: ...
pipeline_survival: yes|no

# NEW — flight-model input fields (recommended for forward signals)
blast_radius: low|low-med|medium|high          # row-from-gate-matrix or qualitative
exposure: solo|engagement|cross-human|public   # who/how-many would be affected
irreversibility: 0.0-1.0                       # 0 = fully reversible, 1 = irreversible
strategic_value: 0.0-1.0                       # upside if the action succeeds (the accelerator)
containment_posture: |                         # the engineered lift
  - sandbox: yes
  - dry-run: yes
  - rollback-window: 24h
  - feature-flag: NAME or null
detection_speed: instant|minutes|hours|days    # how fast we'd know if it broke
autonomy_level: L0|L1|L2|L3|L4                 # the grant under which this action was taken
lambda_used: 0.0-3.0                           # the bravery coefficient at decision time
```

### Why these fields

The v1 trust formula's caution bias is structural: it measures only downside-of-failure and feasibility, never strategic value. The flight model adds value (Thrust), containment (Lift), and detection latency (Lift component) as first-class inputs. To calibrate the model from real history, signals must carry the inputs the model uses.

Legacy signals (pre-2026-05-26) lack these fields. The `lambda_fit.py` tool derives heuristic substitutes from existing fields (`severity` → blast_radius proxy, `type: catch-net-gap` → low-lift indicator, etc.) for the warm-start fit. Forward signals carrying explicit values reduce calibration noise.

### Backfill is optional and opportunistic

Existing signals do not require backfill. If a signal is being re-opened or substantively edited, the author MAY add these fields. Bulk backfill is **not** a closure-discipline requirement — the warm-start λ fit is acceptable with heuristic derivation, and forward instrumentation is the higher-leverage move.

### Schema enforcement

Schema validation lint (when it lands) will:
- WARN if a signal authored after 2026-06-01 lacks `blast_radius` or `strategic_value`
- NEVER block authorship — the recorder-was-optional failure mode is the larger risk
- EMIT a follow-up SIG- to track the gap, attaching it to the offending signal via `related:`

## Where Signals Live

- **Source files:** `.intent/signals/` in each Intent-native repo
- **Naming:** `YYYY-MM-DD-slug.md`
- **Event emitted:** `signal.created` (via GitHub Action on PR merge)
- **Site page:** rendered at theparlor/intent-site <!-- broken link removed: ../docs/signals.html (site moved to separate repo per CLAUDE.md; this repo has no docs/) -->
