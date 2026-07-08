---
id: SIG-001
date: 2026-03-28
source: cowork-session
confidence: high
related_intents: []
status: resolved
upstream_control_path: ".intent/intents/ (17 populated), .intent/specs/, .intent/templates/, CLAUDE.md Work Ontology section"
catch_mechanism: "CLI suite (bin/intent-signal, bin/intent-intent, bin/intent-spec) enforces the hierarchy at creation time; DEC-INTENT-001 through DEC-INTENT-008 ratify the founding framing"
verification_command: "ls /Users/brien/Workspaces/Core/frameworks/intent/.intent/intents/ | wc -l"
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

## Triage, 2026-07-08

Disposition: control exists now. The Signal, Intent, Spec levels of the proposed hierarchy are fully operational (populated .intent/intents/ and .intent/specs/ directories, CLI tools that create each type). Contract, Capability, Feature, and Product did not materialize as separate file types; the ontology settled on a lighter three-tier chain (Signal, Intent, Spec) plus decisions.md and DEC-INTENT-NNN atoms for the verification layer that "Contract" was meant to cover. That is a legitimate simplification, not an open gap: CLAUDE.md's own "Work Ontology (7 levels)" section still lists all seven for reference, but only the first three needed dedicated tooling because the framework stayed solo-practitioner scoped.
