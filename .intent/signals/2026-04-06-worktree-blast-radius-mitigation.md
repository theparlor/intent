---
id: SIG-032
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.95
trust: 0.85
autonomy_level: L4
status: active
cluster: autonomous-infrastructure
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-012
---
# Worktree/blue-green development patterns should feed trust scoring as a reversibility modifier

## Observation

During persona system design, Brien identified that the trust scoring formula treats reversibility as a property of the *change itself* (can this be undone?) but ignores the *development pattern* (where is this change being made?). A change developed in a git worktree or blue/green branch is fundamentally more reversible than the same change made in-place, regardless of what the change does.

Current formula: `trust = clarity × 0.30 + (1/blast_radius) × 0.20 + reversibility × 0.20 + testability × 0.20 + precedent × 0.10`

The reversibility and blast_radius factors should incorporate a **deployment context modifier**:
- In-place edit on main: baseline (no modifier)
- Feature branch: reversibility +0.1, blast_radius ×0.5
- Git worktree (isolated copy): reversibility +0.2, blast_radius ×0.25
- Blue/green parallel environment with full UAT: reversibility → 0.95 floor, blast_radius → near-zero

## Implication

This is a meta-finding about Intent's trust model. If the development infrastructure itself mitigates blast radius, then the autonomy level for *all code changes* can be higher — not by lowering standards, but by making mistakes cheaper to examine and roll back. This creates a positive feedback loop: better infrastructure → higher trust → more autonomous execution → faster development → which funds more infrastructure investment.

The practical consequence: if we adopt worktree-based development as the default pattern for Intent-driven coding, most signals that would score L2 (agent decides, human approves) can legitimately score L3 (agent executes, human monitors), because the approval is replaced by post-merge review of an isolated, examinable change.

## Design Constraint

- The modifier must be verifiable (is this actually in a worktree? is the branch actually isolated?)
- The modifier applies to the trust formula, not to the autonomy level directly — the level is still derived from the score
- This should NOT reduce scrutiny of *what* is built — only *where* it's built during development
