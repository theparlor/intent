---
id: SIG-001
timestamp: 2026-03-28T12:00:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.15
autonomy_level: L0
status: active
cluster: work-ontology-design
parent_signal:
related_intents: []
---
# Signal: Intent needs a formal work ontology

## Observation

The Intent methodology defines the loop (Notice → Spec → Execute → Observe) and the toolchain, but lacks a formal decomposition of work units. Without this, there's no answer to "what replaces tickets?" — the most common question any team adopting Intent will ask.

## Evidence

During Cowork session on 2026-03-28, the question surfaced naturally: "what are our atomic replacements for tickets, stories, tasks, subtasks so that a multitude of agents can build and pull from an intent driven list?"

## Proposed Hierarchy

- Signal → replaces idea/bug report/request
- Intent → replaces epic/initiative (outcome with hypothesis)
- Spec → replaces user story (declarative behavior description)
- Contract → replaces task/subtask/acceptance criteria (verifiable interface agreement — the true atom)
- Capability → replaces component/service (reusable building block)
- Feature → replaces story map column (composed capabilities delivering value)
- Product → replaces program/portfolio (living system of features)

## Key Insight

The atomic unit shifts from "unit of human labor" to "declarative state description agents can execute against." Contracts are done when assertions pass, not when cards move.
