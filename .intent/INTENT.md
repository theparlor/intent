---
name: Intent
purpose: Define and dogfood the Intent methodology — a team operating model for AI-augmented product teams
loop-phase: observe
owner: Brien
spec-source: spec/
observe-via: entire
created: 2026-03-28
---

# Intent

> A team operating model for AI-augmented product teams.
> When AI collapses implementation to hours, the bottleneck shifts from delivery to discovery.
> Intent is the methodology that makes that shift legible and manageable.

## Why This Repo Exists

Agile was designed around a core assumption: implementation is the bottleneck. Sprints, velocity tracking, daily standups — all of it coordinates human effort around the slow, expensive act of building software. When AI agents can implement a well-specified feature in hours, that assumption breaks. The ceremonies become overhead. The hard problem was always discovery — Cagan has been saying this for years — but AI made it undeniable.

This repo is the canonical home for the Intent methodology: a spec-driven operating model built around a continuous loop of **Notice → Spec → Execute → Observe**. It serves two purposes: it documents the methodology, and it dogfoods the methodology by using its own directory structure as the loop.

## Origin

Brien developed Intent on 2026-03-28 after a conversation with engineer Ari, who described how their team empirically discovered the same pattern: tickets became bot specifications, refinement meetings became design sessions, and PRDs moved outside Jira because the tool was optimizing for tracking status, not communicating intent.

The methodology is grounded in Cagan (product discovery over delivery), Patton (story mapping over backlog grooming), Torres (continuous discovery), and Seiden (outcomes over outputs).

## Current Shape

The repo mirrors the Intent loop:

- `notice/` — raw signals, conversations, observations that sparked this work
- `spec/` — the methodology spec, concept brief, autonomous operations design
- `execute/` — (thin — execution happens in other repos that adopt the methodology)
- `observe/` — review findings, quality critiques, what we're learning
- `artifacts/` — visual brief (interactive React component), presentation-ready material
- `reference/` — supporting docs

## Active Contracts

- The methodology spec (`spec/intent-methodology.md`) is the canonical document
- The concept brief (`spec/intent-concept-brief.md`) positions Intent as a product
- The visual brief (`artifacts/intent-visual-brief.jsx`) is the interactive pitch artifact
- All content uses "Intent" naming consistently (renamed from "Dev OS" on 2026-03-28)

## Stack Position

```
Intent          — how the team decides what to build and why (this repo)
Spec-Driven Dev — Kiro, GitHub Spec Kit, Tessl (spec → code)
AI Coding       — Claude Code, Copilot, Cursor (execution)
Entire.io       — agent observability (reasoning traces)
```

## What Success Looks Like

1. Brien's personal workflow runs on Intent daily (Case Study #1)
2. The methodology is clear enough that another practitioner can adopt it from the docs alone
3. The concept brief attracts interest from teams experiencing the Agile + AI friction
4. Quality review flags from 2026-03-28 are addressed (competitive differentiation, GTM realism, operationalized metrics for spec quality)
