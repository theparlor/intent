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
  file_size_kb: 5.4
  content_chars: 4688
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.21
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 791, strength: 0.426}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 769, strength: 0.416}
  - {pair: consulting-operations ↔ engagement-management, count: 498, strength: 0.269}
  - {pair: consulting-operations ↔ turnberry, count: 448, strength: 0.224}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.136}
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

## Where Signals Live

- **Source files:** `.intent/signals/` in each Intent-native repo
- **Naming:** `YYYY-MM-DD-slug.md`
- **Event emitted:** `signal.created` (via GitHub Action on PR merge)
- **Site page:** [signals.html](../docs/signals.html)
