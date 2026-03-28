# Session Origin — 2026-03-28

> How this work started. A broken nightly pipeline escalated through three natural design expansions.

---

## The Trigger

Started with a broken nightly pipeline — a git lock file in Cowork's sandboxed VM. The Library Index nightly refresh ran successfully but couldn't complete git commit/push because the sandbox doesn't have write access to `.git`.

## The Escalation

What began as a bug fix expanded through three design layers:

### 1. Autonomous Operations Layer (spec written)
Designed a three-layer architecture (Pipeline / Orchestrator / Intelligence) to migrate automated workflows from Cowork's sandbox to Claude Code CLI running natively.

### 2. Development Operating System (spec written)
Emerged from Brien's conversation with Ari. Core insight: when implementation takes hours, the entire SDLC gravity shifts left toward strategy, design, and specification. The loop: Notice / Spec / Execute / Observe.

### 3. Product Concept (brief written)
Dev OS as a potential product for AI-augmented practitioners and small teams. Defines the problem statement, target audience, competitive landscape, and staged GTM.

## Key Decisions Made

- Jira dropped for personal dev work (kept for client-facing)
- Spec-driven development adopted: Intent / Shape / Contract
- TASKS.md replaces backlog; Git + Entire.io replaces status tracking
- Toolchain: NotebookLM (research), Cowork (shaping), Claude Code CLI (execution), Entire.io (observation)
- Kiro noted as potential IDE layer (spec-driven model aligns architecturally)

## Connected Resources

- Ari conversation: `notice/ari-conversation.md`
- Methodology spec: `spec/development-operating-system.md`
- Operations spec: `spec/autonomous-operations-design.md`
- Product concept: `spec/dev-os-concept-brief.md`
