---
title: DoR / DoD Library — Canonical Reusable Definitions
id: TEMPLATE-DOR-DOD-LIBRARY
type: library
created: 2026-04-14
updated: 2026-04-14
depth_score: 4
depth_signals:
  file_size_kb: 21.7
  content_chars: 19585
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.15
version: 1.00
status: canonical
origin: brien-original
related_signals:
  - SIG-045
  - SIG-046
related_templates:
  - dor.md
  - dod.md
---
# DoR / DoD Library

> Canonical, reusable Definitions of Ready and Done for Brien's most common work types. Load the applicable entry at the start of any build, spec, engagement, or enrichment pass. Extend with custom conditions specific to the current work; do not override without a recorded decision.

---

## How to Use This Library

1. **Identify your work type** from the catalog below.
2. **Load the DoR** at the start of the work (CATCH phase in skill-intake, before any execution).
3. **Verify every DOR item** before proceeding. If any are unmet, surface them to Brien or resolve them before building.
4. **Load the DoD** at the close of the work (DEPLOY GATE phase in skill-intake).
5. **Verify every DOD item** before declaring complete. If any are unmet, list what's needed — do not mark complete.
6. **Add work-specific custom conditions** to the DoR/DoD blocks in the spec itself. The library entries are the floor, not the ceiling.

---

## Work Type Index

| Work Type | DoR | DoD |
|-----------|-----|-----|
| [Skill Build](#skill-build) | DOR-SKB-001 – 006 | DOD-SKB-001 – 006 |
| [Spec Authoring](#spec-authoring) | DOR-SPC-001 – 004 | DOD-SPC-001 – 005 |
| [Plan Authoring](#plan-authoring) | DOR-PLN-001 – 005 | DOD-PLN-001 – 006 |
| [Engagement Kickoff](#engagement-kickoff) | DOR-EKO-001 – 005 | DOD-EKO-001 – 005 |
| [Engagement Closure](#engagement-closure) | DOR-ECL-001 – 004 | DOD-ECL-001 – 005 |
| [Persona Enrichment Pass](#persona-enrichment-pass) | DOR-PEP-001 – 004 | DOD-PEP-001 – 06 |
| [Critique Panel](#critique-panel) | DOR-CPL-001 – 04 | DOD-CPL-001 – 05 |
| [Signal Closure](#signal-closure) | DOR-SCL-001 – 03 | DOD-SCL-001 – 05 |
| [YAML-Emitting Stage](#yaml-emitting-stage) | DOR-YML-001 – 02 | DOD-YML-001 – 03 |

---

## Skill Build

> Use for any new skill, plugin, command, or composable system being built into the skills-engine. Activates via skill-intake internal-build mode.

### Definition of Ready — Skill Build

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-SKB-001 | Composition audit completed; request classified as extend / compose / new+compose / true-new / don't-build | `composition-audit.md` or equivalent artifact exists at skill directory or session notes | Yes | agent |
| DOR-SKB-002 | Target git repository identified and confirmed initialized | `git status` or `git log` succeeds in target repo path | Yes | agent |
| DOR-SKB-003 | Deployment plan documented: target directory, category, skill name, registration path | Declared in spec INTENT.md or session-captured decision | Yes | both |
| DOR-SKB-004 | Architecture decision locked (extend vs. compose vs. new) — Brien's pick recorded if non-obvious | Decision recorded in session or `.intent/decisions.md` | Yes | both |
| DOR-SKB-005 | Budget declared: ceiling estimate and model allocation (Sonnet vs. Opus) | Ceiling stated in spec or session | No | brien |
| DOR-SKB-006 | DoD for this build is declared and understood | DoD block populated in spec (or this library entry loaded) | Yes | agent |

### Definition of Done — Skill Build

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-SKB-001 | All code/files committed to managed git repo — NOT orphaned in Workspaces | `git log --oneline -- [skill-path]` shows commit | Yes | agent |
| DOD-SKB-002 | Skill registered and discoverable: SKILL.md exists at canonical path in skills-engine | `Glob platforms/claude-code/**/[skill-name]/SKILL.md` returns file | Yes | agent |
| DOD-SKB-003 | CONTEXT.md present at skill directory or category level | File exists | Yes | agent |
| DOD-SKB-004 | Memory updated if skill is load-bearing or process-changing | Memory file exists OR explicit "n/a — not load-bearing" declared | Yes | both |
| DOD-SKB-005 | At least one composition scenario tested: skill invoked with realistic input, output verified | Test output documented in session or `composition-test-[skill]-[date].md` | Yes | both |
| DOD-SKB-006 | Signal captured if this skill changes how Brien works or resolves an active signal | Signal file exists OR explicit "n/a — no signal" declared with reason | Yes | agent |

---

## Spec Authoring

> Use when authoring a new SPEC-NNN or major revision to an existing spec in the Intent framework.

### Definition of Ready — Spec Authoring

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-SPC-001 | Parent intent (INT-NNN) exists and is accepted | `intent-intent show INT-NNN` returns status `accepted` | Yes | agent |
| DOR-SPC-002 | Related existing specs reviewed — no duplicate spec being authored | Agent has read all `SPEC-NNN` files in adjacent domain | Yes | agent |
| DOR-SPC-003 | Contract numbering scheme confirmed: next CON-NNN known | `grep -r "CON-" .intent/specs/` scan completed; next ID confirmed | Yes | agent |
| DOR-SPC-004 | Applicable DoR/DoD library entries loaded for the work type this spec governs | This file consulted; work-type entry copied into spec | Yes | agent |

### Definition of Done — Spec Authoring

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-SPC-001 | All contracts (CON-NNN) are numbered and have explicit verification methods | Every CON-NNN in the spec has `verification_method` field populated | Yes | agent |
| DOD-SPC-002 | Quality gates table complete with verifiable criteria (not prose assertions) | Quality gates section present with checkable conditions | Yes | agent |
| DOD-SPC-003 | Failure modes documented: at least the top 3 ways this spec can fail | Failure modes section present | Yes | agent |
| DOD-SPC-004 | DoR and DoD blocks present in spec (not just referenced to library) | Both sections present in spec body | Yes | agent |
| DOD-SPC-005 | Spec status set to `approved` by Brien or assigned status `agent-approved` for L3+ work | Frontmatter `status` field is `approved` | Yes | brien |

---

## Plan Authoring

> Use when authoring a new PLAN-NNN or major revision to an existing plan. Activates per `Core/frameworks/intent/spec/plan-artifact-convention.md` (SPEC-PLAN-001) + Annex A. Plans are sibling to specs — a plan answers *how/when*, a spec answers *what/why*.

### Definition of Ready — Plan Authoring

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-PLN-001 | Source spec exists with `status: accepted` (or explicit `TBD — spec pending` placeholder + `SIG-PLAN-NO-SPEC` emitted per SPEC-PLAN-001 §2.1.1) | `source_spec:` field in plan frontmatter resolves to extant spec file | Yes | agent |
| DOR-PLN-002 | Phase structure decided: phased (per Annex A §3) or flat. Phased plans declare phase count + checkpoint criteria. | Plan body declares phase count or notes flat structure | Yes | agent |
| DOR-PLN-003 | Budget declared: model allocation per phase (Sonnet vs. Opus), expected wall-time, expected token cost. Surface to Brien if estimate exceeds 10% of weekly bucket per autonomy-grant L2. | Budget block populated in plan body or session notes | Yes | both |
| DOR-PLN-004 | Applicable DoR/DoD library entries loaded for work types the plan executes (e.g., if plan dispatches sub-agents for spec authoring, DOR-SPC-001 et al loaded) | This file consulted; relevant entries cited in plan dependencies | Yes | agent |
| DOR-PLN-005 | Dependencies identified: other plans (PLAN-IDs), signals whose resolution is prerequisite, external systems or approvals needed | Dependencies section populated | Yes | agent |

### Definition of Done — Plan Authoring

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-PLN-001 | All tasks completed OR formally deferred with documented rationale (no silent skips) | Every `- [ ]` checkbox is `- [x]` OR a `Deferred — see <signal-id>` annotation | Yes | agent |
| DOD-PLN-002 | If plan is phased: every phase-checkpoint block satisfied per Annex A §3.2 (verification items checked, artifacts produced, handoff signal emitted) | Each `### CHECKPOINT — Phase N` block has all `- [ ]` verifiation items as `- [x]` and handoff signal file exists | Yes (if phased) | agent |
| DOD-PLN-003 | Signals emitted at appropriate paths per task instructions; signal status fields are honest per closure-DoD (`resolved` only with installed upstream control + catch-net + pipeline survival) | Signal files exist at declared paths; status fields satisfy closure-DoD | Yes | agent |
| DOD-PLN-004 | Handoff section populated (or marked `N/A — single-session plan` for non-multi-session plans) | Handoff section present and non-empty | Yes | agent |
| DOD-PLN-005 | Rollback section populated (or marked `additive-only — no rollback needed`) per SPEC-PLAN-001 §2.1.2 | Rollback section present and non-empty | Yes | agent |
| DOD-PLN-006 | Plan status updated to `completed`, `abandoned`, or `deferred` per SPEC-PLAN-001 §2.1.1 lifecycle. Retro signal filed if appropriate. | Frontmatter `status` field is terminal value; if `abandoned` or `deferred`, reason in plan body + signal filed | Yes | brien-or-agent |

---

## Engagement Kickoff

> Use at the start of any new consulting, advising, or research engagement.

### Definition of Ready — Engagement Kickoff

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-EKO-001 | Scope clear: engagement objectives, deliverable types, and timeframe stated | ENGAGEMENT_INDEX.md exists with scope section | Yes | brien |
| DOR-EKO-002 | Stakeholders mapped: primary contacts, decision-makers, and communication channels identified | Stakeholder list in ENGAGEMENT_INDEX.md | Yes | brien |
| DOR-EKO-003 | Budget declared: rate, hours-cap, billing structure | Financial terms in ENGAGEMENT_INDEX.md or financials/ | Yes | brien |
| DOR-EKO-004 | Working folder structure created per Workspaces convention | `Work/Consulting/Engagements/[Client]/` exists with standard subdirs | Yes | agent |
| DOR-EKO-005 | Placement resolver consulted: `Workspaces/AGENTS.md` Engagement Scope Test applied | Agent has read AGENTS.md for this engagement setup | Yes | agent |

### Definition of Done — Engagement Kickoff

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-EKO-001 | `from-client/` directory exists and contains original client materials (immutable) | Directory exists; files present if originals received | Yes | agent |
| DOD-EKO-002 | `working/` directory initialized for in-progress artifacts | Directory exists | Yes | agent |
| DOD-EKO-003 | `deliverables/` directory scaffolded | Directory exists | Yes | agent |
| DOD-EKO-004 | `knowledge/CONTEXT.md` written with engagement schema | File exists with schema populated | Yes | agent |
| DOD-EKO-005 | `ENGAGEMENT_INDEX.md` exists at engagement root | File exists with at minimum scope + contacts + folder map | Yes | agent |

---

## Engagement Closure

> Use when wrapping an engagement — before archiving, invoicing, and retrospective.

### Definition of Ready — Engagement Closure

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-ECL-001 | All in-flight deliverables either shipped or formally deferred with documented rationale | Deliverable log in ENGAGEMENT_INDEX.md shows no orphaned items | Yes | both |
| DOR-ECL-002 | Stakeholder accept-or-reject signal received on all major deliverables | Email/message/session transcript captures client response | Yes | brien |
| DOR-ECL-003 | Final invoice or billing record prepared | Financials/ shows invoice artifact | Yes | brien |
| DOR-ECL-004 | Any NDA-sensitive materials confirmed to be engagement-scoped (not in Core/) | Placement resolver scan: no client-confidential content in Core/ | Yes | agent |

### Definition of Done — Engagement Closure

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-ECL-001 | Deliverables archived: all final versions in `deliverables/` with clear naming | Glob `deliverables/**` returns all shipped artifacts | Yes | agent |
| DOD-ECL-002 | Retrospective captured as a signal: what worked, what didn't, what to carry forward | Signal file in `.intent/signals/` tagged `retro` | Yes | agent |
| DOD-ECL-003 | Invoice cycle confirmed closed: sent + received acknowledgment | Financial record in engagement `financials/` | Yes | brien |
| DOD-ECL-004 | Glossary entry added if new reusable IP or terminology emerged from this engagement | `Workspaces/memory/glossary.md` updated OR `engagement/glossary.md` updated | Yes | agent |
| DOD-ECL-005 | ENGAGEMENT_INDEX.md updated with closure date and final status | `status: closed` and `closed_date: YYYY-MM-DD` in frontmatter | Yes | agent |

---

## Persona Enrichment Pass

> Use for any corpus enrichment run targeting named-human or archetype personas.

### Definition of Ready — Persona Enrichment Pass

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-PEP-001 | Target persona(s) listed explicitly with registry slugs | Session or spec lists slugs (e.g., `teresa-torres`, `april-dunford`) | Yes | agent |
| DOR-PEP-002 | `sources.yaml` inventory present for each target persona (may be empty but must exist) | File exists at `Core/personas/corpus/[slug]/sources.yaml` | Yes | agent |
| DOR-PEP-003 | Current depth scores synced: registry YAML, processing-log, and enrichment dashboard agree | Cross-check `rendering.depth_score` in registry vs. dashboard | Yes | agent |
| DOR-PEP-004 | Research ceiling declared (free sources only? paid? Opus synthesis authorized?) | Ceiling stated in session or prior signal | No | brien |

### Definition of Done — Persona Enrichment Pass

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-PEP-001 | Corpus files written: at least one new source file per target persona | Files in `Core/personas/corpus/[slug]/` with new content | Yes | agent |
| DOD-PEP-002 | `sources.yaml` updated with all new source discoveries and ingestion status | `sources.yaml` modified date > enrichment start time | Yes | agent |
| DOD-PEP-003 | Processing-log entry added: timestamped record of what was ingested and from where | `processing-log.md` entry in corpus dir | Yes | agent |
| DOD-PEP-004 | Enrichment dashboard updated: depth scores, corpus file counts, last-updated timestamps | `Core/personas/docs/enrichment-dashboard.md` reflects current state | Yes | agent |
| DOD-PEP-005 | Signals captured for any findings that change Brien's understanding of a persona | Signal filed OR "n/a" declared with reason | Yes | agent |
| DOD-PEP-006 | Opus synthesis gate: if synthesis was authorized, synthesis artifact exists at persona corpus | `synthesis.md` exists OR synthesis explicitly deferred with reason | No | both |

---

## Critique Panel

> Use for any panel-critique run (formal or rapid mode).

### Definition of Ready — Critique Panel

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-CPL-001 | Artifact path is resolvable: the thing to be critiqued exists at a readable path | File or content block accessible to agent | Yes | agent |
| DOR-CPL-002 | Persona set selected OR selection criteria specified (domain, tension balance, etc.) | Persona slugs listed OR criteria documented in session | Yes | brien |
| DOR-CPL-003 | Preset chosen (comprehensive / rapid / devil-devil / challenge-only) OR all knobs explicit | Preset named OR explicit stance/depth configuration provided | Yes | both |
| DOR-CPL-004 | Output destination declared (inline response, file, specific path) | Output target stated | No | brien |

### Definition of Done — Critique Panel

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-CPL-001 | Per-persona output rendered: each selected persona produced a critique | N critique blocks present (one per selected persona) | Yes | agent |
| DOD-CPL-002 | Disagreement log produced (unless rapid mode explicitly selected) | Disagreement log section present OR rapid mode noted | Yes | agent |
| DOD-CPL-003 | Summary written: synthesis of key tensions, actionable recommendations | Summary section present at end of output | Yes | agent |
| DOD-CPL-004 | Output filed at declared destination if a path was specified | File exists at stated output path | No | agent |
| DOD-CPL-005 | Sycophancy guard applied: no persona produced only-positive output without challenge | Review per `sycophancy-guard.md` criteria | Yes | agent |

---

## Signal Closure

> Use whenever a signal is being transitioned to `resolved`, `deferred`, or `symptom-repaired, upstream-pending`. Introduced 2026-04-16 per SIG-F-001. Enforces that closure cannot happen without the upstream control being in place (or explicitly deferred with rationale).

### Definition of Ready — Signal Closure

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-SCL-001 | The signal's Implication / Proposed Resolution section is read and its upstream recommendation is identified | Closer can state the upstream control in one sentence | Yes | agent |
| DOR-SCL-002 | Closer has searched the target codebase / spec repo for evidence that the upstream control exists | Search commands recorded or cited | Yes | agent |
| DOR-SCL-003 | Closer has classified the closure: `resolved` (control installed), `deferred` (with rationale + date), or `symptom-repaired, upstream-pending` | Classification stated explicitly | Yes | agent |

### Definition of Done — Signal Closure

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-SCL-001 | If `resolved`: Resolution section cites the upstream control's file path and ID (gate, policy, DoD, emission helper, etc.) | File path / ID present in signal body | Yes | agent |
| DOD-SCL-002 | If `resolved`: closer answers "how would the same defect class be caught if reintroduced?" with a concrete mechanism (test, lint, pre-commit, DoD gate) | Answer present in Resolution or Follow-up | Yes | agent |
| DOD-SCL-003 | If `deferred`: `deferral_rationale:` and `reassess_by:` (ISO date) present in frontmatter | Both fields present | Yes | agent |
| DOD-SCL-004 | If `symptom-repaired, upstream-pending`: follow-up work enumerated with owner and target date | Follow-up section present | Yes | agent |
| DOD-SCL-005 | Related / superseding signals cross-referenced in frontmatter | `related:` / `supersedes_in:` fields populated where applicable | Yes | agent |

---

## YAML-Emitting Stage

> Use for any pipeline stage that writes `.yaml` / `.yml` files (persona-intake IDENTIFY/HARVEST/RENDER, fieldbook ledger, skills-engine registry emission, engagement schema files). Introduced 2026-04-16 per SIG-046 / SIG-F-001. Prevents the recurring class of "LLM wrote YAML with unescaped colons / nested quotes / bad indentation, defect only caught at consumption."

### Definition of Ready — YAML-Emitting Stage

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-YML-001 | Emission path declared: library-based (`yaml.safe_dump` via helper) OR template-with-validation. Hand-templated without validation is NOT a valid path | Path stated in spec / SKILL.md | Yes | agent |
| DOR-YML-002 | Validation gate available: `yaml.safe_load` helper callable from the stage | Helper path + invocation stated | Yes | agent |

### Definition of Done — YAML-Emitting Stage

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-YML-001 | Every YAML file emitted by this stage parses cleanly with `yaml.safe_load()` | Validation gate output recorded (pass for N files) | Yes | agent |
| DOD-YML-002 | On validation failure, stage is BLOCKED from closing. Defects surfaced with file + line + error | Failure produces non-zero exit from validation helper | Yes | agent |
| DOD-YML-003 | On validation failure, a signal is auto-captured describing the cohort shape (so premature-closure doesn't recur) | Signal file present under `.intent/signals/` or deferral documented | Yes | agent |

---

## Using These in Specs

Every new spec should reference the applicable DoR/DoD from this library plus any work-specific conditions:

```markdown
## Definition of Ready
<!-- Load from dor-dod-library.md: [work-type] -->
| DOR-SKB-001 | ... | ... | Yes | agent |
| DOR-SKB-002 | ... | ... | Yes | agent |
<!-- Work-specific additions: -->
| DOR-001 | [custom condition for this specific build] | [verification] | Yes | agent |

## Definition of Done
<!-- Load from dor-dod-library.md: [work-type] -->
| DOD-SKB-001 | ... | ... | Yes | agent |
<!-- Work-specific additions: -->
| DOD-001 | [custom condition for this specific build] | [verification] | Yes | agent |
```

---

## Version History

| Date | Change | Author |
|------|--------|--------|
| 2026-04-14 | Initial: 6 work types — skill-build, spec-authoring, engagement-kickoff, engagement-closure, persona-enrichment, critique-panel | brien/agent |
