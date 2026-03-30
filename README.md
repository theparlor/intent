---
title: Readme
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-29
technologies:
  - jira
thought_leaders:
  - marty-cagan
  - jeff-patton
  - teresa-torres
  - josh-seiden
depth_score: 4
depth_signals:
  file_size_kb: 3.9
  content_chars: 3046
  entity_count: 5
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 1.97
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 571, strength: 0.387}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 558, strength: 0.378}
  - {pair: consulting-operations ↔ engagement-management, count: 483, strength: 0.327}
  - {pair: consulting-operations ↔ turnberry, count: 321, strength: 0.201}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.17}
---
# Intent

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

## This Repo Eats Its Own Dogfood

The directory structure *is* the loop:

```
notice/          ← Signals, observations, raw inputs that started this work
spec/            ← Shaped specifications: the methodology, the ops layer, the product concept
execute/         ← Implementation artifacts (where built things live)
observe/         ← Verification findings, quality reviews, learnings
artifacts/       ← Visual and interactive materials
TASKS.md         ← The living backlog (replaces Jira)
```

---

## Where Intent Sits

| Layer | What It Solves | Examples |
|-------|---------------|----------|
| **Team Operating Model** | How the team flows, decides, and learns | **Intent** ← this |
| **Spec-Driven Development** | How specs become code via AI agents | GitHub Spec Kit, Kiro, Tessl |
| **AI Coding Assistants** | How individuals get AI help | Copilot, Claude Code, Cursor |

Intent is the missing top layer.

---

## Interactive Artifacts

- **[Intent Visual Brief](artifacts/intent-visual-brief.jsx)** — Seven-section interactive product brief (Problem cascade, Core Loop, Stack, Personas, GTM, Hypotheses, Competitive)
- **[Intent-Native Repos](artifacts/intent-native-repos.jsx)** — How to adopt Intent across repos: template structure, adoption tiers, and the Entire.io → Spec feedback loop

**Documentation & marketing site:** [theparlor.github.io/intent-site](https://theparlor.github.io/intent-site/) (separate repo: [theparlor/intent-site](https://github.com/theparlor/intent-site))

---

## Status

**Stage:** Idea → ready for validation  
**Approach:** Thought leadership first, methodology product second, tooling conditional on validation  
**Next step:** 5 in-depth interviews with teams experiencing AI + Agile friction

---

## Origin

Designed in a Cowork session on 2026-03-28, triggered by a conversation with engineer Ari about how AI collapses Agile Scrum. Grounded in Cagan (product operating model), Patton (story mapping), Torres (continuous discovery), and Seiden (outcomes over outputs).

---

*Private repo. Will open when the manifesto is ready.*
