---
id: RETRO-2026-04-13-approval-gradient-SIG-1
type: signal
category: architecture-insight
severity: medium
source: session-synthesis
detected: 2026-04-13
topic: approval-gradient
status: resolved
upstream_control_path: "Core/frameworks/intent/CLAUDE.md, section 'Three Human-Contact Patterns'"
catch_mechanism: "documentation is the control here (a framing/positioning ask, not a runtime gate); CLAUDE.md is the mandatory dev-continuity entry point read before any agent touches this repo, per its own 'Agent Handoff Protocol' section"
verification_command: "grep -n 'Three Human-Contact Patterns' -A3 Core/frameworks/intent/CLAUDE.md"
related:
  - SPEC-APPROVAL-GATE
  - RETRO-2026-04-13-codelayer-pivot-SIG-1
status: open
---

# Two Complementary Gate Systems: Phase Gates vs Action Gates

## Signal

This session revealed that Intent has two distinct gate systems operating on different axes:

1. **Phase gates** (existed before this session): Human reviews at Notice→Spec and Spec→Execute transitions. Spec-shaping protocol (4-persona interrogation). Trust scoring. These prevent building the wrong thing.

2. **Action gates** (built this session): L0 approval entities for external communication during Execute. The gate skill. These prevent saying the wrong thing.

CodeLayer's pivot from per-tool approval to per-phase review validates that phase gates are higher leverage. But action gates remain necessary for irreversible external actions.

## Evidence

- CodeLayer abandoned tool-level approval in favor of phase-level review — the pivot itself is evidence
- Intent's spec-shaping protocol already places the high-leverage gate at spec time, not execution time
- Brien's L0 rule targets external actions specifically, not all execution
- The approval gate is a safety net within Execute, not the primary quality mechanism

## Implication

These two systems should be documented as complementary, not competing. The phase gate is the quality mechanism. The action gate is the safety mechanism. Both are needed, but they serve different purposes and operate at different granularities.

When explaining Intent's governance model, lead with phase gates (higher leverage), then introduce action gates (safety net for irreversible externalities).

## Triage, 2026-07-08

Disposition: control exists now, verified live. `Core/frameworks/intent/CLAUDE.md` under "Three Human-Contact Patterns" states exactly this distinction: phase gates (Notice to Spec transition) are mandatory and prevent building the wrong thing, and action gates (L0 approval) are mandatory and prevent saying the wrong thing, plus the third voluntary pattern (`request_human_input`). This is the framework's dev-continuity entry point, read first by any agent picking up the repo, so the documentation goal this signal asked for is met at the right altitude.
