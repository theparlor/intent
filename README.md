---
title: Readme
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-29
updated: 2026-05-20
version: 0.11.0
technologies:
  - jira
thought_leaders:
  - marty-cagan
  - jeff-patton
  - teresa-torres
  - josh-seiden
frameworks:
  - product-operating-model
  - outcomes-over-output
depth_score: 4
depth_signals:
  file_size_kb: 4.9
  content_chars: 3701
  entity_count: 7
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 1.89
related_entities:
  - {pair: marty-cagan ↔ teresa-torres, count: 185, strength: 0.371}
  - {pair: jeff-patton ↔ teresa-torres, count: 121, strength: 0.32}
  - {pair: jeff-patton ↔ marty-cagan, count: 121, strength: 0.271}
  - {pair: marty-cagan ↔ product-engineering-coaching, count: 96, strength: 0.089}
  - {pair: coaching-methodology ↔ marty-cagan, count: 92, strength: 0.089}
architecture: sibling-composable
pipeline_position: team-operating-model
known_siblings:
  - Shape Up team model (Basecamp)
  - Scrum (Ken Schwaber / Jeff Sutherland)
  - bespoke team operating docs (per-company)
port_contract: "consumes signals from practitioner surfaces; produces specs + contracts + events consumable by execute-layer tooling (Spec Kit, Kiro, Copilot, Claude Code)"
---
# Intent — v0.11.0

> A team operating model for AI-augmented product teams.

When AI collapses implementation from weeks to hours, the bottleneck moves upstream — from *delivery* to *discovery, specification, and observation*. Agile ceremonies built for slow, expensive delivery become overhead. The team's operating model needs to change.

Intent is that operating model.

---

## The Core Loop

```
NOTICE  →  SPEC  →  EXECUTE  →  OBSERVE  →  (back to NOTICE)
```

No sprint boundaries. No ceremony tax. A continuous loop where the team's energy follows the highest-leverage work:

| Phase | What Happens | Replaces |
|-------|-------------|----------|
| **Notice** | Sense signals — user feedback, system patterns, market shifts | Backlog grooming |
| **Spec** | Shape into Intent → Shape → Contract (the full team collaborates) | Sprint planning + ticket writing |
| **Execute** | Humans + AI agents build against the spec | Sprint execution |
| **Observe** | Verify outcomes against reality, feed learnings back | Sprint review + retro |

---

## Three-Layer Architecture

Intent prescribes three independently useful layers:

| Layer | Purpose |
|---|---|
| **Compiled Knowledge Base** | Raw sources compiled into durable domain knowledge (personas, journeys, DDRs, models) |
| **Transformation OS** | The Notice→Spec→Execute→Observe engine with trust scoring, autonomy levels, and event stream |
| **Software Spec & Code** | Agent-ready specs, verifiable contracts, and running implementation |

Six bidirectional flows couple the layers. The double-loop (Observe → Knowledge) questions assumptions, not just optimizes.

Full architecture: `ARCHITECTURE.md`

---

## This Repo Eats Its Own Dogfood

The directory structure *is* the loop:

```
.intent/         ← Signals, intents, specs, contracts, events (130+ signals captured)
spec/            ← Shaped specifications: methodology, trust framework, enforcement specs
learnings/       ← IDD playbook, cross-product applicability, process drift catalog
hooks/           ← 8 governance hooks (autonomy-grant, closure-discipline, overwatch)
spawn-prompts/   ← 8 reusable handoff prompts for governance and build operations
```

---

## Where Intent Sits

Intent fills a distinct pipeline position — one not currently occupied by any existing product category. The table below renders a signal-propagation ordering (each position produces artifacts the adjacent position reads), not a containment hierarchy.

| Position | What It Solves | Examples (siblings at this position) |
|----------|---------------|--------------------------------------|
| **Team Operating Model** | How the team flows, decides, and learns | **Intent** ← this (siblings: Shape Up team model, Scrum, bespoke team OS) |
| **Spec-Driven Development** | How specs become code via AI agents | GitHub Spec Kit, Kiro, Tessl |
| **AI Coding Assistants** | How individuals get AI help | Copilot, Claude Code, Cursor |

Intent is the currently-unfilled position in that pipeline. It is not "above" the other two — it composes with them at declared handoffs. See `Workspaces/.context/DECISIONS.md` (WS-DDR-025) for the sibling-over-parent-child default.

---

## Governance Infrastructure (v0.11.0)

Intent's build-discipline layer is operational as of v0.11.0:

**IDD Build Discipline** — 7-stage loop with DoR/DoD gates. Canonical playbook: `learnings/idd-playbook.md`. Cross-product map: `learnings/idd-cross-product-applicability.md`.

**Process Drift Catalog** — 4 families, 17 entries covering every recurring AI-agent drift pattern observed across the Intent system. `learnings/process-drift-catalog.md`. New in v0.11.0: `1.7 — Artificial-gate-architecture drift` and `4.7 — Governance-skill-without-trigger`.

**5-Layer Autonomy-Grant Enforcement** — Prevents L4-eligible work from being converted to L0 proposals. Spec: `spec/autonomy-grant-enforcement.md`. Hooks: `autonomy-grant-check.sh` (SessionStart), `autonomy-grant-stop-check.sh` (Stop), `autonomy-grant-dispatch-prompt-check.sh` (PreToolUse).

**5-Layer Closure-Discipline Enforcement** — Requires upstream control before `status: resolved`. Spec: `spec/closure-discipline-enforcement.md`. Hooks: `closure-discipline-check.sh` (SessionStart), `closure-discipline-stop-check.sh` (Stop), `closure-discipline-signal-check.sh` (PreToolUse).

**Overwatch Staleness Hook** — SessionStart banner when latest overwatch journal is >7 days (warn) or >14 days (load-bearing posture). `hooks/overwatch-staleness-check.sh`.

---

## Interactive Artifacts

- **[Intent Visual Brief](artifacts/intent-visual-brief.jsx)** — Seven-section interactive product brief (Problem cascade, Core Loop, Stack, Personas, GTM, Hypotheses, Competitive)
- **[Intent-Native Repos](artifacts/intent-native-repos.jsx)** — How to adopt Intent across repos: template structure, adoption tiers, and the Entire.io → Spec feedback loop

**Documentation & marketing site:** [theparlor.github.io/intent-site](https://theparlor.github.io/intent-site/) (separate repo: [theparlor/intent-site](https://github.com/theparlor/intent-site))

---

## Status

**Version:** 0.11.0 (2026-05-20)
**Stage:** Idea → ready for validation
**Approach:** Thought leadership first, methodology product second, tooling conditional on validation
**Governance infrastructure:** Operational — 8 hooks, 8 spawn prompts, IDD playbook, 4-family drift catalog
**Next step:** 5 in-depth interviews with teams experiencing AI + Agile friction

---

## Origin

Designed in a Cowork session on 2026-03-28, triggered by a conversation with engineer Ari about how AI collapses Agile Scrum. Grounded in Cagan (product operating model), Patton (story mapping), Torres (continuous discovery), and Seiden (outcomes over outputs).

---

*Private repo. Will open when the manifesto is ready.*
