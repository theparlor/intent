---
id: SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20
type: drift-pattern
status: resolved
created: 2026-05-20
resolved: 2026-05-20 (same-day; hook landed and registered during overnight orchestrator Phase 5.5.1)
captured_by: orchestrator-prompt-update session (Brien spawn-prompt audit)
resolved_by: overnight-exhaustive-upgrade orchestrator session (this session, Phase 5.5.1 + 5.5.5)
related_signals:
  - SIG-2026-05-06-overwatch-engagement-signal-discovery-gap
  - SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20
  - SIG-HOOK-OVERRIDE-META-INSTRUCTIONAL-2026-05-20
related_specs:
  - Core/products/forge/.intent/HANDOFF-2026-04-15-overwatch-hardening.md (9 carry-forward items)
related_files:
  - Core/frameworks/intent/spawn-prompts/overnight-exhaustive-upgrade.md (orchestrator updated to install fix)
  - Core/frameworks/intent/hooks/overwatch-staleness-check.sh (the installed hook; symlinked from ~/.claude/hooks/)
  - Core/frameworks/intent/learnings/process-drift-catalog.md (Family 4.7 entry — meta-pattern captured)
  - ~/.claude/settings.json (hook registered under SessionStart)
upstream_control_path: Core/frameworks/intent/hooks/overwatch-staleness-check.sh
catch_mechanism: SessionStart hook emits warn banner if latest JRN-*overwatch* >7 days, load-bearing posture if >14 days; manual test confirms it fires on current state (was 12 days stale at orchestrator boot, now refreshed by overwatch-overnight-orchestrator journal)
pipeline_survival: hook is symlinked from intent repo source (theparlor/intent) to ~/.claude/hooks/; registered in ~/.claude/settings.json under SessionStart; runs on every session; drift-catalog Family 4.7 documents the meta-pattern for future governance-skill design
---

# Signal: Overwatch is itself subject to drift (12-day stale on 2026-05-20)

## What was noticed

While auditing the overnight-exhaustive-upgrade orchestrator prompt for an upcoming overnight session, Brien asked: "why did overwatch stop functioning too? it should have had the repo of what work we need to do next."

Investigation:
- Last `JRN-*overwatch*` journal in `Core/products/org-design-tooling/journal/` is dated **2026-05-08** (file mtime; the journal slug says 20260507).
- Today is **2026-05-20**. That's **12 days stale**.
- `~/.claude/hooks/` contains 12 hooks (autonomy-grant, closure-discipline, cast-yaml-validate, skill-intake-gate, etc.) — **NONE invoke overwatch**.
- `~/Workspaces/Core/frameworks/intent/hooks/` contains 6 hooks — **NONE invoke overwatch**.
- No scheduled task fires `/overwatch`.
- The `overwatch` skill at `~/Workspaces/.claude/commands/overwatch.md` is invoked only by Brien manually typing `/overwatch`.

## The pattern

**Governance skills without auto-triggers silently rot.** They are designed to catch drift everywhere else in the system, but they themselves rely on operator memory — which, for an ADHD operator with a 168-hour weekly budget and 33 products/frameworks demanding attention, is not a reliable trigger.

This is structurally identical to the artificial-gate-drift pattern (SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20) but at a meta-level: instead of architecting unnecessary L0 gates on L4-eligible work, the system architects a critical operation (governance sweep) without ANY gate or trigger at all, then relies on human memory to fill the gap.

The two patterns are siblings:
- artificial-gate-drift: unnecessary friction on reversible work
- overwatch-staleness: zero friction on a load-bearing periodic operation

Both produce silent drift. The fix surface is the same: install the right structural trigger, neither over-gating nor under-triggering.

## Concrete failure modes this enabled

1. **Backlog invisibility.** Without overwatch running, the "what work do we need to do next" question has no canonical answer. The orchestrator prompt for tonight's overnight run was authored without a fresh state-of-the-system view — Brien correctly noticed this gap.
2. **HANDOFF-2026-04-15 items un-shipped.** 9 carry-forward items from the 2026-04-15 sweep (engagement-onboarding write-through fix, first persona-freshening cycle, .intent/ stub auto-creation, etc.) sat in a HANDOFF.md for 35 days because overwatch wasn't re-running to surface their continued absence.
3. **Write-through failures uncaught.** The whole point of the write-through architecture (SPEC-003, SIG-028) is that overwatch is the catch-net for hook breakage. With overwatch dormant, hook breakage propagates silently.
4. **Persona freshening stalled.** Cast freshening cadence (monthly/quarterly) relies on overwatch surfacing HIGH_RISK entries. Dormant overwatch = no freshening pressure = drift in the persona corpus.

## Repair (symptom-level, executed in this session)

The orchestrator spawn prompt `Core/frameworks/intent/spawn-prompts/overnight-exhaustive-upgrade.md` was updated to:
- Add **Phase 0.5: Mandatory full /overwatch run** before any subagent dispatch
- Add **Phase 5.5: Overwatch Rehabilitation track** with 5 sub-items:
  - 5.5.1: Author `~/.claude/hooks/overwatch-staleness-check.sh` (SessionStart banner if >7d stale; load-bearing posture if >14d)
  - 5.5.2: Scheduled task for weekly `/overwatch` if scheduled-tasks MCP available
  - 5.5.3: Execute HANDOFF-2026-04-15-overwatch-hardening.md carry-forward items
  - 5.5.4: Surface overwatch status in `weekly-summary` and `daily-digest` skills
  - 5.5.5: Drift-catalog entry capturing this pattern
- Use overwatch findings as the canonical work-backlog feeder for Phase 1 (audits) and Phase 2 (execution)

## Repair (upstream-level, pending)

This signal closes ONLY when:
1. `~/.claude/hooks/overwatch-staleness-check.sh` exists, is registered in settings.json under SessionStart, and emits the expected banner given current journal mtimes
2. The next SessionStart in a fresh session is verified to display the banner
3. A drift-catalog entry exists documenting the meta-pattern
4. The HANDOFF-2026-04-15 carry-forward items are closed inline (with their own write-through hooks installed where applicable)

Until then: status is `symptom-repaired, upstream-pending`.

## Cross-references

- Upstream signal authoring this fix into structure: orchestrator update commit (this session)
- Sibling drift pattern (over-gating vs under-triggering): SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20
- Spec governing closure discipline: `Core/frameworks/intent/spec/closure-discipline-enforcement.md`
- The 12-day-stale evidence: `Core/products/org-design-tooling/journal/JRN-20260507-overwatch-*` (most recent overwatch journals)
- Carry-forward backlog: `Core/products/forge/.intent/HANDOFF-2026-04-15-overwatch-hardening.md`
