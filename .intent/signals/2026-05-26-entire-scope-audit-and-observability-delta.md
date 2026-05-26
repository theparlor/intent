---
id: SIG-ENTIRE-SCOPE-2026-05-26
timestamp: 2026-05-26T15:00:00Z
source: handoff-audit
author: brien
confidence: 0.92
trust: 0.85
autonomy_level: L4
status: active
cluster: observability-boundaries
parent_signal:
related_intents:
  - intent-observability-stack
  - witness-event-substrate
related_decisions:
  - DEC-007
audit_origin: handoff-2026-05-25-chat-session
phase: 1-of-2
target_phase_2: canonicalization-via-DDR-and-targeted-edits
---
# Entire.io scope audit — observability layer delta

> Phase 1 of a 2-phase audit triggered by the 2026-05-25 chat-session handoff. Phase 1 (this signal) owns the thinking. Phase 2 will canonicalize the corrections via a new DDR that supersedes DEC-007 plus 7 targeted doc edits. Surface deltas, then file.

## TL;DR

The hypothesis carried in the handoff confirms with a sharper edge.

**Entire.io is correctly scoped as authoring-side provenance** — agent-session trace capture (prompts → tool calls → files touched → commit, with intra-session checkpoints). Granularity = git commit. Capture window = during the agent session. **It is not the runtime-observability layer.**

The framework's *canonical spec surface* (`observe.html`, `observe/README.md`, `observations/`, `spec/observability-stack.md`, Witness positioning) already treats Entire correctly — as one of N event sources feeding `.intent/events/events.jsonl`. **The over-trust lives in the framework's dev-continuity language**: `CLAUDE.md` (the agent handoff entry point), `DEC-007` in the decision log ("Entire.io is the observability layer"), and propagated through the JSX artifacts that are rendered to the site.

The runtime half of the Observe leg is already specced and partially built: **OTel Collector + Grafana/Tempo/Mimir/Loki** (`observe/README.md` + `observe.html` + `spec/observability-stack.md`), routed through **`observations/`** for double-loop feedback, and federated through **Witness** for the cross-product event substrate. **Nothing structural needs to be invented — only the framing needs to be honest.**

The "two observabilities" distinction is real, publishable, and load-bearing for future framework users. Recommendation: ship it as a short framework-site post.

## What was audited & why

Triggered by Brien's 2026-05-25 chat-session handoff observation:

> "We actually pulled entire.io into the full Intent framework to cover early observability, but I suspect we did not pay enough attention and trusted it to be more and broader in nature."

Chat-side search could not surface the integration documentation. This Code-side audit was tasked with finding it, ground-truthing the framework's claims against Entire's actual capability surface, and naming the delta.

## Where Entire integration is documented (Phase 1, Task 1)

There is no single canonical "we integrated Entire" doc. The integration is distributed across three doc tiers:

**Spec tier (formal records):**
- `Core/frameworks/intent/spec/decision-log.md` DEC-007 (line 131) — "Entire.io is the observability layer that runs alongside all three"
- `Core/frameworks/intent/spec/intent-concept-brief.md` line 86 — "agent observability (Entire.io)" listed as one of three intellectual-foundation pillars
- `Core/frameworks/intent/spec/product-roadmap.md` line 156 — `.entire/settings.json` + `.entire/logs/` listed as Execute-phase asset (status: configured)
- `Core/frameworks/intent/spec/product-roadmap.md` lines 162, 172 — bridge-into-event-stream framing
- `Core/frameworks/intent/spec/product-roadmap.md` line 177 — **explicit OPEN question, never resolved**: "What's the right boundary between Intent's observability and tools like Entire.io that already instrument agent execution?"
- `Core/frameworks/intent/spec/SPEC_TEMPLATE.md` line 161 — template reference

**Dev-continuity tier (CLAUDE.md):**
- `Core/frameworks/intent/CLAUDE.md` line 132 — Persona table: "◉ AI Agent — Claude Code, GitHub Actions, **Entire.io**. Primary: Execute, Observe."
- `Core/frameworks/intent/CLAUDE.md` line 143 — Three-layer repo pattern: "`.entire/` — Observability (execution traces from Entire.io)"
- `Core/frameworks/intent/README.md` line 136 — "Entire.io → Spec feedback loop"

**Artifact tier (JSX interactives, rendered to the public site):**
- `intent-work-system.jsx` — lines 55, 260, 261, 276, 329, 419, 448, 464, 734
- `intent-native-repos.jsx` — lines 47, 90, 192, 274, 365, 391 (incl. "Entire.io closes the loop from execution back into the spec layer")
- `intent-event-catalog.jsx` — lines 167, 171, 186, 301, 304, 306, 536, 594, 624 (Phase 3 integration target + session-hook event source)
- `intent-product-roadmap.jsx` — lines 97, 102, 155

**Product tier (correct scoping — these stay):**
- `Core/products/witness/CONTEXT.md` — Entire listed as one of N event sources alongside `.intent/events/events.jsonl`, hook stderr, cron exhaust
- `Core/products/witness/docs/positioning.md` line 25 — "Entire.io execution traces" listed as one of five event-source conventions
- `Core/products/witness/.entire/config.yaml` — scopes Entire to "Agent reasoning traces during Witness development sessions" — authoring-side
- `Core/products/witness/engine/adapters/entire-io.py` — Witness adapter that reads Entire output into the event store
- `Core/products/_intake/2026-05-09-portfolio-coherence-uplift/witness-report.md` — PCU correctly treats Entire as one of six event-emitting surfaces

**Memory tier (stale, flagged for correction):**
- `memory/reference_entire_io.md` (31 days old) — says config dir is `Core/products/library-index/.entire/`. Wrong: actual config is at `Core/products/witness/.entire/config.yaml`. The `library-index/.entire/` path has no config subdir — only `logs/`, `metadata/`, `settings.json`, `tmp/`.

## Claims catalog & capability mapping (Phase 1, Tasks 2 + 3)

Each framework claim mapped against Entire's actual capability (per handoff Section 4 — README/landing page ground-truth, v0.6.1 May 2026):

| # | Claim | Source | Verdict | Notes |
|---|---|---|---|---|
| 1 | "Entire.io is **the observability layer**" | spec/decision-log.md L131 (DEC-007) | **Overclaim** | Entire is git-commit-grain authoring-trace capture. Runtime/post-deploy observability has no Entire dimension. |
| 2 | "agent observability (Entire.io)" as third intellectual-foundation pillar | spec/intent-concept-brief.md L86 | **Narrow term promoted to broad term** | Entire IS one form of agent observability (authoring traces). The framing implies it covers the full observability axis. |
| 3 | `.entire/` labeled "Observability" in three-layer repo pattern | CLAUDE.md L143 | **Mis-scoped label** | Directory contents are correct (Entire's session traces). Label "Observability" overscopes role. Compare to `observations/` which actually IS the runtime-observability directory and is separate. |
| 4 | AI Agent persona = "Claude Code, GitHub Actions, Entire.io" | CLAUDE.md L132 | **Category collision** | Claude Code + GitHub Actions execute. Entire records the execution. It is not an agent; it is a session recorder. |
| 5 | Entire.io as Tier 0 of Intent adoption | intent-native-repos.jsx L192, L365 | **Supported AS authoring provenance** | "Just Entire.io enabled" gives real value: cheap, immediate, "how did this code get written" provenance without requiring `.intent/` scaffolding. Tier 0 framing is correct *if* scoped to authoring provenance. |
| 6 | "Entire.io closes the loop from execution back into the spec layer" | intent-native-repos.jsx L391 | **Overclaim** | Entire records how code was *written*. It does not measure whether the resulting code did what it was supposed to do once running. Loop closure (Observe→Notice) per observe.html requires the OTel/Grafana runtime stack — Entire is one input to that stack, not the closure mechanism. |
| 7 | "Agent reads Entire.io traces after every execution" → Observe-cycle input | intent-work-system.jsx L734 | **Partial** | Reading the authoring trace tells you what the agent intended and did. It does not tell you whether the artifact works in production. Authoring trace ≠ runtime telemetry. |
| 8 | Entire.io as Observe-phase input (alongside "metrics, user signals") | intent-work-system.jsx L419, L464 | **Mis-prioritized** | Entire is one input among many. Framing implies primary input. |
| 9 | Signal example: "Entire.io trace shows 3 failed auth attempts in deploy pipeline" | intent-work-system.jsx L55 | **Mis-scoped example** | Entire captures the engineer-agent's *session* investigating the deploy pipeline. It does NOT directly observe the deploy pipeline. Example conflates session-trace with deployment-telemetry. |
| 10 | "Entire.io agent trace capture ✅ Configured" under Execute-phase assets | spec/product-roadmap.md L156 | **Correct** | This is the right home: Execute-phase asset, configured, providing authoring trace for what agents did during build. |
| 11 | Open question: "What's the right boundary between Intent's observability and tools like Entire.io?" | spec/product-roadmap.md L177 | **Filed open. Never resolved.** | This audit IS the de facto resolution. |

## The named delta (Phase 1, Task 4)

The handoff Section 3 working metaphor holds and sharpens:

|                          | Entire                                                                                                        | Intent's Observe leg (as architected)                                                                                                                            |
|--------------------------|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **What it observes**     | The *authoring* path: prompt → response → files touched → commit. Provenance of how the code got written.     | The *running-system* path: runtime metrics, contract assertion pass/fail, latency distributions, trust-score drift, signal-source distribution, spec-vs-actual deltas. |
| **Plane**                | Cockpit / keystroke-to-commit                                                                                  | Aircraft telemetry / commit-to-reality                                                                                                                            |
| **Granularity**          | One agent session (`YYYY-MM-DD-<UUID>`), one commit, intra-session checkpoints (12-char hex)                  | One trace, one span, one metric sample, one log line                                                                                                              |
| **Implementation**       | `entire` CLI v0.6.1 (Homebrew binary), shadow git branch `entire/checkpoints/v1`, post-session hook            | OTel Collector + Grafana/Tempo/Mimir/Loki, `observations/` runtime-feedback directory, intent-observe MCP server (port 8003), Witness federating substrate         |
| **Capture window**       | During agent session                                                                                          | During code execution in production                                                                                                                              |
| **Outcome verification?**| **No** — records what the agent did, not whether it worked                                                    | **Yes** — contract assertions, metric thresholds, incident catalog                                                                                                |

**The over-trust pattern:** Entire was correctly identified as cheap, immediate, Tier-0 authoring-provenance value (✅). Then in the framework's internal documentation (CLAUDE.md, DEC-007, intent-concept-brief.md as "third pillar"), Entire was promoted from "authoring provenance" to "the observability layer." The runtime-observability mechanism (OTel/Grafana/Tempo) was specced *separately* in `observe/README.md` + `observe.html`, without flagging that the earlier "Entire as observability layer" framing was now structurally wrong.

**Result:** the canon-on-the-rendered-page (Observe leg surface) is honest and OTel-native. The canon-in-the-CLAUDE.md is over-scoped. New readers entering through CLAUDE.md (which IS the agent-handoff entry point) absorb the over-trust framing first.

## Recommended re-scope (Phase 1, Task 5)

### (a) The honest scope for Entire inside Intent

**Entire.io = authoring-side provenance.** Captures the agent-session path that produced each commit (prompts, tool calls, files touched, transcripts, token usage). Granularity = git commit + intra-session checkpoints. Capture window = during the agent session.

**Entire is one of N event sources feeding `.intent/events/events.jsonl`.** It is correctly positioned as a Tier 0 adoption mechanism for new repos (cheap, immediate, requires no `.intent/` scaffolding) — but Tier 0 value is *provenance*, not *observability*.

**Entire is not the Observe leg of the Intent loop.** It is not the runtime-telemetry mechanism. It is not the loop-closure mechanism. It feeds inputs to those mechanisms.

### (b) What owns the runtime half of Observe (the role wrongly attributed to Entire)

**The architecture is already in place; only the framing is mis-attributed.**

- **`Core/frameworks/intent/observe/`** — OTel Collector pipeline + adapters (`file-tail.py` tails `events.jsonl` and emits OTel spans). README is explicit: "OTel-native distributed tracing for the Intent loop. Connects the event system to Grafana via OpenTelemetry Collector." **This is the runtime-observability mechanism.**
- **`Core/frameworks/intent/observe.html` (rendered framework page)** — describes the Grafana dashboard with five panels (cycle-time histogram, signal source distribution, trust-score distribution, contract assertion pass/fail, signal clustering trends). **This is the human-facing surface of runtime observability.**
- **`Core/frameworks/intent/observations/`** — the runtime-feedback directory (`metrics/`, `incidents/`) with double-loop semantics (Flow 5 → knowledge base updates; Flow 6 → spec corpus updates). **This is where Observe-leg findings persist.**
- **`Core/frameworks/intent/spec/observability-stack.md`** — the full architecture spec (referenced from content-map.md as the source-of-truth for observability claims across 7 site pages).
- **`Core/products/witness/`** — the federating event-substrate that ingests all sources (Entire, hook stderr, `.intent/events/events.jsonl`, cron exhaust, Cortège fetch traces, library-index health summaries) and promotes patterns to signals with preserved lineage.

**Composition:** Entire session → `.intent/events/events.jsonl` (via session-hook adapter) → OTel Collector (via `observe/adapters/file-tail.py`) → Grafana/Tempo/Mimir/Loki. **Entire feeds the runtime stack; it does not replace it.**

## Phase 2 canonicalization handoff list

Concrete edits required (all L4 reversible local writes — Workspaces-local, no external surface). Recommended for Sonnet sub-agent dispatch per model-economy guidance (mechanical filing work; Phase 1 owned the thinking):

1. **`Core/frameworks/intent/spec/decision-log.md` DEC-007 (line 131)** — supersede with a new DDR. Old: "Entire.io is the observability layer that runs alongside all three." New: "Entire.io is the authoring-provenance recorder that runs alongside all three. Runtime observability is owned by the OTel/Grafana stack (`observe/`) and the `observations/` runtime-feedback directory." Frame the new DDR with explicit `superseded_by:` link back to DEC-007.

2. **`Core/frameworks/intent/CLAUDE.md` line 143** — change "`.entire/` — Observability (execution traces from Entire.io)" → "`.entire/` — Authoring provenance (agent-session traces from Entire.io). One source feeding `.intent/events/events.jsonl`."

3. **`Core/frameworks/intent/CLAUDE.md` line 132 (Persona table)** — separate Entire from Claude Code + GitHub Actions. Suggested: re-cast AI Agent persona to "Claude Code, GitHub Actions" and add a separate line in the same section: "Authoring Provenance Sources: Entire.io session traces, Granola transcripts, session-ledger md."

4. **`Core/frameworks/intent/spec/intent-concept-brief.md` line 86** — change "agent observability (Entire.io)" → "agent authoring provenance (Entire.io)". Optionally shift the third-pillar anchor to "runtime observability (OpenTelemetry/Grafana)" and reference Entire elsewhere as a session-trace input.

5. **`Core/frameworks/intent/spec/product-roadmap.md` line 177 (open question)** — resolve and remove from the open-questions block. Move resolution into product-roadmap narrative: "Entire records authoring-side provenance; Intent's runtime observability is OTel/Grafana via `observe/`. Entire is one event source feeding `events.jsonl` (Witness adapter); it does not duplicate or replace the runtime stack."

6. **`Core/frameworks/intent/artifacts/intent-work-system.jsx`** — fix mis-scoped examples at lines 55, 419, 464, 734. The "3 failed auth attempts in deploy pipeline" example should source from production metrics, not an Entire trace. The "Agent reads Entire.io traces after every execution" → Observe-cycle line should be rephrased: "Agent reads Entire.io traces to understand the authoring path; reads OTel-emitted runtime metrics to understand the outcome."

7. **`Core/frameworks/intent/artifacts/intent-native-repos.jsx` line 391** — change "Entire.io closes the loop from execution back into the spec layer" → "Entire.io seeds the loop by capturing authoring provenance; the loop closes at the Observe leg via runtime telemetry plus signal promotion."

8. **`memory/reference_entire_io.md`** — update stale config path. Current: "Config dir: `Core/products/library-index/.entire/`." Actual: `Core/products/witness/.entire/config.yaml`. Multiple `.entire/` directories exist (Witness owns Entire integration as a federating consumer; Intent framework's own `.entire/` is for the framework's own development).

## Pause-and-surface check (Phase 1, Task 6)

One material delta to the handoff framing is worth flagging:

The over-trust does **not** live in the canonical Observe-leg spec or in the rendered `observe.html` — those are correctly OTel-native. The over-trust lives specifically in **DEC-007**, in **CLAUDE.md** (the agent-handoff entry point), and in the JSX artifacts that propagate from the dev-continuity surface to the public site.

This is a narrower failure mode than "we built the framework on a bad assumption." The framework architecture is sound. The framework's *agent-context surface* over-attributes one of its sources. Phase 2 fixes 7 specific files; the runtime stack and `observe.html` do not need structural changes.

## Open decisions for Brien (from handoff Section 9)

These are L0/L1 decisions Brien sets — surfacing for the next decision-window:

1. **Is "authoring provenance" the right scoped role for Entire, or narrower?** Recommendation: keep at "authoring provenance" — narrower than "observability" but wide enough to preserve Tier 0 adoption value (provenance is a legitimate input to `.intent/events/events.jsonl`). Narrowing further (e.g., "Execute-phase session-recovery only") loses real value.

2. **Substrate exposure (handoff Section 6) — read-only vs. read/write priority?** Out of Phase 1 scope. Recommendation: read-only first (lower cost, fast win, no auth/conflict complexity); write-back as second milestone.

3. **Hosting question — always-on endpoint vs. desktop-resident?** Out of Phase 1 scope. The constraint crux per the handoff; the Max-subscription / routing-restriction constraints (April 2026) are the binding gate.

4. **Publish the "two observabilities" distinction?** Recommendation: yes, as a short framework-site post. The distinction is clean, useful to practitioners who confuse session-trace with runtime-telemetry, and frames the OTel/Entire boundary correctly without exposing the over-trust mistake. The cockpit/aircraft metaphor is the publishable hook.

## Out of Phase 1 scope (deferred)

The cross-surface substrate exposure problem (handoff Section 6) is a separate architectural track. Phase 1 of THAT track produces design-question answers, the architecture brief naming the exposure mechanism (MCP-front vs. repo-as-truth), and the desktop explicitly recast as a reader. Phase 1 of the Entire audit does not block on it. Phase 2 canonicalization can proceed independently.

## Verification on next render

If `Core/frameworks/intent/` gets a `render_all` pass before Phase 2 lands, this audit's findings survive because the deliverable lives in `.intent/signals/` — the framework's canonical signal stream, read by every framework-level audit. Phase 2 fixes will land in canonical spec + CLAUDE.md surfaces and survive their own render pipelines (which propagate downstream to intent-site via the content-map.md mapping).

---

*Phase 1 complete. Phase 2 awaits Brien's confirmation of the recommended re-scope, then mechanical canonicalization across the 7 named files + memory update. Recommended dispatch: Sonnet sub-agent with this signal as the brief.*
