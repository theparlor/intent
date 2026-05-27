---
title: Decision Log
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
technologies:
  - jira
  - slack
depth_score: 5
depth_signals:
  file_size_kb: 20.2
  content_chars: 19248
  entity_count: 2
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.16
related_entities:
  - {pair: consulting-operations ↔ teresa-torres, count: 66, strength: 0.111}
  - {pair: consulting-operations ↔ marty-cagan, count: 63, strength: 0.094}
  - {pair: consulting-operations ↔ subaru, count: 44, strength: 0.121}
  - {pair: consulting-operations ↔ slack, count: 41, strength: 0.124}
  - {pair: consulting-operations ↔ jeff-patton, count: 40, strength: 0.085}
---
# Decision Log

> Every significant decision from Intent's founding: naming, positioning, architecture. With context, alternatives considered, and rationale.

## Why Log Decisions?

Most product decisions are invisible. They happen in conversations, Slack threads, or someone's head — and by the time a new team member asks "why does it work this way?", the context is gone. The decision log is Intent's antidote: a durable, git-tracked record of what was decided, what alternatives were considered, and why.

This is also a core piece of Intent's open development commitment. If we're asking teams to adopt a new operating model, they deserve to see how that operating model was designed — including the wrong turns, the tradeoffs, and the things we're still unsure about.

## Decision Format

Each decision follows a consistent structure:

- **Context:** What situation prompted the decision
- **Alternatives considered:** What other options were on the table
- **Decision:** What was chosen
- **Rationale:** Why this choice over the alternatives
- **Date:** When the decision was made
- **Source:** Where the decision was made (session, conversation, review)

## Decisions

### DEC-001: Product named "Intent"

**Decided:** 2026-03-28

**Context:** Working name was "Dev OS" throughout initial development. Sounded like DevOps infrastructure tooling, which confused the positioning.

**Alternatives considered:** Frame, Premise, Lucid, Upstream, "Intent Operating Flow"

**Decision:** Single word "Intent" — names exactly what the layer produces. One word, like Entire.io.

**Rationale:** The product IS intent — the layer where teams crystallize why they're building what they're building. The name should be the thing, not a metaphor for the thing. Intent captures the philosophical core: teams declare what they want, agents execute against it. The name hints at both user intent (what teams need) and agent intent (what guides execution). Single word, easy to pronounce, available.

### DEC-002: Position as a team operating model, not a tool

**Decided:** 2026-03-28

**Context:** Should Intent be a SaaS tool, a methodology, or a consulting offering?

**Alternatives considered:** Build a Jira replacement, build a CI/CD integration, build a dashboard.

**Decision:** Pitch Intent as a methodology for teams, not as feature-bundled software.

**Rationale:** The bottleneck isn't tooling — it's organizational model. Selling a tool optimizes the wrong lever. Selling a methodology lets teams adopt at their own pace and layer Intent on top of existing infrastructure.

### DEC-003: Build in the open from day one

**Decided:** 2026-03-28

**Context:** How transparent should Intent's own development be?

**Alternatives considered:** Launch with a private beta, launch with polish, launch stealth.

**Decision:** Publish signals, decisions, and architectural choices publicly. Dogfood Intent's own observe layer.

**Rationale:** Early-stage methodology products benefit from transparency. Showing work builds trust. Doing it publicly forces us to think clearly about our own decisions. It's also a credibility test: if we don't practice what we preach, practitioners will notice.

### DEC-004: File-native, git-tracked, OTel-compatible

**Decided:** 2026-03-28

**Context:** How should Intent artifacts be stored and events be emitted?

**Alternatives considered:** Central backend, GraphQL API, proprietary event format.

**Decision:** All Intent artifacts (signals, intents, specs, contracts, decisions, events) live in versioned files. No proprietary database. Emit events in OpenTelemetry format.

**Rationale:** Practitioners distrust lock-in. File-native means they can read and modify Intent artifacts with any text editor. Git tracking is audit trail. OTel compatibility means events integrate with existing observability stacks. These choices reduce friction for adoption and give teams control.

### DEC-005: Target practitioner-architects first

**Decided:** 2026-03-28

**Context:** Who is the initial audience?

**Alternatives considered:** Target PMs, target CTOs directly, target large enterprises.

**Decision:** Go-to-market focused on senior ICs who feel the gap acutely and have org influence.

**Rationale:** Practitioner-architects have felt the problem (AI-augmented workflow breaks agile) and have the credibility to reshape process. They're more likely to experiment. Word-of-mouth from them to PMs and leadership is more credible than top-down adoption.

### DEC-006: Specs as contracts, not stories

**Decided:** 2026-03-28

**Context:** What mental model should teams use for specifying work?

**Alternatives considered:** Enhance user stories with more structure, adopt BDD, adopt property-based testing frameworks.

**Decision:** Shift mental model from "user stories" (prose narrative) to "contracts" (verifiable assertions).

**Rationale:** Agents need verifiable acceptance criteria before they can execute. "Given-when-then" helps but still implies prose is the source of truth. Contracts invert that: the spec is the contract, prose is supplementary. This makes agent execution deterministic.

### DEC-007: Three-layer stack positioning

**Decided:** 2026-03-28

**Superseded by: DEC-009 (2026-05-26)** — Entire.io scoping corrected from "observability layer" to "authoring-provenance recorder."

**Context:** Needed to clarify where Intent sits relative to existing tools (Kiro, GitHub Spec Kit, Claude Code, etc.)

**Decision:** Intent sits ABOVE spec-driven dev tools, which sit above AI coding assistants. Entire.io is the observability layer that runs alongside all three.

**Rationale:** Existing tools handle spec→code and code execution. Nobody owns the "why are we building this" layer. That's the gap.

### DEC-008: Staged GTM over tooling-first

**Decided:** 2026-03-28

**Context:** Should Intent invest in tooling immediately or validate the methodology first?

**Decision:** Stage it: thought leadership (manifesto + case studies) → methodology product (playbook + workshops) → tooling (conditional on validation).

**Rationale:** Building tooling before validating the methodology is premature. The highest-leverage move is content + interviews, not code. Need 5 in-depth interviews with teams struggling with AI + Agile friction before committing to tooling investment.

### DEC-009: Entire.io scoped as authoring provenance (supersedes DEC-007)

**Decided:** 2026-05-26

**Context:** DEC-007 (2026-03-28) framed Entire.io as "the observability layer." Subsequent framework development (observe/ OTel stack, observations/ runtime feedback, Witness federating substrate) revealed this framing is over-broad: Entire captures authoring-side provenance only.

**Alternatives considered:**
- (a) Leave DEC-007 as-is and note the limitation elsewhere — rejected, leaves the over-broad claim in canonical canon.
- (b) Narrow Entire's role to "Execute-phase session-recovery only" — rejected, loses legitimate provenance-input value to events.jsonl.
- (c) Supersede with explicit authoring-provenance scope — selected.

**Decision:** Entire.io is the authoring-provenance recorder that runs alongside spec-driven dev tools and AI coding assistants. Runtime observability is owned by the OTel/Grafana stack (`observe/`) and the `observations/` runtime-feedback directory. Entire is one event source feeding `.intent/events/events.jsonl` via the Witness adapter (`Core/products/witness/engine/adapters/entire-io.py`).

**Rationale:** Granularity = git commit + intra-session checkpoints. Capture window = during the agent session. Outcome verification (did the artifact work in production?) is not in Entire's capability surface — that lives in the OTel stack with contract assertions, metric thresholds, and incident catalog. Conflating the two created an over-trust pattern in framework dev-continuity surfaces while the rendered spec surface (observe.html) was already OTel-native. This DDR aligns the documentation with the architecture.

**Supporting evidence:** `/Users/brien/Workspaces/Core/frameworks/intent/.intent/signals/2026-05-26-entire-scope-audit-and-observability-delta.md`

### DEC-010: intent-knowledge MCP scope extended to substrate exposure

**Decided:** 2026-05-26

**Context:** `Core/frameworks/intent/ARCHITECTURE.md` (line 107) defines `intent-knowledge` (port 8004) with verbs `ingest`, `query`, `lint` — per SPEC-001 and DDR-005. The CLI implementation is pending per Gap 7.1 / track E3 in `.intent/specs/2026-05-20-upgrade-plan.md`. The 2026-05-26 Cowork Phase 1 brief on substrate exposure identifies `intent-knowledge` as the natural host for cross-surface substrate exposure verbs. Two options exist: (a) build a new MCP server (`intent-substrate`, port 8005) dedicated to substrate exposure; (b) extend `intent-knowledge`'s scope to cover substrate exposure, treating substrate query as a specialization of knowledge query. This decision picks (b).

**Alternatives considered:**
- (a) New dedicated `intent-substrate` server (port 8005) — rejected. Creates two servers whose verbs would significantly overlap; substrate *is* the knowledge corpus. Splitting violates the principle that the four-server family maps to the four loop phases plus knowledge.
- (c) Defer the entire question; ship intent-knowledge with only `ingest`/`query`/`lint`, leave substrate exposure as a future track — rejected. The substrate-exposure problem is the load-bearing reason to prioritize the intent-knowledge CLI implementation; deferring loses the motivating use case.

**Decision:** `intent-knowledge` MCP server's scope is extended to explicitly include **cross-surface substrate exposure**. The verb set is broadened beyond `ingest`/`query`/`lint`:

| Verb | Purpose | Bound |
|---|---|---|
| `query(text)` | Top-K relevant chunks via BM25+vector (library-index composition) | K configurable, default 10, max 25 |
| `get(entity_id)` | Single entity by canonical ID (SIG-NNN, INT-NNN, SPEC-NNN, DEC-NNN, WS-DDR-NNN) | One entity per call |
| `list(type, filter)` | Entity list shaped as title+id+timestamp+status (not full body) | Default 20, max 50 |
| `lineage(signal_id)` | Backward + forward lineage chain (depth 3) | Bounded by graph traversal |
| `freshness(path)` | Last-modified + last-render state | Single path |
| `ingest` (existing) | Per SPEC-001 / DDR-005 | unchanged |
| `lint` (existing) | Per SPEC-001 / DDR-005 | unchanged |

The server composes with `library-index` for the `query` verb's BM25+vector ranking. `get`/`list`/`lineage`/`freshness` read directly from the repo file tree. **Phase 1 scope:** read-only verbs only. Write-back verbs (`capture_signal`, `propose_intent`) are deferred to a Phase 2 decision once auth + redaction + conflict design lands. **Deployment:** `intent-knowledge.fastmcp.cloud/mcp` on FastMCP Cloud free tier or Cloudflare Workers, completing the four-server family alongside intent-notice / intent-spec / intent-observe.

**Rationale:** `intent-knowledge` already owns the knowledge-graph cross-cutting layer (ARCHITECTURE.md line 108: "Cross-cutting (Layer 1)"). Substrate query is the natural specialization of knowledge query — the substrate *is* a knowledge corpus with extra structure (canonical IDs, lineage, freshness state). The four-server family stays clean: Notice / Spec / Observe / Knowledge maps to Notice / Spec / Execute+Observe / cross-cutting. library-index composition is identical whether substrate exposure is on intent-knowledge or a sibling server. Picking intent-knowledge avoids duplicating the composition seam. Phase 1 scope is tight — five new read verbs + library-index composition.

**Consequences:** Substrate exposure is delivered via the existing four-server architecture, not a new product. Operational surface area unchanged. The intent-knowledge MCP server's "specced; CLI pending" status (ARCHITECTURE.md line 111) gets a concrete shipping target with a clear motivating use case. Cost: five new verbs vs. three originally specced — moderate increase. Risk: library-index API exposure to intent-knowledge is the one structural unknown; if library-index does not currently expose a usable Python/HTTP API, that exposure becomes a sub-milestone (in scope for E3 track).

**Validation criteria:** Validated when (1) `intent-knowledge` MCP server is deployed at `intent-knowledge.fastmcp.cloud/mcp`; (2) the five read verbs are callable from a chat-surface client; (3) the `query` verb composes correctly with library-index's relevance filter; (4) token-context burn stays bounded — no single call returns more than one entity body or > N shaped summaries; (5) the four-server family at $0/mo is preserved.

**Related:** WS-DDR-099 (substrate exposure mechanism — Workspaces-level placement & governance), DEC-009 (Entire scoped as authoring provenance), DEC-004 (file-native, git-tracked, OTel-compatible), ARCHITECTURE.md lines 107-111 + 303-307, `.intent/specs/2026-05-20-upgrade-plan.md` Gap 7.1 / track E3, SPEC-001.

**Supporting evidence:** `/Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/01-track-a-substrate-exposure-architecture.md`

### DEC-011: bin/intent-init scaffold script + Witness registered-products.yaml

**Decided:** 2026-05-26

**Context:** The 2026-05-26 audit (SIG-ENTIRE-SCOPE-2026-05-26 → DEC-009) named the four composition tiers (Entire / events.jsonl / Witness federation / OTel runtime) but did not produce the operational scaffold. Today the Tier 0 + Tier 1 climb is ~6 minutes of manual setup per product, and Tier 2 registration is ad-hoc. The 2026-05-26 Cowork Phase 1 runbook proposes consolidating that setup into a single CLI: `bin/intent-init`.

**Alternatives considered:**
- `~/.claude/scripts/intent-init` — rejected. Developer-local rather than framework-canonical. New scaffold should ship with the framework, not with one developer's local config.
- `Core/products/scaffolding/` as a new product housing the scaffold — rejected. Creates a meta-product with one tool and no other inhabitants, violating product-shape conventions.
- Auto-discovery (scan `Core/products/*/.entire/`) instead of explicit `registered-products.yaml` — rejected. Some products (client engagements with confidentiality constraints) will need to opt out of federation; explicit registration is the safer default. Revisitable past ~50 products.
- `bin/intent-init` only, no Witness registry file — products auto-register by writing to a Witness-watched path — rejected as more complex than needed at current scale.

**Decision (per Brien's D5-refined close, 2026-05-26):** The framework adopts a scaffold CLI at `Core/frameworks/intent/bin/intent-init` that takes a new product **or client engagement** through the Tier 0 + Tier 1 climb in one command. Per D5-refined: **classification is universal Day 1; Witness federation is selective by tier** — internal-tier federates Day 1, engagement-tier federation is deferred until Phase 2 (when scope enforcement has run hot and per-engagement redaction-maps are authored on demand).

```bash
bin/intent-init <product-name> \
  --path <relative-path> \
  --enable entire,events \
  --classification <tier> \         # REQUIRED — public | internal | confidential:<engagement>
  --register-with witness            # default ON for internal; auto-deferred for confidential:*
```

**Behavior:**
1. Create `<path>/.intent/{events,signals,intents,specs}` and `<path>/.entire/`.
2. Run `entire enable` in the new product directory.
3. Install the session-end hook (`hooks/session-end.sh`) into the product's `.claude/hooks/`.
4. Write `<path>/.intent/classification.yaml` with the declared tier. Schema is enforced — the CLI errors out on engagement-shaped paths (`Core/engagements/*`) without an explicit `--classification confidential:<engagement>`. Default `internal` for product-shaped paths (`Core/products/*`).
5. Append to `Core/products/products.json` (or `Core/engagements/engagements.json` for `confidential:*`-tier work).
6. Witness registration logic:
   - `public` or `internal` tier → append to `Core/products/witness/.intent/registered-products.yaml` Day 1 (federation ON).
   - `confidential:*` tier → NOT appended to Witness registry Day 1. Federation deferred to Phase 2. Conservation-law-respecting default.
7. Echo classification + federation status so the operator sees what just happened.

**Companion artifacts:** `Core/products/witness/.intent/registered-products.yaml` (per-product registration with classification tier preserved — internal tier only Day 1) and `<product>/.intent/classification.yaml` (universal per-product classification declaration, read by the Track A substrate-exposure MCP on every query to apply binary scope enforcement Day 1; read again in Phase 2 to apply shaped-view substitutions from per-engagement redaction-maps).

**Rationale:** Reduces per-product cost from ~6 minutes manual + ~2 minutes Witness registration to ~30 seconds single command. Sibling of the existing `bin/` family (`bin/intent-knowledge` planned per E3 track, `bin/lib/id_gen.sh` already shipping). Explicit registration matches WS-DDR-025's structural commitments — sibling composition with declared interfaces. **Tier-aware scaffold Day 1, engagement federation deferred (D5-refined):** every product gets a classification declaration at birth. The structural commitment to multi-consumer substrate is honored Day 1 — but Witness federation for confidential-tier substrate waits until Phase 2 because Witness's append-only conservation law makes "put it in and figure scope out later" a non-recoverable mistake. Confidentiality is declared, not inferred. No refactor cost later: when Brien needs chat-surface query against an engagement substrate, the work is (a) author the engagement's `redaction-map.yaml` (~30 min one-time); (b) flip the engagement's Witness-registration switch on (one config line); (c) the already-built tier-aware MCP server picks up the engagement-scope token. No code change.

**Consequences:** Spinning up a new product becomes a 30-second operation. Lowers the activation cost of new product creation — encourages signal-rich product proliferation in line with the methodology. Tier 2 registration becomes auditable (the yaml is git-tracked, decisions about which products federate are recorded). Cost: one CLI to maintain. Bash or Python; recommend Python for portability. Risk: products.json schema evolution; mitigation: products.json already has manual-curation discipline; one more writer is not a structural risk.

**Validation criteria:** Validated when (1) `bin/intent-init my-new-product --path Core/products/my-new-product/ --enable entire,events --register-with witness` succeeds end-to-end; (2) the product gets a working Tier 1 setup (verifiable via `tail -1 .intent/events/events.jsonl` after a test session); (3) the Witness registered-products.yaml gets a correctly-shaped entry; (4) `Core/products/products.json` gets a correctly-shaped entry; (5) Tier 2 federation activates once `engine/adapters/entire-io.py` lands (independent track, WIT-004 #5).

**Related:** WS-DDR-099 (substrate exposure — Track A sibling), DEC-010 (intent-knowledge MCP scope extension — Track A sibling), DEC-009 (Entire scoped as authoring provenance — upstream), WIT-004 #5 (`engine/adapters/entire-io.py` stub completion — Tier 2 dependency), `Core/frameworks/coherence-engineering/principles/architecture-first-content-sequenced.md` (this DEC is one of the six analog instances of the principle — the scaffold CLI declares all four classification tiers + Witness-federation hook on Day 1; engagement-tier federation is content-only deferral, not architectural), `Core/frameworks/intent/.intent/signals/2026-05-26-architecture-first-content-sequenced-pattern.md` (establishing signal — names DEC-011 explicitly as instance evidence).

**Supporting evidence:** `/Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/02-track-b-spawn-a-product-runbook.md`

---

## Where Decisions Live

- **Source files:** `.intent/decisions.md` in each Intent-native repo
- **Event emitted:** `decision.recorded` (manual emission)
- **Site page:** rendered at theparlor/intent-site <!-- broken link removed: ../docs/decisions.html (site moved to separate repo per CLAUDE.md; this repo has no docs/) -->
