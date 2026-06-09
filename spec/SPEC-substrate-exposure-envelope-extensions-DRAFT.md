---
title: Substrate-Exposure Envelope & Verb Extensions (D1–D4)
type: spec
maturity: draft
confidentiality: internal
reusability: specific
created: 2026-05-31
updated: 2026-05-31
depth_score: 4
depth_signals:
  file_size_kb: 14.8
  content_chars: 13697
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.07
status: draft
ratification_state: "RATIFIED + BUILT 2026-05-31 — all five deltas approved (D2 override = entity frontmatter, Open Q1 closed) AND implemented in servers/knowledge.py (commit 5ca8566); servers/test_knowledge.py green at 56 tests (run via servers/.venv). Recorded in decision-log.md DEC-012. Remaining Execute step: deploy to intent-knowledge.fastmcp.cloud (Brien-driven)."
vocabulary_state: reconciled to our canon 2026-05-31 — see §0 (intentionally divergent from the validating category)
extends: substrate-exposure-architecture.md
target: Core/frameworks/intent/servers/knowledge.py
source_signals:
  - SIG-2026-05-31-personal-synthesis-layer-commoditizing
  - SIG-2026-05-31-personal-memory-altitude-mismatch
  - SIG-2026-05-31-verbatim-passthrough-differentiator
  - SIG-2026-05-31-exposed-vocabulary-divergence-principle
related_decisions:
  - WS-DDR-099 (substrate exposure mechanism — MCP-front + repo-as-truth)
  - DEC-010 (intent-knowledge MCP scope extension — current verb set)
  - DEC-009 (two observabilities)
---
# Substrate-Exposure Envelope & Verb Extensions (D1–D4)

> Four validation-driven refinements to the `intent-knowledge` MCP envelope + verb set, plus a
> preservation invariant. These sharpen the **spine's interface** (the defensible surface per the
> S1–S3 synthesis) — they are not a new memory engine.

> ## ✅ RATIFIED + BUILT 2026-05-31
> Brien ratified all five deltas via decision surface on 2026-05-31 — D1/D3/D4 + `preservation_invariant`
> (low-risk) and **D2** (the schema change), with **D2's override surface = entity frontmatter**
> (closes Open Q1). Recorded in `spec/decision-log.md` **DEC-012** (DEC-010 carries a forward pointer).
> **Built + tested 2026-05-31 (TDD):** D1–D4 + `preservation_invariant` implemented in
> `servers/knowledge.py` (new verbs `get_core`/`audit_chain`; new envelope fields `sightline`/`supply_policy`);
> `servers/test_knowledge.py` is green at **56 tests** (20 new, RED→GREEN). The deploy step
> (`intent-knowledge.fastmcp.cloud`) remains Brien-driven.

**Status:** `draft` · **Created:** 2026-05-31 · **Last touched:** 2026-05-31

---

## 0. Vocabulary reconciliation (why these names)

The validating category (LYKN / Mem0 / Supermemory / Zep / Obsidian-Bases) has its own
vocabulary. Per `SIG-2026-05-31-exposed-vocabulary-divergence-principle`, our exposed-surface
vocabulary is **intentionally NOT 100% matched** to theirs — to avoid derivative/positioning
challenges and to signal that we operate one altitude up (S2), not as a me-too memory product.
Every term below is anchored in our preexisting canon and is layer/boundary-explicit.

| Their / generic term | Our term | Anchored in |
|---|---|---|
| `brief` / snippet | **`sightline`** | spatial/visual metaphor; `tagline` (Voices); "fat-marker sketch" (Spec template) |
| `injection_policy` | **`supply_policy`** | "context supply chain" (substrate-exposure §composes-with; plan-mode) |
| `rule` / `fact` / `belief` | **`normative` / `grounded` / `provisional`** | the Intent ontology: DDR/contract (binding) · observation/event (sourced) · signal+confidence (revisable) |
| `get_context_block` | **`get_core`** | "slice" (substrate-exposure); `get`/`list`/`lineage` verb shape |
| `search_vault` ("vault" = Obsidian) | **`query`** (existing — no new verb) | the shipped `query` verb (DEC-010); renaming it would import Obsidian *and* break the deployed contract |
| `audit_gaps` | **`audit_chain`** | "traceability chain" (Intent); `chain_audit` (Cast); "lint" coverage |
| "verbatim-passthrough" | **`preservation_invariant`** | Voices "preservation check" + INV-* ; Witness "verbatim source preservation" / "conservation law" |
| `STM` / `LTM` | **standing core / on-demand retrieval** | "slice" framing; avoids memory-category coding |

Boundary/layer reading: `sightline` and `supply_policy` are **envelope-boundary** concepts;
`normative/grounded/provisional` is **epistemic standing** in our ontology; `get_core` /
`query` / `audit_chain` are **verbs at the exposure boundary**; `preservation_invariant` is a
**boundary invariant**. None mirror the category's words.

---

## 1. Intent

### What I noticed

The 2026-05-31 category scan (S1–S3) surfaced four adoptable design deltas (D1–D4) that the
commoditizing personal-synthesis category has converged on — and which sharpen our **already-
shipped** `intent-knowledge` server (verbs `query`/`get`/`list`/`lineage`/`freshness`, Phase 1
read-only, deploy pending). They are refinements at the operating-model altitude, validated by
the market, not borrowed direction.

### Why it matters now

The server shipped Phase 1 but **has not deployed** (`servers/DEPLOYMENT-INTENT-KNOWLEDGE.md`,
Brien-driven step pending). The envelope contract is therefore still soft — the cheapest moment
to fold in `sightline` + supply-policy typing is *before* deploy hardens it against live clients.
S1's strategic payload says: invest in the spine's interface quality. The envelope *is* that
interface.

### Desired outcome

A chat/agent surface can (a) triage relevance from a one-line `sightline` on a cheap tier before
any full-body read; (b) know an item's **supply policy** from its epistemic standing
(normative/grounded/provisional); (c) pull a cheap always-on **standing core** and run on-demand
retrieval as two distinct tools; (d) ask the graph "what's broken / un-wired" via `audit_chain`;
and (e) trust that sourced items come back **verbatim**, never silently re-synthesized at the
boundary.

---

## 2. Shape

### Approach

Extend the existing envelope and verb set on `servers/knowledge.py`. Compose with what already
shipped — `classification.yaml` (scope tier) and the library-index BM25 backend (already wired
per `substrate-exposure-architecture.md` Phase-2 swap). No new datastore; repo stays the truth.

### The deltas

**D1 — `sightline` (required envelope field).** Every returned entity carries a required one-line
`sightline`. Relevance routing / preamble-as-router: a cheap tier (Ollama) triages on `sightline`
before Claude reads the full body. Extends the shaped-summary discipline already used by the
`list` verb to a required field on *all* returns. **Low risk** — additive envelope field.

**D2 — supply-policy typing (envelope field `supply_policy`).** ⚠ **SCHEMA CHANGE.**

| Value | Maps to our ontology | Supply behavior |
|---|---|---|
| `normative` | DDR / contract / constraint (binding) | **always supply** |
| `grounded` | observation / event (sourced ground-truth) | supply **on demand, with provenance** |
| `provisional` | signal / hypothesis (revisable, carries confidence) | supply **with confidence + source tag** |

Pairs with D1: **standing sets supply policy, `sightline` sets routing** → deterministic
Ollama→Claude tiering. **Key simplification:** `supply_policy` largely *derives* from an entity's
existing type/status — a DDR is `normative`, an event/observation is `grounded`, a signal is
`provisional`. So this is mostly a **projection of the ontology we already have**, with an
optional authored override; it is not a from-scratch taxonomy. That lowers its risk (see
§Ratification). It still requires explicit approval before any write (see §Open questions).

**D3 — dual-read.** Adds one verb; reuses one.
- `get_core` — cheap, always-on **standing core** (a small standing-context slice; Supermemory's
  live `profile.md` is the *reference design* from S1). **New verb.**
- on-demand retrieval = the **existing `query` verb** (top-K BM25+vector). No "vault", no new
  verb — D3's "search" half is already shipped.
- Token-efficiency goal expressed as two tools: small-always-on (`get_core`) + large-on-demand
  (`query`). Preserves substrate-exposure §Q4 discipline (worst-case one full entity body / call).

**D4 — `audit_chain` (Observe-phase verb).** Graph audit of the traceability chain — un-specced
Signals, un-contracted Specs, unverified Contracts, orphans → **drift JSONL + a glanceable color
signal.** This already exists *conceptually* as Intent's lint and Cast's `chain_audit` ("orphans
are flagged" — `intent/CLAUDE.md`); D4 exposes it as an MCP verb + Base-style **views** (coverage,
unverified-Contract count, staleness — per the Bases convergent-validation note). **Low risk** —
read-only audit.

**`preservation_invariant` (from S3).** At the envelope boundary, `grounded` and `provisional`
items with named provenance MUST be returned **verbatim with source preserved** — no synthesis-
rewrite at the exposure layer. Envelope-level analog of Voices' `named_dissents` preservation
check and Witness's conservation law.

### Boundaries

**In:**
- Additive envelope fields (`sightline`, `supply_policy`)
- Verbs: `get_core` (new) + `query` (existing, reused); `audit_chain` (new)
- `preservation_invariant` + a round-trip test
- Base-style `views` over `audit_chain` output

**Out:**
- Write-back / capture-from-anywhere (stays Phase 2 per WS-DDR-099)
- **Engine swap** (Mem0/Supermemory/Zep are reference/fallback only — *we build, not adopt*)
- The deploy step (`intent-knowledge.fastmcp.cloud/mcp` — Brien-driven)
- Any change to scope-token / `classification.yaml` tier semantics (`supply_policy` composes with
  tier; it does not replace it)

### Key decisions (already made — do not revisit)

- Repo-as-truth + MCP-front composition (WS-DDR-099).
- Classification tier + scope-token enforcement (DEC-010) stays; `supply_policy` is orthogonal to
  confidentiality tier.
- library-index BM25 is the retrieval backend; on-demand retrieval reuses the existing `query`.
- Voices' verbatim preservation + Witness's conservation law are the models for
  `preservation_invariant`.
- Exposed vocabulary is intentionally divergent from the validating category (§0).

### Open questions (agent must STOP and ask)

1. ~~**D2 — override surface.**~~ **RESOLVED 2026-05-31 (Brien): override lives in entity
   frontmatter** (durable, git-tracked, co-located with the entity; matches repo-as-truth).
   `supply_policy` otherwise derives from entity type; unknowns default to `provisional`, never
   `normative`.
2. **D3 — `get_core` source:** hand-curated `profile.md` analog, or synthesized on the fly from
   top-ranked entities?
3. **D4 — orphan false-positives:** intentional orphans (e.g., parked signals) need an
   `intentional: true` opt-out or `audit_chain` will nag.

### Prior art (read before building)

- `Core/frameworks/intent/spec/substrate-exposure-architecture.md` — the design this extends
- `Core/frameworks/intent/servers/knowledge.py` + `servers/test_knowledge.py` — the target
- `Core/products/voices/spec/SPEC-001-voices-dissent-preservation.md` — preservation invariant model
- `Core/frameworks/intent/spec/classification-schema.md` — the orthogonal tier field
- S1–S3 + the vocabulary-principle signal

---

## 3. Contract

### Done when

- [x] `query`/`get`/`list` return a required non-empty `sightline` on every entity. *(D1 — `test_*_carries_sightline`)*
- [x] every returned entity carries `supply_policy ∈ {normative,grounded,provisional}`, derived from type with optional frontmatter override. *(D2 — `test_supply_policy_*`)*
- [x] `get_core` returns a bounded standing core (≤ ~1k tokens) with no full-body dump. *(D3 — `test_get_core_*`)*
- [x] on-demand retrieval is the existing `query` (top-K; K default 10, max 25). *(unchanged — existing `query` tests stay green)*
- [x] `audit_chain` emits drift findings + a single glanceable color (green/amber/red) summary. *(D4 — `test_audit_chain_*`)*
- [x] `preservation_invariant`: a test asserts a sourced `grounded`/`provisional` item round-trips byte-identical. *(`test_preservation_invariant_*`)*

### Smoke test

```
# against a local intent-knowledge server, post-ratification:
mcp call get_core                     → bounded standing core; every item has sightline + supply_policy
mcp call query "substrate"            → top-K, each hit carries sightline
mcp call audit_chain                  → {color, counts:{unspecced_signals, uncontracted_specs,
                                          unverified_contracts, orphans}} + drift.jsonl path
# assert: a known sourced grounded item comes back verbatim (no paraphrase)
```

### Failure modes to watch

- `sightline` drifts into being treated as the *answer* by the cheap tier (mitigate: sightline is
  routing-only, contract-documented as non-authoritative).
- `supply_policy` mis-types a revisable `provisional` as `normative` → over-supply of unstable
  inference. (Default unknowns to `provisional`, never `normative`.)
- `preservation_invariant` silently violated by a future summary helper (mitigate: the round-trip
  test is the catch-net; wire it like a Voices INV-* invariant).
- `audit_chain` false-positives on intentional orphans (see Open Q3).

### Observability

`audit_chain` **is** the observability surface — the drift JSONL + color signal is the Observe-
phase read on substrate health. Ties to DEC-009's authoring-observability path.

---

## Ratification (per-delta — RATIFIED 2026-05-31)

**RATIFIED 2026-05-31** (Brien, via decision surface). All five deltas approved for build.

| Delta | Risk | Schema change? | Status |
|---|---|---|---|
| D1 `sightline` | low (additive field) | no | ☑ ratified |
| D2 `supply_policy` typing | low–medium (mostly a projection of existing types + an override) | **YES** | ☑ ratified — **override = entity frontmatter** (Open Q1 closed) |
| D3 `get_core` (+ reuse `query`) | low (one new verb) | no | ☑ ratified |
| D4 `audit_chain` + Base-style views | low (read-only) | no | ☑ ratified |
| `preservation_invariant` | low (a refusal + a test) | no | ☑ ratified |

Decision-log edges are now **written** (not just surfaced): **DEC-012** records the ratified
envelope/verb extension + the D2 typed-envelope schema + the frontmatter-override choice, and
**DEC-010** carries a forward pointer to DEC-012. Still **surfaced, not written** (not part of this
ratification): the spine-vs-engine positioning DDR and the S2 altitude-placement atom.

**Built 2026-05-31 (TDD).** D1–D4 + `preservation_invariant` are implemented in
`servers/knowledge.py` and covered by 20 new tests in `servers/test_knowledge.py` (full
suite green at 56). The preservation round-trip test is the wired catch-net. Remaining
Execute step is the deploy (`intent-knowledge.fastmcp.cloud`), which is Brien-driven.

---

## Notes

This spec deliberately stops at the operating-model altitude. It does not touch the memory engine
(commoditizing per S1) and does not adopt an external one (reference/fallback only). It invests
exactly where the S1–S3 synthesis says the moat is: the spine's interface, the preservation
invariant, and the audit loop — in our own vocabulary.
