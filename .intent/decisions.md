# Decision Log

## 2026-03-28 — Product named "Intent"

**Context:** Working name was "Dev OS" throughout initial development. Sounded like DevOps infrastructure tooling, which confused the positioning.
**Alternatives considered:** Frame, Premise, Lucid, Upstream, "Intent Operating Flow"
**Decision:** Single word "Intent" — names exactly what the layer produces. One word, like Entire.io.
**Why:** The product IS intent — the layer where teams crystallize why they're building what they're building. The name should be the thing, not a metaphor for the thing.
**Source:** Cowork session 2026-03-28

## 2026-03-28 — Three-layer stack positioning

**Context:** Needed to clarify where Intent sits relative to existing tools (Kiro, GitHub Spec Kit, Claude Code, etc.)
**Decision:** Intent sits ABOVE spec-driven dev tools, which sit above AI coding assistants. Entire.io is the observability layer that runs alongside all three.
**Why:** Existing tools handle spec→code and code execution. Nobody owns the "why are we building this" layer. That's the gap.
**Source:** Cowork session 2026-03-28, concept brief development

## 2026-03-28 — Dogfood the repo structure

**Context:** How should the Intent methodology repo itself be organized?
**Decision:** Mirror the Notice → Spec → Execute → Observe loop as top-level directories
**Why:** The medium is the message. If the methodology is a loop, the repo should be a loop. Also serves as the reference implementation for other teams adopting Intent.
**Source:** Cowork session 2026-03-28

## 2026-03-28 — Staged GTM over tooling-first

**Context:** Should Intent be a SaaS tool, a methodology, or a consulting offering?
**Decision:** Stage it: thought leadership (manifesto + case studies) → methodology product (playbook + workshops) → tooling (conditional on validation)
**Why:** Building tooling before validating the methodology is premature. Brien is a solo practitioner — the highest-leverage move is content + interviews, not code.
**Quality flags:** GTM timeline may be optimistic for solo practitioner. Need 5 in-depth interviews with teams struggling with AI + Agile friction before committing to tooling investment.
**Source:** Concept brief quality review, Cowork session 2026-03-28

## 2026-03-28 — Ari conversation as primary evidence

**Context:** Needed empirical validation beyond Cagan/Patton/Torres theory
**Decision:** Ari's team experience is Case Study #0 — a real team that discovered the pattern independently
**Why:** Theory says discovery is the bottleneck. Ari's team proved it: their tickets became "specifications for bots to run," their refinement became "heavily design oriented," and their PRDs moved outside Jira.
**Source:** Brien's conversation with engineer Ari, captured in notice/ari-conversation.md

## 2026-03-28 — Rename all references from "Dev OS" to "Intent"

**Context:** After naming decision, needed consistency across all files, GitHub repo, and local workspace
**Decision:** Comprehensive rename: repo name, file names, file contents, memory files, cross-references
**Challenges:** GitHub API doesn't support file deletion or rename (git mv). Required CLI cleanup script for stubs and renames. 68KB JSX file successfully pushed through API despite size concerns.
**Source:** Cowork session 2026-03-28, commit history in theparlor/intent
