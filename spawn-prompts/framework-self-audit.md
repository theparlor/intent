---
title: Intent Framework — Self-Audit Prompt
id: SPAWN-FRAMEWORK-SELF-AUDIT
type: spawn-prompt
created: 2026-05-20
depth_score: 2
depth_signals:
  file_size_kb: 4.8
  content_chars: 4518
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.22
scope: framework-only
weight: light
parent: overnight-exhaustive-upgrade.md
---
# Intent Framework Self-Audit

> Lighter than `overnight-exhaustive-upgrade.md`. Targets the Intent framework repo only.
> Use this when you want a targeted audit of Intent's own health without the full
> overnight orchestrator's cross-product scope.

## Working Dir
`/Users/brien/Workspaces/Core/frameworks/intent/`

## Posture
L4. Read-heavy, emit signals and patch documentation. Do not build new hooks or
specs inline — emit trigger signals for those instead and let subsequent IDD loops
execute them.

## Audit Dimensions (run all in parallel where possible)

### 1 — IDD Dogfood
Does `.intent/` use the Notice→Spec→Execute→Observe loop correctly?
- Are signals being captured and triaged (check recent mtime in `.intent/signals/`)?
- Are specs being authored and approved (check `.intent/specs/`)?
- Is the Observe stage wired (check `.intent/events/events.jsonl` recency)?
- Is the double-loop (Observe → Knowledge update) active or still specced-only?

### 2 — 5-Layer Closure-Discipline Enforcement
Verify all 5 layers are deployed and not drifted:
- Layer 1: `~/.claude/hooks/closure-discipline-check.sh` — present + executable?
- Layer 2: `memory/feedback_closure_discipline.md` — present?
- Layer 3: Soft-queue regex in stop hook — present in `closure-discipline-stop-check.sh`?
- Layer 4: Stop hook deployed + registered in `~/.claude/settings.json`?
- Layer 5: PreToolUse signal-file check — present in `~/.claude/hooks/closure-discipline-signal-check.sh`?
- Table-cell extension: does `COMPLETION_RE` in Layer 4 include `| Done |` / `| ✅ |` pattern?

### 3 — 5-Layer Autonomy-Grant Enforcement
Verify all 6 layers (5 in spec + dispatch hook as Layer 5/6):
- Layer 1: `~/.claude/hooks/autonomy-grant-check.sh` — present + registered?
- Dispatch hook: `~/.claude/hooks/autonomy-grant-dispatch-prompt-check.sh` — present?
- Drift catalog Family 1.7 (artificial-gate) present in `learnings/process-drift-catalog.md`?

### 4 — Signal-Stream Operational Health
- Count total signals in `.intent/signals/` and report breakdown by naming convention
- Are new signals using ULID format (per SPEC-003) or still using legacy `SIG-NNN`/date-slug?
- Report count of legacy-named signals created after SPEC-003 date (2026-04-09)
- Is `spec/signal-stream.md` present and referencing current closure-DoD triad schema?

### 5 — Process-Drift-Catalog Completeness
- Read `learnings/process-drift-catalog.md`
- Count families and entries
- Verify Family 1.7 (Artificial-gate) and Family 4.7 (Governance-skill-without-trigger) are present
- Identify any signals in `.intent/signals/` that reference a drift pattern not yet in catalog

### 6 — Spawn-Prompt Library Coverage
- List all files in `spawn-prompts/`
- Identify any recurring spawn workflow that lacks a prompt (check recent session history for patterns)

### 7 — Documentation Health
- Is `VERSION` current? Compare against most-recent CHANGELOG entry
- Is `CHANGELOG.md` within 30 days of today? If not, flag as stale
- Is `TASKS.md` updated? Check for items from most recent audit
- Does `CLAUDE.md` MCP tool count match actual tool definitions in `tools/intent-mcp/server.py`?

### 8 — Overwatch Hook
- Is `~/.claude/hooks/overwatch-staleness-check.sh` present and registered in `~/.claude/settings.json`?
- What is the mtime of the most recent `JRN-*overwatch*` file in any known journal directory?
- If >7 days, emit a signal noting the staleness

## Output Format

For each dimension:
1. **Finding:** one-line summary (Pass / Partial / Gap)
2. **Gap detail** (only if not Pass): what is missing, what file/path, what action needed
3. **Signal emitted** (if gap is actionable): filename of signal emitted to `.intent/signals/`

## Signal Emission Rules
- Emit a signal for every gap that requires a follow-on IDD loop (new hook, new spec, migration)
- Do NOT inline-build new hooks or specs — emit trigger signals only
- Use filename pattern: `SIG-SELF-AUDIT-{DIMENSION}-{DATE}.md`

## Commit Pattern
```bash
cd /Users/brien/Workspaces/Core/frameworks/intent
git add .intent/signals/ TASKS.md CHANGELOG.md VERSION
git commit -m "audit(intent): framework self-audit $(date +%Y-%m-%d) — {N} gaps found, {M} signals emitted

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
git push origin HEAD
```

## Acceptance
- [ ] All 8 dimensions assessed
- [ ] Gap signals emitted for actionable findings
- [ ] TASKS.md updated if new gaps found
- [ ] CHANGELOG.md + VERSION bumped if documentation is stale
- [ ] Push lands
