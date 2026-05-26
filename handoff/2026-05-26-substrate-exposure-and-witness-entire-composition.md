# Handoff — Substrate Exposure + Witness/Entire Composition Architecture

**Session date:** 2026-05-26
**Origin surface:** Claude Code (desktop) — Phase 1 + Phase 2 of the Entire scope audit completed and shipped
**Target surface:** Cowork (architecture brief + composition design) → Code (canonicalization of decisions)
**Owner:** Brien — engineer/architect/system designer; creator of the Intent methodology; author of Coherence Engineering as its practice layer.

---

## 0. How to use this document

Read end to end before acting. This handoff carries two coupled architectural tracks that emerged from a single closed audit thread:

- **Track A — Substrate exposure:** The desktop is currently both the single source of truth *and* a single point of failure. Chat surfaces can't reach the canonical `.intent/` + `wiki/` substrate when traveling or working from non-desktop interfaces. Architect the fix.
- **Track B — Witness + Entire composition for N products:** A composition runbook so any new product/project Brien spawns can adopt the observability fabric mechanically — Tier 0 (Entire provenance) → Tier 1 (local event stream) → Tier 2 (Witness federation) → Tier 3 (runtime telemetry). The pattern exists in spec; the operational scaffolding does not.

The two tracks share a root cause: **the substrate is structurally bound to one machine and one surface, when it should be sibling-composable across surfaces *and* across products.** Treat them as siblings — each is independently shippable, and each unblocks the other when complete.

A note on intent: the reasoning in §1–§3 is load-bearing — it is the framework's two-observabilities distinction freshly resolved (DEC-009, ratified 2026-05-26). Don't discard the reasoning to get to the decisions faster; the reasoning constrains the decisions.

---

## 1. Where we are (closure status of the preceding work)

The 2026-05-25 Entire scope audit closed cleanly today:

- **Phase 1 audit signal:** `Core/frameworks/intent/.intent/signals/2026-05-26-entire-scope-audit-and-observability-delta.md` (SIG-ENTIRE-SCOPE-2026-05-26) — full findings, claims catalog, capability mapping, named delta.
- **Phase 2 canonicalization commit:** `theparlor/intent` `293283b` (rebased from `a73c561`) — 7 files changed, 234 insertions, 26 deletions. Contains: DEC-009 ratifying the new Entire scope (supersedes DEC-007), CLAUDE.md `.entire/` line re-scoped, AI Agent persona separated from authoring-provenance sources, intent-concept-brief third-pillar phrasing corrected, product-roadmap §177 open question resolved in narrative, 4 intent-work-system.jsx sub-edits, 1 intent-native-repos.jsx hero-description fix.
- **Memory hygiene:** `~/.claude/projects/-Users-brien-Workspaces/memory/reference_entire_io.md` updated — stale config path corrected, Witness's adapter named as the canonical federating consumer.

The closure-discipline triad is satisfied:
- **Upstream control:** DEC-009 is now the canonical record. New framework readers entering through CLAUDE.md or DEC-007 encounter the corrected scope first.
- **Catch-net:** the audit signal lives in `.intent/signals/` and is read by every future framework-level audit pass; the supersession is bidirectional (DEC-007 carries `Superseded by: DEC-009`, DEC-009 carries `supersedes DEC-007`).
- **Pipeline survival:** framework canonical docs survive `render_all`; JSX artifacts render to the public site (`theparlor/intent-site`) via the standard sync.

This handoff is what comes *after* that closure: the two architectural tracks that the audit surfaced but explicitly deferred.

---

## 2. The conceptual frame (carry forward verbatim)

Two structural ideas land at the root of both tracks. Don't discard them; the decisions in §6 unwind to these.

### 2a. Two observabilities (DEC-009-anchored)

| | Authoring path | Running-system path |
|---|---|---|
| What it observes | Prompt → response → files touched → commit. Provenance of *how the code got written*. | Runtime metrics, contract-assertion pass/fail, latency distributions, trust-score drift, signal-source distribution. Provenance of *whether the artifact works*. |
| Plane | Cockpit / keystroke-to-commit | Aircraft telemetry / commit-to-reality |
| Granularity | One agent session (`YYYY-MM-DD-<UUID>`) | One trace, one span, one metric sample |
| Capture window | During agent session | During code execution in production |
| Tool | Entire.io (post-session hook + shadow git branch) | OTel Collector + Grafana/Tempo/Mimir/Loki |
| Status | ✅ Working (Tier 0 in any repo) | 🟡 Specced but not running |
| Loop role | Seeds the loop | Closes the loop |

Both are required for a product to claim *real* observability. Entire alone is not observability — it is one of N inputs to it. The two-observabilities framing is publishable (per audit Open Decision #4).

### 2b. Substrate as sibling, not as machine

The substrate (`.intent/` + `wiki/` + the connected knowledge graph) is currently *bound* to the desktop filesystem. Every surface that wants to read or write the substrate has to be on the desktop. This collapses three distinct concerns into one:

- **Identity** (what is the canonical state of an artifact at time T?)
- **Reachability** (who can read it, from where, with what authority?)
- **Liveness** (is the source-of-truth process online?)

The WS-DDR-025 sibling-over-parent-child principle says: when these concerns can be served by different mechanisms, separate them. The substrate should be a *sibling* of the surfaces that consume it — an MCP-shaped query interface, or a repo-shaped versioned record, or a hosted projection — chosen per consumer, not collapsed into "files on Brien's laptop." The desktop demotes from source-of-truth to *one reader among several*.

---

## 3. Track A — Substrate exposure (handoff §6 from the predecessor doc)

**Problem statement:** Chat-surface Claude (mobile/web/desktop app, anywhere Brien isn't sitting at Code) has memory-*fragments* of Brien's work, never the work itself. This very thread is the proof — a Claude chat session needed to write a handoff *to* Code because chat couldn't reach the Intent framework, `.intent/` signals, Witness scaffolding, or any of the design substrate. When Brien travels, his thinking partner becomes a stranger.

**Design direction (not yet decided — Cowork resolves):** Two non-exclusive mechanisms to evaluate.

### Option 1 — MCP server fronting the knowledge farm

- Extends the existing `intent-notice` (8001) / `intent-spec` (8002) / `intent-observe` (8003) / `intent-knowledge` (8004) MCP server family with a substrate-exposure surface.
- Any surface (chat included) connects to the MCP endpoint and queries: signals, intents, specs, decisions, knowledge artifacts, persona registry entries, freshness state.
- Read-first, write-back as second milestone.

**Cleanest fit with existing architecture.** Lines up with the "first brain" design (Ollama for bulk processing; Claude reserved for high-judgment synthesis). The qmd retrieval layer (BM25 + vector) is the relevance-filtering front end — only relevant slices cross the wire, bounding token-context burn.

### Option 2 — Committed repo as addressable truth

- The `.intent/` + `wiki/` repo *is* the canonical plane.
- Surfaces read from the repo (or a hosted projection of it) rather than from any one machine.
- Code's plan-mode already treats the repo as a versioned "context supply chain"; this generalizes that to all surfaces.
- Hosted projection (GitHub Pages? Cloudflare Pages? a small Worker?) gives chat surfaces a fetchable URL surface without exposing the raw repo.

**Lower-novelty fit but with a hard hosting constraint.** The Max-subscription / April-2026 routing restrictions are the binding gate — see §5.

The two options are not mutually exclusive. Probable answer: MCP-front *and* repo-as-truth, with the MCP server reading the repo on demand and the repo serving as the source-of-truth.

### Constraints to honor (carry forward from predecessor handoff)

- Architecture must stay within Max subscription and avoid third-party API routing restrictions effective April 2026.
- Ollama handles bulk processing/storage of markdown; Claude Code/Cowork reserved for high-judgment synthesis.
- Littlebird vs. Kestrel evaluated for continuous capture; combined architecture preferred.
- **Token-context burn is the primary risk** when connecting knowledge farms to Claude via MCP. The exposure design MUST answer: how does a chat surface pull *relevant slices* without dragging the whole substrate into context?

### Design questions (Cowork resolves these, in order)

1. **Minimum addressable unit:** does the chat surface need a *query interface* (ask the substrate) or a *sync* (mirror a subset locally)? Recommendation: query-first; sync is a Phase 2 add.
2. **Read-only from chat, or read/write?** Recommendation: read-only first (lower cost, fast win, no auth/conflict complexity). Write-back closes the loop from anywhere — Signals/Notices captured from mobile — but raises redaction, auth, and conflict-resolution costs. Stage it.
3. **Hosting:** where does the MCP server run so it's reachable when the desktop is off/asleep/traveling? Options under evaluation: GitHub Actions (simplest), Cloudflare Worker (most capable, matches existing FastMCP Cloud pattern), dedicated machine (interim). Does this violate the Max-subscription / routing-restriction constraints? **This is the constraint crux. Track A blocks until it's answered.**
4. **Relevance filtering:** how does the qmd BM25+vector layer (or equivalent) keep token burn bounded? Recommendation: at the MCP server, not at the client. Client asks "show me signals related to Subaru Phase 5"; server returns the top N ranked chunks. Client never sees the full substrate.

### Deliverable shape — Track A

An architecture brief (markdown, 2–3 pages) naming:
- The chosen exposure mechanism (MCP-front + repo-as-truth composition, or single-mechanism)
- The runtime/hosting answer with constraint-validation
- The relevance-filtering strategy (qmd? something simpler?)
- The desktop's recast role (one reader among N)
- The Phase 1 / Phase 2 cut: minimum viable read-only exposure, then write-back

If a load-bearing decision lands, write a DDR. WS-level (`Workspaces/.context/DECISIONS.md`) if it touches placement/governance; Intent-framework-local (`Core/frameworks/intent/spec/decision-log.md`, next sequential DEC) if it's a framework architecture call.

---

## 4. Track B — Witness + Entire composition for any new product

**Problem statement:** the audit (SIG-ENTIRE-SCOPE-2026-05-26) named the composition tiers but did not produce the operational runbook. For *any* new product/project Brien spawns, the observability fabric should be enable-able mechanically — no per-product code, no bespoke wiring.

**The composition pattern (settled, from DEC-009 + Witness CONTEXT.md):**

```
Tier 0 — Provenance (cheap, immediate)
   entire enable  →  .entire/ directory captures session traces locally

Tier 1 — Local event stream
   session-end hook emits to .intent/events/events.jsonl
   (the product's own event log; sibling to .entire/)

Tier 2 — Federation
   Witness adapter ingests the product's events.jsonl  →  Witness events-store
   (Witness becomes the federating substrate across N products)

Tier 3 — Runtime telemetry
   product emits OTel spans for runtime events (contract pass/fail, latency, errors)
   →  OTel Collector  →  Grafana panels  →  observations/ records
   (closes the Observe → Notice loop)
```

The scaling property: tiers are *independent*. A new product can sit at Tier 0 for weeks before climbing. Witness ingests via standard transports (OTLP + structured stderr JSONL); a new product just emits in those formats — Witness doesn't need product-specific code per new entrant.

### What's missing for "spring up any product" to work mechanically

1. **Scaffold script:** `intent-init <product>` (or equivalent) that creates `.intent/`, runs `entire enable`, installs the session-end hook, registers with Witness. Per the SignalCaptureSystem-style tiered adapters in `Core/frameworks/intent/spec/signal-capture-system.md`, this could be a Tier-1-style local-CLI scaffold.
2. **Witness adapter completion:** `Core/products/witness/engine/adapters/entire-io.py` is a stub (migration #5 in WIT-004 order, per Witness CONTEXT.md). Adapter needs to read `.entire/metadata/<session-uuid>/full.jsonl` and emit Witness events with proper `source.system` tagging.
3. **Standard OTel emission helper:** a small library (Python? shell?) so products don't write OTel boilerplate. Sits at `Core/frameworks/intent/observe/adapters/` alongside `file-tail.py`. Could be a thin wrapper over `opentelemetry-sdk` that products import for their runtime emit calls.
4. **Composition runbook:** a checklist document at `Core/frameworks/intent/playbooks/spawn-a-product.md` (or similar) that lists the four tiers and the exact commands to climb each. Adoption ladder by design.

### Design questions — Track B

1. **Where does the scaffold script live?** Options: `bin/intent-init` (in the framework repo, callable from anywhere), `Core/products/scaffolding/` (new product-scaffolding sub-product), `~/.claude/scripts/` (developer-local). Recommendation: `bin/intent-init` — keeps the scaffold close to the framework canon.
2. **Witness adapter — synchronous tail or batched ingest?** Today the framework's Observe leg uses a file-tail adapter (`file-tail.py`) that emits OTel spans for each event. Witness's adapter could follow the same pattern — tail `.entire/metadata/` directories per registered product. Or batch ingest hourly. Recommendation: tail, for parity with `file-tail.py`.
3. **How does Witness discover new products?** Today Witness has no product-registration mechanism — the adapter has to be configured per product. Options: a `witness-registered-products.yaml` at the Witness root (manual registration), a `products.json` scan (auto-discovery of any directory with `.entire/`), or a sibling-registry pattern (each product self-registers by writing to a Witness-watched path).
4. **What's the per-product cost of climbing each tier?** Tier 0: one command (`entire enable`). Tier 1: ~10 lines of session-hook config. Tier 2: ~1 line in Witness config to point the adapter at the new product. Tier 3: variable — depends on the product's runtime surface. Cowork resolves with concrete numbers.

### Deliverable shape — Track B

A composition runbook (markdown, 1–2 pages) at `Core/frameworks/intent/playbooks/spawn-a-product.md` that:
- Names the four tiers with exact commands
- Lists prerequisites (Witness running, OTel Collector configured, etc.)
- Lists per-product cost at each tier (lines of config, minutes of work)
- Names the dependencies between Track A and Track B (e.g., "Witness's substrate exposure design from Track A becomes the federation point for Track B")

If load-bearing scaffold-design decisions land, write a DDR (Intent-framework-local).

---

## 5. Constraints (shared across both tracks)

- **Max subscription only.** No external API routing. Effective April 2026.
- **Ollama for bulk processing / storage.** Claude Code/Cowork only for high-judgment synthesis.
- **Token-context burn is the primary risk** when connecting substrates to Claude. Every exposure design must bound the surface a chat surface sees.
- **The Max-subscription / routing-restriction constraints bound the hosting answer.** If always-on hosting violates the constraints, the substrate-exposure track is forced to "desktop-resident with stale-tolerated chat surface" — and the design changes meaningfully.
- **Witness is at Scaffold tier** per PCU-2026-05-09 — runtime built (Phase 5, 2026-05-13), MCP server (WIT-005), adapter stubs (WIT-004), but full implementation pending. SPEC-001 is `draft/blocked` on two cross-product dependencies (library-index AM-3 audit at 100%; Conduit OTLP-emit path shipping). Track B can design around Witness's current state without unblocking those dependencies first; the design should explicitly note the dependency-completion conditions for Tier 2 to go live.

---

## 6. Open decisions for Brien (resolved in Cowork or before)

These are L0/L1 decisions Brien sets. The Cowork agent should surface them but not unilaterally close them.

1. **Hosting (Track A, Q3):** is Brien willing to run a small always-on endpoint (Cloudflare Worker, GitHub Actions schedule, dedicated machine), or must everything stay desktop-resident and the chat surface accept staleness when the desktop is offline? **This is the constraint crux for Track A.**
2. **Substrate exposure read/write scope:** read-only-first (recommended) or read/write from day one?
3. **Witness adapter completion timing:** is Track B blocked on the WIT-004 migration #5 stub becoming production, or can Track B's runbook ship with Tier 2 marked "ready when Witness adapter ships"?
4. **Publishable framework-site post on "two observabilities":** ship it? (Audit recommendation: yes, short post, cockpit/aircraft metaphor as the hook.)
5. **Scope of "any product":** does this include client engagements (Subaru, ASA, etc.) or only Brien-internal products (Forge, Cast, Witness, Throughline, etc.)? Confidentiality + redaction considerations differ.

---

## 7. Existing architecture to compose with (don't reinvent)

The Cowork agent should pull these into context early; they constrain the design space.

- **Witness** — `Core/products/witness/` — observability anchor at the event→signal position. CONTEXT.md, ARCHITECTURE.md, spec/SPEC-001-witness-observability-anchor.md (draft/blocked), `engine/adapters/entire-io.py` (stub).
- **Intent framework Observe leg** — `Core/frameworks/intent/observe/` — OTel Collector + Grafana pipeline. README.md, otel-collector-config.yaml, adapters/file-tail.py.
- **Intent framework `.intent/`** — `Core/frameworks/intent/.intent/` — signals, intents, specs, contracts, decisions, events. The canonical substrate; the thing chat needs to read.
- **Intent MCP server family** — `intent-notice` (8001), `intent-spec` (8002), `intent-observe` (8003), `intent-knowledge` (8004). FastMCP-based, deployable to FastMCP Cloud or Cloudflare Workers at $0/mo.
- **Cortège fetch fabric** — `Core/products/cortege/` — domain-aware fetch with per-domain concurrency caps; relevant if the substrate exposure needs to fetch external content.
- **library-index** — `Core/products/library-index/` — Brien's 39k+ file knowledge graph; the qmd retrieval layer (BM25 + vector). Probable relevance-filtering anchor for Track A.
- **DEC-009 (just-ratified)** — `Core/frameworks/intent/spec/decision-log.md` — the Entire scope record. Track B must reference it.

---

## 8. Phase split (Cowork → Code)

**Phase 1 (Cowork — this handoff):** thinking work.
- Track A architecture brief
- Track B composition runbook
- DDRs for any load-bearing decisions
- Surface deltas to Brien before rewriting framework canon

**Phase 2 (Code — after Cowork):** filing work.
- Commit the architecture brief + runbook to `Core/frameworks/intent/playbooks/` (or wherever the Cowork output lands)
- Apply any framework canon edits the architecture brief requires
- Scaffold `bin/intent-init` if Track B's design specifies it
- Update Witness adapter from stub if Track B's design unblocks it

Don't try to do Phase 2 in the Cowork session. Phase 1 owns thinking; Phase 2 owns filing.

---

## 9. Source manifest

- **Phase 1 audit signal:** `Core/frameworks/intent/.intent/signals/2026-05-26-entire-scope-audit-and-observability-delta.md` — the load-bearing context for the two-observabilities frame. Read end-to-end.
- **DEC-009 (just-ratified):** `Core/frameworks/intent/spec/decision-log.md` line 147 — the canonical Entire-scope decision.
- **Phase 2 commit:** `theparlor/intent` `293283b` — full diff of the canonicalization.
- **Witness CONTEXT.md:** `Core/products/witness/CONTEXT.md` — the federating-substrate design.
- **Witness positioning.md:** `Core/products/witness/docs/positioning.md` — the "what Witness is and isn't" doc, with the five-source list.
- **Intent framework ARCHITECTURE.md:** `Core/frameworks/intent/ARCHITECTURE.md` — three-layer model, MCP server family, schema alignment, trust formula, autonomy levels.
- **Intent framework Observe leg:** `Core/frameworks/intent/observe/README.md` — OTel pipeline.
- **Intent framework rendered Observe page:** `Core/frameworks/intent-site/docs/observe.html` — the canon-as-published view of the Observe leg.
- **Predecessor handoff (2026-05-25 chat session):** the document that triggered the Entire audit; substrate-exposure language is unchanged in this handoff except where DEC-009 sharpened it.
- **Cortège, library-index, qmd retrieval references:** check `Core/products/cortege/`, `Core/products/library-index/`, and the qmd ranking layer in library-index for relevance-filtering precedents.

---

## 10. Open decisions for Brien (consolidated)

See §6. The five decisions there are not resolved in this handoff — they are Cowork's job to surface, structure, and (where possible) recommend. Brien closes them.

---

*End of handoff. Phase 1 (Cowork) owns the thinking. Phase 2 (Code) owns the filing. Surface deltas before overwriting framework canon. The two-observabilities frame (§2a) and the substrate-as-sibling principle (§2b) are load-bearing — don't dilute them to ease an architectural decision.*
