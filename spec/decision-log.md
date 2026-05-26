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
depth_score: 4
depth_signals:
  file_size_kb: 7.1
  content_chars: 6534
  entity_count: 2
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.31
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

---

## Where Decisions Live

- **Source files:** `.intent/decisions.md` in each Intent-native repo
- **Event emitted:** `decision.recorded` (manual emission)
- **Site page:** rendered at theparlor/intent-site <!-- broken link removed: ../docs/decisions.html (site moved to separate repo per CLAUDE.md; this repo has no docs/) -->
