---
id: SIG-2026-06-10-build-intake-gate-d4-scoped
type: signal
status: resolved
severity: medium
created: 2026-06-10
target: "Build-intake gate (G4 collision) — skill-intake mandate scoped to outward-facing + irreversible build classes per D4"
discovered_during: "2026-06-10 architecture-vs-intents review (Core/products/parallax/research/2026-06-10-architecture-vs-intents-review.md, gap G4 / decision D4): build-intake-mandatory fired at L0 on ANY build/create/make request, while the ratified doctrine (validation-economy §2; docket charter §7) holds that pre-build gates on reversible work are drag with no risk being managed. Two operating strategies simultaneously in force. Brien adjudicated D4 on 2026-06-10: accept the recommendation — scope the gate to the classes the inversion preserves."
requested_by: brien (D4 adjudication 2026-06-10, via workflow orchestration)
verification_command: "grep -q 'D4 adjudication' /Users/brien/.claude/hooks/skill-intake-gate-check.sh && grep -q 'GATED_CLASS_PATTERNS' /Users/brien/.claude/hooks/skill-intake-gate-check.sh && grep -q 'BUILD_INTAKE_BYPASSED' /Users/brien/.claude/hooks/skill-intake-gate-check.sh && grep -q 'D4-scoped' /Users/brien/.claude/skills/build-intake-mandatory/SKILL.md && printf '%s' '{\"session_id\":\"sig-verify-reversible\",\"tool_name\":\"Agent\",\"tool_input\":{\"prompt\":\"build a skill for parsing receipts inside fieldbook with tests\"}}' | /Users/brien/.claude/hooks/skill-intake-gate-check.sh >/dev/null 2>&1 && printf '%s' '{\"session_id\":\"sig-verify-outward\",\"tool_name\":\"Agent\",\"tool_input\":{\"prompt\":\"build a tool to publish the public site to github pages\"}}' | /Users/brien/.claude/hooks/skill-intake-gate-check.sh >/dev/null 2>&1; [ $? -eq 2 ] && echo VERIFIED"
upstream_control_path: "/Users/brien/.claude/hooks/skill-intake-gate-check.sh — the Layer 1 PreToolUse hook IS the enforcement point; the scope rule now lives in its GATED_CLASS_PATTERNS block (D4 scope check). Second surface (two-surface lesson): /Users/brien/.claude/skills/build-intake-mandatory/SKILL.md (Layer 2 SessionStart cognitive surface) updated in the same pass — rule text, layer table, protocol trigger, and frontmatter description all carry the D4 scoping."
catch_mechanism: "NEW firing ledger written by the hook itself: ~/.claude/audit/build-intake-gate-firings.log records GATED-FIRE / SCOPED-PASS / FLAG-PASS dispositions per dispatch — this is the concrete substrate the review's gate-ablation pass (currently a sketch, per G4) will read when it is built. Until the ablation pass exists, the ledger is capture-only (no automated consumer); Layer 5 overwatch session-end audit remains the standing post-hoc reviewer of gate behavior. Honest status: the ledger is the monitor's data feed, not yet the monitor."
pipeline_survival: "The scope rule survives in the hook (machine-enforced at every Agent dispatch), in the SKILL.md loaded every SessionStart, and in the hook header changelog citing the D4 adjudication + review path. The bypass escape (BUILD_INTAKE_BYPASSED=1 -> ~/.claude/audit/build-intake-bypasses.log) is preserved byte-for-byte in behavior."
reconsider_when:
  - "The gate-ablation pass is built -> point it at build-intake-gate-firings.log; if SCOPED-PASS builds show the rework anti-pattern SIG-045 was created to prevent (composition-audit skips causing rework), the D4 scope is too narrow — widen the gated classes with evidence."
  - "An outward-facing or irreversible build slips through ungated (false negative in GATED_CLASS_PATTERNS) -> add the missed phrasing to the pattern list; Layer 5 overwatch audit is the detector."
  - "Brien reverses D4 or the validation-economy doctrine is amended -> restore the unscoped gate by deleting the D4 scope-check block (single bounded block, marked with dated comments)."
verification_run_at: 2026-06-10
---
# Build-intake gate scoped to D4-preserved classes

## What changed

**1. `/Users/brien/.claude/hooks/skill-intake-gate-check.sh` (Layer 1, the enforcement hook):**
- Added a D4 scope check between build-pattern matching and the bypass/flag/block logic: after a prompt matches a build-trigger phrase, it must ALSO match a `GATED_CLASS_PATTERNS` entry for the gate to engage.
- Gated classes implemented exactly per the adjudication: (a) outward-facing — public site/page/repo/release, GitHub Pages, publish, client-facing, deliverable-for, external integration/service/API/webhook, MCP/connector tied to external/third-party; (b) irreversible-class — new (top-level) product, new public repo, category/positioning artifact/narrative, marketing narrative/positioning.
- Reversible local builds (scripts, tests, schemas, docs, extensions inside existing products) now exit 0 with a `SCOPED-PASS` ledger entry instead of blocking.
- `BUILD_INTAKE_BYPASSED=1` escape + its audit logging to `~/.claude/audit/build-intake-bypasses.log`: **unchanged** (verified by test T4 — bypass allowed and logged).
- New ledger `~/.claude/audit/build-intake-gate-firings.log`: GATED-FIRE (blocked), SCOPED-PASS (build matched, class not gated), FLAG-PASS (gate satisfied via session flag).
- Dated changelog block added to the hook header citing D4 adjudication 2026-06-10 and the review path.

**2. `/Users/brien/.claude/skills/build-intake-mandatory/SKILL.md` (Layer 2, SessionStart surface):**
- Frontmatter description + rule body rewritten to the scoped classes; reversible-local pass-through stated explicitly ("do not invoke skill-intake reflexively — that is unmanaged drag").
- Layer table notes the hook's D4 scoping + firing ledger. Changelog blockquote cites D4 + review path.
- 5-layer architecture, protocol steps (CATCH → … → DEPLOY-GATE), banner, and session-flag mechanics untouched.

## Test evidence (actual hook invocations, 2026-06-10)
| Case | Input | Expected | Actual |
|---|---|---|---|
| T1 reversible local ("build a skill … inside fieldbook, with tests and schema updates") | Agent dispatch | allow, SCOPED-PASS | exit 0, SCOPED-PASS logged |
| T2 outward-facing ("publish the intent-site to GitHub Pages as a public site") | Agent dispatch | block | exit 2, `{"continue": false}` emitted, GATED-FIRE logged |
| T3 irreversible ("create a new top-level product directory … positioning artifact") | Agent dispatch | block | exit 2, GATED-FIRE logged |
| T4 bypass (T2 prompt + BUILD_INTAKE_BYPASSED=1) | Agent dispatch | allow + audit | exit 0, BYPASS line appended to build-intake-bypasses.log |
| T5 non-Agent tool | Bash tool input | allow | exit 0 |

## Surfaces audited and NOT changed (with reason)
- `Core/products/forge/outputs/claude-code/meta/skill-intake/SKILL.md` — the skill-intake protocol itself; D4 changes WHEN the protocol is mandatory, not WHAT it does. Out of D4 scope.
- `Core/frameworks/intent/spec/` — no build-intake spec exists; `autonomy-grant-enforcement.md` references the 5-layer pattern as architecture precedent only, no scope statement to reconcile.
- `~/.claude/settings.json` hook registration — unchanged (same hook path, same PreToolUse event).
- `memory/feedback_build_intake_enforcement_active.md` — one-line memory pointer; its claim ("all 5 layers live") remains true. Left to the memory-maintenance loop; the operative surfaces both carry the scoping.
